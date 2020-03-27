#!/usr/bin/env python
# coding: utf-8

# In[108]:



import numpy as np 
import cv2
import matplotlib.pyplot as plt
def plot(img):
    plt.imshow(img,cmap="gray")
    plt.show()
def pad(img,num):
    h,w=img.shape
    img_n=np.zeros([h+2*num,w+2*num])
    img_n[num:h+num,num:w+num]=img
    return img_n
def Convolution(img,K,t):
    a=K.shape[0]
    s=a//2
    h,w=img.shape
    img_p=pad(img,s)
    img_o=np.empty([h,w])
    for i in range(s,s+h):
        for j in range(s,s+w):
            cal=np.sum(img_p[i-s:i+s+1,j-s:j+s+1]*K)
            if cal>=t:
                img_o[i-s,j-s]=1
            elif cal<=-t:
                img_o[i-s,j-s]=-1
            else:
                img_o[i-s,j-s]=0                
    return img_o,s,h,w
def detection(img_o,s,h,w):
    img_o=pad(img_o,s)
    img_f=np.ones([h,w])*255
    for i in range(s,s+h):
        for j in range(s,s+w):
             if -1 in np.ones([2*s+1,2*s+1])*img_o[i,j]*img_o[i-s:i+s+1,j-s:j+s+1] and img_o[i,j]>=1:
                    img_f[i-s,j-s]=0
    return img_f
            
                    
def zero(img,k,t):
    
    out=255*(~(out>t).astype("int"))
    return out                
img = cv2.imread("lena.bmp")
h,w,l=img.shape
img=img.astype(img.dtype)[:,:,1]


# In[111]:


Lap=[np.array([[0,1,0],[1,-4,1],[0,1,0]]),
     1./3.*np.array([[1,1,1],[1,-8,1],[1,1,1]]),
     1./3.*np.array([[2,-1,2],[-1,-4,-1],[2,-1,2]])
    ]
t=15
img_o,s,h,w=Convolution(img,Lap[0],t)
img_f=detection(img_o,s,h,w)
cv2.imwrite("Lap1.bmp",img_f)
t=15
img_o,s,h,w=Convolution(img,Lap[1],t)
img_f=detection(img_o,s,h,w)
cv2.imwrite("Lap2.bmp",img_f)


t=20
img_o,s,h,w=Convolution(img,Lap[2],t)
img_f=detection(img_o,s,h,w)
cv2.imwrite("Lap_min.bmp",img_f)


# In[104]:


LoG = np.array([
		[0, 0, 0, -1, -1, -2, -1, -1, 0, 0, 0],
		[0, 0, -2, -4, -8, -9, -8, -4, -2, 0, 0],
		[0, -2, -7, -15, -22, -23, -22, -15, -7, -2, 0],
		[-1, -4, -15, -24, -14, -1, -14, -24, -15, -4, -1],
		[-1, -8, -22, -14, 52, 103, 52, -14, -22, -8, -1],
		[-2, -9, -23, -1, 103, 178, 103, -1, -23, -9, -2],
		[-1, -8, -22, -14, 52, 103, 52, -14, -22, -8, -1],
		[-1, -4, -15, -24, -14, -1, -14, -24, -15, -4, -1],
		[0, -2, -7, -15, -22, -23, -22, -15, -7, -2, 0],
		[0, 0, -2, -4, -8, -9, -8, -4, -2, 0, 0],
		[0, 0, 0, -1, -1, -2, -1, -1, 0, 0, 0]
	])


# In[115]:


t=3000
img_o,s,h,w=Convolution(img,LoG,t)
img_f=detection(img_o,s,h,w)
cv2.imwrite("LoG.bmp",img_f)


# In[118]:


DoG = np.array([
		[-1, -3, -4, -6, -7, -8, -7, -6, -4, -3, -1],
		[-3, -5, -8, -11, -13, -13, -13, -11, -8, -5, -3],
		[-4, -8, -12, -16, -17, -17, -17, -16, -12, -8, -4],
		[-6, -11, -16, -16, 0, 15, 0, -16, -16, -11, -6],
		[-7, -13, -17, 0, 85, 160, 85, 0, -17, -13, -7],
		[-8, -13, -17, 15, 160, 283, 160, 15, -17, -13, -8],
		[-7, -13, -17, 0, 85, 160, 85, 0, -17, -13, -7],
		[-6, -11, -16, -16, 0, 15, 0, -16, -16, -11, -6],
		[-4, -8, -12, -16, -17, -17, -17, -16, -12, -8, -4],
		[-3, -5, -8, -11, -13, -13, -13, -11, -8, -5, -3],
		[-1, -3, -4, -6, -7, -8, -7, -6, -4, -3, -1]
	])


t=1
img_o,s,h,w=Convolution(img,DoG,t)
img_f=detection(img_o,s,h,w)
cv2.imwrite("DoG.bmp",img_f)
