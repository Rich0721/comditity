import cv2
import os
from glob import glob
import numpy as np



def remove_background(image_source):
    background = cv2.imread("background_003.jpg")
    foreground = cv2.imread(image_source)
    gray_f = cv2.cvtColor(foreground, cv2.COLOR_BGR2GRAY)
    gray_b = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)
    gray = cv2.absdiff(gray_f, gray_b)
    ret, thresh = cv2.threshold(gray, 70, 255, cv2.THRESH_BINARY_INV)

    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=20)
    _, cns, _ = cv2.findContours(opening.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    cv2.imshow("test", opening)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    '''
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)

    bg = cv2.dilate(opening, kernel, iterations=3)

    dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    ret, fg = cv2.threshold(dist_transform, 0.7*dist_transform.max(), 255, 0)

    fg = np.uint8(fg)
    unknown = cv2.subtract(bg, fg)

    ret, makers = cv2.connectedComponents(fg)
    makers = makers + 1

    makers[unknown==255] = 0

    makers = cv2.watershed(foreground, makers)
    foreground[makers == -1] = [255, 255, 255]
    '''
    '''
    cv2.imshow("test", foreground)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    '''
remove_background(image_source="0.jpg")