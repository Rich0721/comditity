import cv2
import os
import numpy as np

def image_process(background_image="background_002.jpg", foreground_image="0.jpg"):
    '''
    Extract foreground x, y, w, h
    Return xmin, ymin, xmax, ymax
    '''
    background = cv2.imread(background_image)
    foreground = cv2.imread(foreground_image)

    gray_background = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)
    gray_foreground = cv2.cvtColor(foreground, cv2.COLOR_BGR2GRAY)

    diff_both_image = cv2.absdiff(gray_background, gray_foreground)
    
    T, img = cv2.threshold(diff_both_image, 110, 255,  cv2.THRESH_BINARY)

   
    img = cv2.dilate(img, None, iterations=32)
    img = cv2.erode(img, None, iterations=32)
    img = cv2.dilate(img, None, iterations=16)
   

    _, cnts, _ = cv2.findContours(img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    xmin = 0
    ymin = 0
    xmax = 0
    ymax = 0

    max_area = 0
    
    for c in cnts:
        area = cv2.contourArea(c)
        x, y, w, h = cv2.boundingRect(c)
        area  = w * h
        
        
        if area > max_area:
            max_area = area
            xmin = x
            ymin = y
            xmax = x + w
            ymax = y + h
        
    
    #cv2.rectangle(foreground, (xmin, ymin), (xmax, ymax), (0, 0 ,255), 1)
    #cv2.imshow("111", foreground)
    #cv2.waitKey(0)
    
    return xmin, ymin, xmax, ymax

#image_process()

