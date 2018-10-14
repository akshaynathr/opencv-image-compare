import cv2
import pytesseract as pt



def read_image(img):
    #img = cv2.imread('1.png',cv2.IMREAD_COLOR)
    config = ('-l eng --oem 1 --psm 3')
    t=pt.image_to_string(img,config=config)
    return t

