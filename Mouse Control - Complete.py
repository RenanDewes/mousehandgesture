import cv2
import mediapipe as mp
import pyautogui

capturehands = mp.solutions.hands.Hands()
drawingOption = mp.solutions.drawing_utils

screenWidth, screenHeight = pyautogui.size()

x4 = y4 = 100
x8 = y8 = 1
x12 = y12 = 1
y14 = y16 = y20 = 1

blockedMouse = False
isClicked = False
leftClick = True
rightClick = True
doubleClick = True

camera = cv2.VideoCapture(0)

while True:
	_, image = camera.read()
	imgHeight, imgWidth, _ = image.shape
	image = cv2.flip(image, 1)
	rgbImg = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
	outputHands = capturehands.process(rgbImg)
	all_hands = outputHands.multi_hand_landmarks

	if all_hands:
		for hand in all_hands:
			drawingOption.draw_landmarks(image, hand)
			oneHandLandmarks = hand.landmark 

			for id, lm in enumerate(oneHandLandmarks):
				if (lm.x is not None) and (lm.y is not None):
					imgXAxis = int(lm.x * imgWidth)
					imgYAxis = int(lm.y *imgHeight)
					
				if id == 4:
					x4 = imgXAxis
					y4 = imgYAxis
				if id == 8:
					x8 = imgXAxis
					y8 = imgYAxis
					if blockedMouse == False:
						cv2.circle(image, (imgXAxis, imgYAxis), 15, (0, 255, 255))
						mouseXAxis = int(screenWidth / imgWidth * imgXAxis)
						mouseYAxis = int(screenHeight / imgHeight * imgYAxis)
						pyautogui.moveTo(mouseXAxis, mouseYAxis)
				if id == 12:
					y12 = imgYAxis
					x12 = imgXAxis
				if id == 14:
					y14 = imgYAxis
				if id == 16:
					y16 = imgYAxis
				if id == 20:
					y20 = imgYAxis

				if (x4 - x8) > (-30):
					blockedMouse = True

					if ((y14 - y8) < 0) and ((y14 - y12) > 30):
						
						if (leftClick == True) and (isClicked == False):
							pyautogui.mouseDown()
							isClicked = True
							leftClick = False
							
					else:
						leftClick = True
						isClicked = False
						pyautogui.mouseUp()
						print("esquerdo")


					if ((y14 - y12) < 0) and ((y14 - y8) > 30):

						if (rightClick == True) and (isClicked == False):
							pyautogui.mouseDown(button = 'right')
							isClicked = True
							rightClick = False
							
					else:
						rightClick = True
						isClicked = False
						pyautogui.mouseUp(button = 'right')
						print("direito")


					if ((y14 - y8) > 0) and ((y14 - y8) < 30) and ((y14 - y12) > 0) and ((y14 - y12) < 30):
						isClicked = True

						if (doubleClick == True):
							pyautogui.doubleClick()
							doubleClick = False
							print("duplo")
					else:
						doubleClick = True
						isClicked = False

				else:
					blockedMouse = False
						
	cv2.imshow("Hand Gesture", image)
	
	key = cv2.waitKey(5)
	if key == 27:
		break

camera.release()
cv2.destroyAllWindows()