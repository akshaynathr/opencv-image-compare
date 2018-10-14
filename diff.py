
from skimage.measure import compare_ssim
import imutils
import cv2
from text_recognizer import img_read
from text_recognizer import clean_latin
from text_recognizer import unicodetoascii
file1='img6.png'

file2='img7.png'

img1 = cv2.imread(file1)
img2 = cv2.imread(file2)

g1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
g2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)


(score,diff) = compare_ssim(g1,g2,full=True)

print("Similarity score :{}".format(score))

diff= (diff *255).astype("uint8")

thresh = cv2.threshold(diff,0,255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]

f=0
textA=[]
textB=[]
text_result=[]
# loop over the contours
for c in cnts:
	# compute the bounding box of the contour and then draw the
	# bounding box on both input images to represent where the two
	# images differ
	(x, y, w, h) = cv2.boundingRect(c)
	#print(x,y,w,h)
	#print (x + w, y + h)
	imgA= img1.copy()
	imgB= img2.copy()
	crop_imgA = imgA[y:y+h+10, x:x+w+10]
	crop_imgB = imgB[y:y+h+10, x:x+w+10]

	#cv2.imshow("A",crop_imgA)

	cv2.destroyAllWindows()

	#cv2.imshow("B",crop_imgB)


	cv2.destroyAllWindows()

	cv2.rectangle(img1, (x, y), (x + w, y + h), (0, 0, 255), 2)
	#cv2.imshow("AA",img1)
	f=f+1
        #print(f)
	#cv2.imwrite('A'+str(f)+'.png',crop_imgA)
	#cv2.imwrite('B'+str(f)+'.png',crop_imgB)
	cv2.rectangle(img2, (x, y), (x + w, y + h), (0, 0, 255), 2)
	#cv2.imshow("BB",img2)
        t1=img_read.read_image(crop_imgA)
        t2=img_read.read_image(crop_imgB)
        t1= t1.strip("'")
        t2= t2.strip("'")

        if(t1.strip(' ') != ''):
            textA.append(unicodetoascii.unicodetoascii(clean_latin.clean_latin1(t1)))

        if(t2.strip(' ') != ''):
            textB.append(unicodetoascii.unicodetoascii(clean_latin.clean_latin1(t2)))


        if t1.strip(' ')== '' and t2.strip(' ')=='':
            continue
        if t1.strip(' ') == '' and t2.strip(' ')!='':
            #print("Element "+ t2 +" has been moved in position")
            text_result.append("Element "+ t2 +" has been moved in position")
            continue
        if t2.strip(' ') == '' and t1.strip(' ')!='':
            #print("Element "+ t1 +" has been moved in position")
            text_result.append("Element "+ t1 +" has been moved in position")
            continue


        text_result.append("Element "+t2+" moved  to position of "+t1)



#print(textA)
#print(textB)
# check the items missing in the screenshots
if score !=1:
    print("Change detected\n")
    print("Predicting the changes (Note : result may not be fully accurate.Please check the image diff to confirm the changes)\n")
    for j in textA:
        if j not in textB:
            text_result.append('Element '+ j +' is removed')

    for k in textB:
        if k not in textA:
            text_result.append('Element '+ k + ' is added')

    for i in set(text_result):
        print(i)

"""
    for i in textA:
        if i not in textB:
            print("Element " +i + " renamed/removed")
        else:
            print("Element " +i + " position changed")

    for j in textB:
        if j not in textA:
            print("Element "+j + " is newly added")
"""
cv2.destroyAllWindows()
#show the output images
#cv2.imshow("Original", img1)
cv2.imshow("Modified", img2)

#cv2.imshow("Diff", diff)
#cv2.imshow("Thresh", thresh)

cv2.waitKey(0)
cv2.destroyAllWindows()
