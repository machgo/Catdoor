f = open('../runtime/doorlock.state', 'w')
f.write('locked')
f.close()

f = open("../runtime/doorlock.state", 'r')
state = f.read()
print state
f.close()