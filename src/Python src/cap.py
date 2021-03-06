import io
import socket
import struct
import time
from picamera import PiCamera 


client_socket = socket.socket()
client_socket.connect(("199.98.20.88",8000))

connection = client_socket.makefile('wb')


try:
	camera = PiCamera()
	camera.resolution = (640,480)
	camera.rotation = 180
	camera.start_preview()
	time.sleep(2)

	start = time.time()
	stream = io.BytesIO()
	for foo in camera.capture_continuous(stream, 'jpeg'):
		connection.write(struct.pack('<L',stream.tell()))
		connection.flush()
		stream.seek(0)
		connection.write(stream.read())
			
		if time.time() - start > 30:
			break
		stream.seek(0)
		stream.truncate()
	
	connection.write(struct.pack('<L',0))

finally:
	connection.close()
	client_socket.close()
