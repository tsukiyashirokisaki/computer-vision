#!/usr/bin/env python
# coding: utf-8

# In[308]:


import numpy as np 
import cv2


# In[309]:


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


# In[310]:


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


# In[311]:


#import matplotlib.pyplot as plt
#plt.imshow(img,cmap="gray")
def pad(img,num):
    h,w=img.shape
    img_n=np.zeros([h+2*num,w+2*num])
    img_n[num:h+num,num:w+num]=img
    return img_n


# In[312]:


def border(l,i):
    a0=l[1,1] ; a1=l[1,2] ; a2=l[0,1] ; a3=l[1,0] ; a4=l[2,1]
    a5=l[2,2] ; a6=l[0,2] ; a7=l[0,0] ; a8=l[2,0]
    if i==4:
        neighbor=[a1,a2,a3,a4]
    elif i==8:
        neighbor=[a1,a2,a3,a4,a5,a6,a7,a8]
    if a0==0:
        return 0
    else:
        for ele in neighbor:
            if a0!=ele:
                return 1
        return 2
# 0->0 ; b-> 1 ;i->2
    
    


# In[353]:


def pair(l,i):
    a0=l[1,1] ; a1=l[1,2] ; a2=l[0,1] ; a3=l[1,0] ; a4=l[2,1]
    a5=l[2,2] ; a6=l[0,2] ; a7=l[0,0] ; a8=l[2,0]
    if i==4:
        neighbor=[a1,a2,a3,a4]
    elif i==8:
        neighbor=[a1,a2,a3,a4,a5,a6,a7,a8]
    if a0==0:
        return 0
    h=0
    for ele in neighbor:
        if ele==1 :
            h+=1
    if a0!=1 or h<1:
        return 3
    if a0==1 and h>=1:
        return 4
# q->3 ; p->4
    


# In[357]:


img = cv2.imread("lena.bmp")
h,w,l=img.shape
img=img.astype(img.dtype)[:,:,1]
img_d=np.empty([64,64])
for i in range(0,h,8):
    for j in range(0,w,8):
        img_d[i//8,j//8]=img[i,j]
img=img_d
h,w=img.shape
img=binarize(img)
cv2.imwrite("lena_threshold_downsample.bmp",img[1:h+1,1:w+1]*255)
img=pad(img,1)
ite=0
while True:
    #cv2.imwrite("lena_thinning%d.bmp"%(ite),img[1:h+1,1:w+1]*255)
    #plt.imshow(img[1:h+1,1:w+1]*255,cmap="gray")
    #plt.show()
    last_img=np.zeros([h+2,w+2])
    last_img[:,:]=img
    img_y=np.zeros([h+2,w+2])
    for i in range(1,h+1):
        for j in range(1,w+1):
            img_y[i,j]=yokoi(img[i-1:i+2,j-1:j+2])
    img_p=np.zeros([h+2,w+2])
    for i in range(1,h+1):
        for j in range(1,w+1):
            img_p[i,j]=pair(img_y[i-1:i+2,j-1:j+2],4)
    for i in range(1,h+1):
        for j in range(1,w+1):
            if yokoi(img[i-1:i+2,j-1:j+2])==1 and img_p[i,j]==4:
                img[i,j]=0
    if (img==last_img).all():
        break
    ite+=1
    
cv2.imwrite("lena_thinning.bmp",img[1:h+1,1:w+1]*255)
#plt.imshow(img[1:h+1,1:w+1]*255,cmap="gray")
#plt.show()
    
    


# In[ ]:





# In[ ]:




