import glob
import os

import cv2
import time
from backend import send_email

video = cv2.VideoCapture(1)
time.sleep(1)

first_frame = None
status_list = []
count = 1

def clean_folder():
    imgs = glob.glob("img/*.png")
    for image in imgs:
        os.remove(image)

while True:
    # if no object status is 0
    status = 0
    check, frame = video.read()

    # convert the frame to a grayscale image to reduce data size
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply a Gaussian Blur to the frame  to further reduce data size
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)



    if first_frame is None:
        first_frame = gray_frame_gau


    # Compare the initial, "first_frame" with the current, filtered frame "gray_frame_gau"
    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)

    thresh_frame = cv2.threshold(delta_frame, 20, 255, cv2.THRESH_BINARY)[1]

    dilate_frame = cv2.dilate(thresh_frame, None, iterations=2)
    cv2.imshow("video", frame)

    # contours of object
    contours, check = cv2.findContours(dilate_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) < 5530:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)

        # the section that will send email if we notice a rectangle
        if rectangle.any():
            # for when there is a object in view
            status = 1
            # saving a img
            # cv2.imwrite("image.png", frame) # static no go for this operation
            # dynamtic so it will add a number instead of saving over the same file name
            cv2.imwrite(f"img/image{count}.png", frame)
            count = count + 1
            all_imgs = glob.glob("img/*.png")
            index = int(len(all_imgs) / 2)
            img_with_obj = all_imgs[index]

    status_list.append(status)
    # showing the last two items in the list
    # looking for change or no change
    status_list = status_list[-2:]

    # object lef the frame in to send the email
    if status_list[0] == 1 and status_list[1] == 0:
        send_email(img_with_obj)
        clean_folder()

    cv2.imshow("video", frame)

    key = cv2.waitKey(1)
    if key == ord("q"):
        break

video.release()