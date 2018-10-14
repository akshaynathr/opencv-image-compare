
from skimage.measure import compare_ssim
import imutils
import cv2
 
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

# loop over the contours
for c in cnts:
	# compute the bounding box of the contour and then draw the
	# bounding box on both input images to represent where the two
	# images differ
	(x, y, w, h) = cv2.boundingRect(c)
	print(x,y,w,h)
	print (x + w, y + h)
	imgA= img1.copy()
	imgB= img2.copy()
	crop_imgA = imgA[y:y+h, x:x+w]
	crop_imgB = imgB[y:y+h, x:x+w]

	cv2.imshow("A",crop_imgA)

	input()
	cv2.destroyAllWindows()

	cv2.imshow("B",crop_imgB)


	input()	
	cv2.destroyAllWindows()

	cv2.rectangle(img1, (x, y), (x + w, y + h), (0, 0, 255), 2)
	cv2.imshow("AA",img1)
	f=f+1
	cv2.imwrite(str(f)+'.png',crop_imgA)
	cv2.rectangle(img2, (x, y), (x + w, y + h), (0, 0, 255), 2)
	cv2.imshow("BB",img2)

 
	print("==================")

cv2.destroyAllWindows()
#show the output images
#cv2.imshow("Original", img1)
cv2.imshow("Modified", img2)

#cv2.imshow("Diff", diff)
#cv2.imshow("Thresh", thresh)
cv2.waitKey(0)
cv2.destroyAllWindows()
