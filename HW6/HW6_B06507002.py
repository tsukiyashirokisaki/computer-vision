
import numpy as np 
import cv2
img = cv2.imread("lena.bmp")
h,w,l=img.shape
img=img.astype(img.dtype)[:,:,1]
def binarize(img):
    t=128
    t_img=np.empty([h,w]).astype("int")
    for i in range(h):
        for j in range(w):
            if img[i,j]<128:
                t_img[i,j]=0
            else:
                t_img[i,j]=1
    return t_img
img=binarize(img)
def pad(img,num):
    h,w=img.shape
    img_n=np.zeros([h+2*num,w+2*num])
    img_n[num:h+num,num:w+num]=img
    return img_n

def H(b,c,d,e):
    if b==c and b==1 and (d!=b or e!=b):
        return "q"
    if b==c and b==1 and (d==b and e==b ):
        return "r"
    else:
        return "s"



def yokoi(l):
    x=[np.s_[1,1],np.s_[1,2],np.s_[0,1],np.s_[1,0],np.s_[2,1],np.s_[2,2],np.s_[0,2],np.s_[0,0],np.s_[2,0]]
    a1=H(l[x[0]],l[x[1]],l[x[6]],l[x[2]])
    a2=H(l[x[0]],l[x[2]],l[x[7]],l[x[3]])
    a3=H(l[x[0]],l[x[3]],l[x[8]],l[x[4]])
    a4=H(l[x[0]],l[x[4]],l[x[5]],l[x[1]])
    a=[a1,a2,a3,a4]
    r=0 ; q=0
    for i in range(4):
        if a[i]=="r":
            r+=1
        if a[i]=="q":
            q+=1
    if r==4:
        return 5
    else:
        return q


img_d=np.empty([64,64])
for i in range(0,h,8):
    for j in range(0,w,8):
        img_d[i//8,j//8]=img[i,j]


img_pad=pad(img_d,1)
img_y=np.zeros([64,64],dtype="int")
for i in range(64):
    for j in range(64):
        img_y[i,j]=yokoi(img_pad[i:i+3,j:j+3])
img_y=img_y.astype("str")

img_y[img_y=="0"]=" "
np.savetxt('yokoi.txt', img_y, delimiter='',fmt='%s')


