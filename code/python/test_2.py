from __future__ import division
from picamera.array import PiRGBArray
from picamera import PiCamera
from fonction import *
from ligne import *
import RPi.GPIO as gpio
import sys
import smbus
import time
import cv2
import numpy as np


adress=0x03

#adresse I2C
bus=smbus.SMBus(1)

time.sleep(2)
print("adresse I2C", adress)
gpio.setmode(gpio.BCM)
gpio.setup(17, gpio.OUT)
flag =0
flagD =0
flagDD=0
flagG =0
flagDG=0
flagA =0
flagF =0
flagAV =0
camera=PiCamera()
camera.resolution=(1250, 600)#L*H
camera.framerate=49
rawCapture = PiRGBArray(camera, size=(1250,600))

time.sleep(0.1)
#CVPoint objectPos = cvPoint(-1,-1)
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):


    image = frame.array
    #cv2.imshow("Frame", image)

    key =cv2.waitKey(1) & 0xFF
    
    rawCapture.truncate(0)

    #Im=cv2.imread(image[1])
    #hsv=cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    im_gray=cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    hsv2 = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)

    (thresh, im_bw) =cv2.threshold(im_gray, 128,255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)



    transfo = np.ones(image.shape, dtype="uint8")*50 # creation de notre matrice de transformation
    eclair = cv2.add(image, transfo) #creation de notre image plus lumineuse
    sombre = cv2.subtract(image, transfo)
    





    cropped = image [500:600 , 1:1250]
    hsv = cv2.cvtColor(cropped, cv2.COLOR_RGB2HSV)



    ret, seuil =cv2.threshold (hsv, 0,255,0)
    #cv2.imshow("hsv", hsv)
    lower_white=np.array([0, 0, 212])
    upper_white=np.array([131, 255, 255])

    mask=cv2.inRange(hsv, lower_white, upper_white)

    test = cv2.bitwise_and(cropped, cropped, mask=mask)
    

    
    kernel_erode = np.ones((4,4), np.uint8)
    eroded_mask =cv2.erode(mask,kernel_erode,iterations=1)
    kernel_dilate = np.ones((6,6), np.uint8)
    dilated_mask =cv2.dilate(eroded_mask, kernel_dilate, iterations=1)

    contours,hierarchy = cv2.findContours(dilated_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours,key=cv2.contourArea, reverse=True)[:1]

    




    """ ligne blanche 
    """
    if flagAV==0 :
        bus.write_byte(adress,1)
        print("marche")
        time.sleep(0.01)
        flagAV=1

    
    
                  
   
    
 

    #if flagF==0 :

    cx2=ligne2(cropped, contours)
    print("cx2", cx2)
    #flagDG,flagD, flagDD, flagG, flagA=ligne (cropped, flagD, flagDD, flagG, flagA, flagDG, contours)
    #    flagF=1

    #if flagF==0 :
    flag=stop(im_gray, flag, image)
     #  flagF=1
    """

    elif flagF==1 :
        #flag=feu(im_gray,flag,image)
        flagF=0

    """





    """ affichage images"""


    """ 
    #cv2.imshow("Frame", im_gray)
         
    cv2.line(image, (200,0), (200,600),(255,0,255))
    cv2.line(image, (525,0), (525,600),(255,0,255))
    cv2.line(image, (725,0), (725,600),(255,0,255))
    cv2.line(image, (1050,0), (1050,600),(255,0,255))
    #new_im=cv2.Canny(image,300,400)
    #cv2.imshow("Frame",image)"""
    #cv2.imshow("cropped", cropped)
    #cv2.imshow("Frame",im_gray)
    #cv2.imshow("Fram2e",image)
    """
    #cv2.imshow("Frame", image)
    cv2.imshow("eclair", eclair)
    """
