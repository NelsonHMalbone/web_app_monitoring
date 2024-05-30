import cv2
import time

video = cv2.VideoCapture(1)
time.sleep(1)

first_frame = None

while True:
    check, frame = video.read()
    # convert the frame to a grayscale image to reduce data size
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply a Gaussian Blur to the frame  to further reduce data size
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)



    if first_frame is None:
        first_frame = gray_frame_gau


    # Compare the initial, "first_frame" with the current, filtered frame "gray_frame_gau"
    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)

    thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]

    dilate_frame = cv2.dilate(thresh_frame, None, iterations=2)

    cv2.imshow("My Vid", dilate_frame)

    key = cv2.waitKey(1)
    if key == ord("q"):
        break

video.release()