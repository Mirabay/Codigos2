from djitellopy import Tello
import cv2
import numpy as np

# Frame source: 0-> from webcam 1-> from drone
frame_source = 0

# HSV initial values
H_min = 70
H_max = 125
S_min = 130
S_max = 200
V_min = 120
V_max = 255
# create HSV min and max arrays
hsv_min = np.array([H_min,S_min,V_min])
hsv_max = np.array([H_max,S_max,V_max])

deadzone = 50

area_min = 800
def callback(x):
	global hsv_max
	global hsv_min
	if frame_source == 0:
		H_min = cv2.getTrackbarPos('H_min', 'HSV Adjust')
		H_max = cv2.getTrackbarPos('H_max', 'HSV Adjust')
		S_min = cv2.getTrackbarPos('S_min', 'HSV Adjust')
		S_max = cv2.getTrackbarPos('S_max', 'HSV Adjust')
		V_min = cv2.getTrackbarPos('V_min', 'HSV Adjust')
		V_max = cv2.getTrackbarPos('V_max', 'HSV Adjust')
	hsv_min = np.array([H_min,S_min,V_min])
	hsv_max = np.array([H_max,S_max,V_max])

# Create a window
cv2.namedWindow("HSV Adjust")

# Create trackbars for color change
cv2.createTrackbar('H_min', 'HSV Adjust', H_min, 180, callback)
cv2.createTrackbar('H_max', 'HSV Adjust', H_max, 180, callback)
cv2.createTrackbar('S_min', 'HSV Adjust', S_min, 255, callback)
cv2.createTrackbar('S_max', 'HSV Adjust', S_max, 255, callback)
cv2.createTrackbar('V_min', 'HSV Adjust', V_min, 255, callback)
cv2.createTrackbar('V_max', 'HSV Adjust', V_max, 255, callback)

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
		img_tracking = img.copy()
		
		hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
		mask = cv2.inRange(hsv_img,hsv_min, hsv_max)
		result = cv2.bitwise_and(img,img,mask=mask)

		imgBlur = cv2.GaussianBlur(result,(7,7),1)
		imgGray = cv2.cvtColor(imgBlur,cv2.COLOR_BGR2GRAY)

		contours,hierachy = cv2.findContours(imgGray,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
		for cnt in contours:
			area = cv2.contourArea(cnt)
			if area > area_min:
				cv2.drawContours(img_tracking,cnt,-1,(255,0,255),7)
				peri = cv2.arcLength(cnt,True)
				approx = cv2.approxPolyDP(cnt,0.02*peri, True)
				x,y,w,h = cv2.boundingRect(approx)
				cv2.rectangle(img_tracking,(x,y),(x+w,y+h),(0,255,0),0)
				print(x,y)

		# Showing limit Lines
		cv2.line(img_tracking,((500//2)-deadzone,0),((500//2)-deadzone,500),(255,255,0),2)
		cv2.line(img_tracking,((500//2)+deadzone,0),((500//2)+deadzone,500),(255,255,0),2)



		# Writing the battery level in the image.... cv2.putText(ImageName, text, location, font, scale, color, thickness)
		if frame_source == 1:
			cv2.putText(img, 'Battery:  ' + str(drone.get_battery()), (0, 50), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 255, 0), 3)

		# Showing the image in a window
		cv2.imshow("Image", img_tracking)

		# Keyboard monitor
		key = cv2.waitKey(15) & 0xFF #esto puede dar algunos problemas pero es nuestro acceso desde el teclado

		if frame_source == 1 :
		# close the windows and break the program if 'q' is pressed
			if key == 113:
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
				drone.left_rigth_velocity = 0
				drone.foward_backward_velocity = drone.speed
				drone.up_down_velocity = 0
				drone.yaw_velocity = 0
				# Enviamos las velocidades
				drone.send_rc_control(drone.left_rigth_velocity,drone.foward_backward_velocity,drone.up_down_velocity,drone.yaw_velocity)
			# lands if 's' is pressed
			elif key == 's': #108
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
