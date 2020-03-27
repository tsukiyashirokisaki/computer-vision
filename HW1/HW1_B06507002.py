import numpy as np 
import cv2
img = cv2.imread("lena.bmp")
h,w,c=img.shape
count=0
for i in range(h):
    for j in range(w):
        for k in range(c-1):
            if img[i][j][k]!=img[i][j][k+1]:
                count=1
                break

def upside_down(img,count):
    h,w,c=img.shape
    newimg=np.zeros([h,w,c])
    for i in range(h):
        newimg[i]=img[h-1-i]
    if count==0:
        return newimg.astype(img.dtype)[:,:,1]
    return newimg.astype(img.dtype)
cv2.imwrite('upside_down.bmp', upside_down(img,count))
def right_side_left(img,count):
    h,w,c=img.shape
    newimg=np.zeros([h,w,c])
    for i in range(h):
        for j in range(w):
            newimg[i][j]=img[i][w-1-j]
    if count==0:
        return newimg.astype(img.dtype)[:,:,1]
    return newimg.astype(img.dtype)
cv2.imwrite('right_side_left.bmp', right_side_left(img,count))

def diagonally_mirrored(img,count):
    if count==0:
        return np.transpose(img,(1,0,2))[:,:,1]
    return np.transpose(img,(1,0,2))
cv2.imwrite("diagonally_mirrored.bmp",diagonally_mirrored(img,count))


