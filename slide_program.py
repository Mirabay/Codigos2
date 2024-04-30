from djitellopy import Tello
import cv2

# Frame source: 0-> from webcam 1-> from drone
frame_source = 1

# Initializing camera stream
if frame_source == 0:
	capture = cv2.VideoCapture(0)
elif frame_source == 1: # Aquí pon las velocidades del drone
	drone = Tello()
	drone.connect()
	drone.streamoff()
	drone.streamon()

	drone.left_rigth_velocity = 0
	drone.foward_backward_velocity = 0
	drone.up_down_velocity = 0
	drone.yaw_velocity = 0

	drone.speed = 50
	drone.status = 0
	
# Creamos una ventana para el slider
cv2.namedWindow('Trackbar')
cv2.resizeWindow('Trackbar', (500,100))

# callback para el slider de velocidad
def callback(x):
	if frame_source == 1:
		drone.speed = cv2.getTrackbarPos('Speed','Trackbar')


# Creamos el Trackbar para la velocidad
cv2.createTrackbar('Speed','Trackbar',0,100,callback)

cv2.setTrackbarPos('Speed','Trackbar',in_speed)

def main():
	print("main program running now")
	# Ciclo principal
	while True:
		# Obtaining a new frame
		if frame_source == 0:
			ret, img = capture.read()
		elif frame_source == 1:
			frame_read = drone.get_frame_read()
			img = frame_read.frame
			img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)

		# Rotating the image
		img = cv2.flip(img, 1)

		# Resizing the image --- cv2.resize('ImageName',(x_dimension,y_dimension))
		img = cv2.resize(img, (500, 500))

		# Writing the battery level in the image.... cv2.putText(ImageName, text, location, font, scale, color, thickness)
		if frame_source == 1:
			cv2.putText(img, 'Battery:  ' + str(drone.get_battery()), (0, 50), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 255, 0), 3)

		# Showing the image in a window
		cv2.imshow("Image", img)

		# Keyboard monitor
		key = cv2.waitKey(15) & 0xFF #esto puede dar algunos problemas pero es nuestro acceso desde el teclado
		key = chr(key)
		# close the windows and break the program if 'q' is pressed
		if key == 'q':
			cv2.destroyAllWindows()
			if frame_source == 1:
				drone.land()
				drone.streamoff()

				drone.end()
			break
		# take off if 't' is pressed
		elif key == 't': #116
			drone.status = 1
			drone.takeoff()
		# lands if 'l' is pressed
		elif key == 'l': #108
			drone.status = 0
			drone.land()

		## Movimientos mediante las velocidades 
		# lands if 'w' is pressed
		elif key == 'w': #119
			if drone.status == 1:
				drone.left_rigth_velocity = 0
				drone.foward_backward_velocity = drone.speed
				drone.up_down_velocity = 0
				drone.yaw_velocity = 0
			# Enviamos las velocidades
				drone.send_rc_control(drone.left_rigth_velocity,drone.foward_backward_velocity,drone.up_down_velocity,drone.yaw_velocity)
		# lands if 's' is pressed
		elif key == 's': #108
			if drone.status == 1:
				drone.left_rigth_velocity = 0
				drone.foward_backward_velocity = -drone.speed
				drone.up_down_velocity = 0
				drone.yaw_velocity = 0
				drone.send_rc_control(drone.left_rigth_velocity,drone.foward_backward_velocity,drone.up_down_velocity,drone.yaw_velocity)

		# lands if 'd' is pressed
		elif key == 'd': #108
			drone.left_rigth_velocity = drone.speed
			drone.foward_backward_velocity = 0
			drone.up_down_velocity = 0
			drone.yaw_velocity = 0
			drone.send_rc_control(drone.left_rigth_velocity,drone.foward_backward_velocity,drone.up_down_velocity,drone.yaw_velocity)

		# lands if 'a' is pressed
		elif key == 'a': #108
			drone.left_rigth_velocity = drone.speed
			drone.foward_backward_velocity = 0
			drone.up_down_velocity = 0
			drone.yaw_velocity = 0
			drone.send_rc_control(drone.left_rigth_velocity,drone.foward_backward_velocity,drone.up_down_velocity,drone.yaw_velocity)
		else:
			drone.left_rigth_velocity = 0
			drone.foward_backward_velocity = 0
			drone.up_down_velocity = 0
			drone.yaw_velocity = 0
			drone.send_rc_control(drone.left_rigth_velocity,drone.foward_backward_velocity,drone.up_down_velocity,drone.yaw_velocity)


try:
	main()

except KeyboardInterrupt:
	print('KeyboardInterrupt exception is caught')
	cv2.destroyAllWindows()
	if frame_source == 1:
		drone.land()
		drone.streamoff()
		drone.end()

else:
	print('No exceptions are caught')
