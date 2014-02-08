import cv2.cv as cv
import time
import uuid
import sys
from daemon import Daemon
import os
import requests
import json

class MyDaemon(Daemon):
    def run(self):
        t = Target()
        t.run()

def UploadLog (message, eventnumber=0):
    payload = {"Title": "camera","Message": message, "EventNumber": eventnumber}
    headers = {'content-type': 'application/json'}

    try:
        r = requests.post("http://echo.home.balou.in:9321/DoorService/LogEntries", timeout=2.0, data=json.dumps(payload), headers=headers)
    except requests.exceptions.RequestException as e:
        print e

def UploadImage (filename, filePath):
    f = open (filePath, "rb")
    data = f.read();
    UU = data.encode("base64")

    payload = {"FileName": filename,"Data": UU}
    headers = {'content-type': 'application/json'}
    try:
        r = requests.post("http://echo.home.balou.in:9321/DoorService/Pictures", timeout=2.0, data=json.dumps(payload), headers=headers)
    except requests.exceptions.RequestException as e:
        print e


class Target:

    def __init__(self):
        self.capture = cv.CaptureFromCAM(0)
        UploadLog("Started CaptureFromCAM", 2001)
        # cv.SetCaptureProperty(self.capture, cv.CV_CAP_PROP_FRAME_HEIGHT, 1280)
        # cv.SetCaptureProperty(self.capture, cv.CV_CAP_PROP_FRAME_WIDTH, 960)
        # cv.SetCaptureProperty(self.capture, cv.CV_CAP_PROP_FORMAT, cv.IPL_DEPTH_32F)

    def run(self):
        # Capture first frame to get size
        frame = cv.QueryFrame(self.capture)
        frame_size = cv.GetSize(frame)
        color_image = cv.CreateImage(cv.GetSize(frame), 8, 3)
        grey_image = cv.CreateImage(cv.GetSize(frame), cv.IPL_DEPTH_8U, 1)
        moving_average = cv.CreateImage(cv.GetSize(frame), cv.IPL_DEPTH_32F, 3)

        first = True

        while True:
            closest_to_left = cv.GetSize(frame)[0]
            closest_to_right = cv.GetSize(frame)[1]

            color_image = cv.QueryFrame(self.capture)

            # Smooth to get rid of false positives
            cv.Smooth(color_image, color_image, cv.CV_GAUSSIAN, 3, 0)

            if first:
                difference = cv.CloneImage(color_image)
                temp = cv.CloneImage(color_image)
                cv.ConvertScale(color_image, moving_average, 1.0, 0.0)
                first = False
            else:
                cv.RunningAvg(color_image, moving_average, 0.020, None)

            # Convert the scale of the moving average.
            cv.ConvertScale(moving_average, temp, 1.0, 0.0)

            # Minus the current frame from the moving average.
            cv.AbsDiff(color_image, temp, difference)

            # Convert the image to grayscale.
            cv.CvtColor(difference, grey_image, cv.CV_RGB2GRAY)

            # Convert the image to black and white.
            cv.Threshold(grey_image, grey_image, 70, 255, cv.CV_THRESH_BINARY)

            # Dilate and erode to get people blobs
            cv.Dilate(grey_image, grey_image, None, 18)
            cv.Erode(grey_image, grey_image, None, 10)

            storage = cv.CreateMemStorage(0)
            contour = cv.FindContours(grey_image, storage, cv.CV_RETR_CCOMP, cv.CV_CHAIN_APPROX_SIMPLE)
            points = []

            motionDetected = False

            if len(contour):
                motionDetected = True
                print "Motion detected, save to file..."
                
            if motionDetected:
                UploadLog("Motion Detected, Uploading Photo", 2011)
                filename = str(uuid.uuid1()) + ".jpg"
                fullname = "/opt/catdoor/camera/new/" + filename
                cv.SaveImage(fullname, color_image)
                UploadImage(filename, fullname)

            # else:
            #     filename = str(uuid.uuid1()) + ".jpg"
            #     fullname = "/opt/catdoor/camera/new/" + filename
            #     cv.SaveImage(fullname, color_image)
            #     UploadImage(filename, fullname)


            while contour:
                bound_rect = cv.BoundingRect(list(contour))
                contour = contour.h_next()

                pt1 = (bound_rect[0], bound_rect[1])
                pt2 = (bound_rect[0] + bound_rect[2], bound_rect[1] + bound_rect[3])
                points.append(pt1)
                points.append(pt2)
                cv.Rectangle(color_image, pt1, pt2, cv.CV_RGB(255,0,0), 1)

            if len(points):
                center_point = reduce(lambda a, b: ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2), points)
                cv.Circle(color_image, center_point, 40, cv.CV_RGB(255, 255, 255), 1)
                cv.Circle(color_image, center_point, 30, cv.CV_RGB(255, 100, 0), 1)
                cv.Circle(color_image, center_point, 20, cv.CV_RGB(255, 255, 255), 1)
                cv.Circle(color_image, center_point, 10, cv.CV_RGB(255, 100, 0), 1)

            time.sleep(2)


if __name__ == "__main__":
    daemon = MyDaemon('/opt/catdoor/camera/daemon-camera.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            UploadLog("Stopping daemon", 2002)
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            # t = Target()
            # t.run()

            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)