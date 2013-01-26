from bottle import Bottle, run, static_file

app = Bottle()

@app.get('/')
def hello():
	return static_file('index.html','static')

@app.get('/balou')
def GetBalou():
	return 'Show Balou'

@app.get('/catdoor')
def GetCatdoor():
	return 'Show Catdoor'

@app.put('/catdoor')
def PutCatdoor():
	return 'Edit Catdoor'

run(app, host='0.0.0.0', port=8080, debug=True)
