import cv2
import mediapipe as mp
import pyautogui

cap = cv2.VideoCapture(0)
hand_detector = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()
index_y = 0

scroll_speed = 30

drag_start_x = 0
drag_start_y = 0

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1840)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 680)

while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks

    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(frame, hand)
            landmarks = hand.landmark

            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)

                if id == 8:  # index finger
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                    index_x = screen_width / frame_width * x
                    index_y = screen_height / frame_height * y

                if id == 4:  # thumb
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                    thumb_x = screen_width / frame_width * x
                    thumb_y = screen_height / frame_height * y

                if id == 12:  # middle finger
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                    mid_x = screen_width / frame_width * x
                    mid_y = screen_height / frame_height * y

                if id == 16:  # ring finger
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                    ring_x = screen_width / frame_width * x
                    ring_y = screen_height / frame_height * y

                if id == 20:
                    cv2.circle(img=frame, center=(x, y), radius=8, color=(0, 255, 255))
                    pinky_x = screen_width / frame_width * x
                    pinky_y = screen_height / frame_height * y

                    # print(index_y - thumb_y, mid_y - thumb_y, ring_y-thumb_y, mid_y - index_y, mid_y-ring_y)
                    # s= abs(mid_y - index_y)
                    # q = abs(mid_y - ring_y)
                    if  abs(index_y - thumb_y) < 35:  # left click
                        pyautogui.leftClick()
                        pyautogui.sleep(1)

                    elif abs(mid_y - thumb_y) < 20:  # right click
                        pyautogui.rightClick()
                        pyautogui.sleep(1)

                    elif abs(ring_y - thumb_y) < 35:  # double click
                        pyautogui.doubleClick()

                    elif abs(mid_y - index_y) < 10:  # scroll up
                        pyautogui.scroll(100)

                    elif abs(mid_y - ring_y) < 10:  # scroll down
                        pyautogui.scroll(-100)

                    elif abs(pinky_y - thumb_y) < 35:
                        pyautogui.dragTo(pinky_x, pinky_y, duration=0.5)

                    elif abs(index_y - thumb_y) > 80:  # move cursor
                        pyautogui.moveTo(index_x, index_y, duration=0.03, tween=pyautogui.easeInOutQuad)



                cv2.imshow('Virtual Mouse', frame)
                cv2.waitKey(1)