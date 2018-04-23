from __future__ import division
from picamera.array import PiRGBArray
from picamera import PiCamera
import smbus
import time
import cv2
import numpy as np

#adresse I2C
bus=smbus.SMBus(1)
adress=0x1a




def stop(im_gray,flag, image):

    #detection stop

    template = cv2.imread('stop.png',0)
    
    
    w, h = template.shape[::-1]
    res =cv2.matchTemplate(im_gray, template ,cv2.TM_CCOEFF_NORMED)
    threshold = 0.4 
    loc= np.where( res >= threshold)
    if np.any( res >= threshold):
        print("stop")
        bus.write_byte(adress,6)
        time.sleep(5)
        flag =0
        
        if flag ==0:
            bus.write_byte(adress,4)
            print("avancer")
            time.sleep(1)
            flag =1
    else :
        
        if flag ==0:
            print("avancer")
            bus.write_byte(adress,4)
            flag =1
    for pt in zip(*loc[::-1]):
                  cv2.rectangle(image, pt, (pt[0]+w,pt[1]+h),(0,0,255),2)

    return flag










def feu(im_gray,flag, image):                  

    #detection feu rouge

    templateFeu = cv2.imread('feu_rouge.png',0)

    

    
    wF, hF = templateFeu.shape[::-1]
    resFeu =cv2.matchTemplate(im_gray, templateFeu ,cv2.TM_CCOEFF_NORMED)
    thresholdFeu = 0.8
    locFeu= np.where( resFeu >= thresholdFeu)
    if np.any( resFeu >= thresholdFeu):
        print("feu rouge")
        bus.write_byte(adress,6)
        time.sleep(5)
        flag =0
        print("flag : ", flag)
        if flag ==0 :
            bus.write_byte(adress,4)
            print("avancer")
            time.sleep(1)
            flag =1
    else :
        if flag ==0:
            print("avancer")
            bus.write_byte(adress,4)
            flag =1
    for pt in zip(*locFeu[::-1]):
                cv2.rectangle(image, pt, (pt[0]+wF,pt[1]+hF),(0,0,255),2)


    return flag

