#!/usr/bin/env python
# coding: utf-8

# In[19]:


import numpy as np 
import cv2
from numpy.random import seed
from numpy.random import rand
from numpy.random import randn # gaussian
import matplotlib.pyplot as plt
def plot(img):
    plt.imshow(img,cmap="gray")
    plt.show()
def Convolution1(img,K):
    a,b=K.shape
    s=a//2
    h,w=img.shape
    img_p=pad(img,s)
    img_o=np.empty([h,w])
    for i in range(s,s+h):
        for j in range(s,s+w):
            img_o[i-s,j-s]=np.sum(img_p[i-s:i+s+1,j-s:j+s+1]*K)
    return img_o.astype(np.uint8)
            
    
k1=np.array([
[0,1,1,1,0],
[1,1,1,1,1],
[1,1,1,1,1],
[1,1,1,1,1],
[0,1,1,1,0]])
img = cv2.imread("lena.bmp")
h,w,l=img.shape
img=img.astype(img.dtype)[:,:,1]


# In[20]:


#import matplotlib.pyplot as plt
#plt.imshow(img,cmap="gray")
def pad(img,num):
    h,w=img.shape
    img_n=np.zeros([h+2*num,w+2*num])
    img_n[num:h+num,num:w+num]=img
    return img_n


# In[21]:


def dilation(img,k):
    h,w=img.shape
    h_p,w_p=k.shape[0]-1,k.shape[1]-1
    h_i,h_f=h_p//2,h+h_p//2
    w_i,w_f=w_p//2,w+w_p//2
    d_img=np.zeros([h+h_p,w+w_p])
    n_img=np.zeros([h+h_p,w+w_p])
    n_img[h_i:h_f,w_i:w_f]=img
    for i in range(h_i,h_f):
        for j in range(w_i,w_f):
            d_img[i,j]=np.max(n_img[-(h_p//2)+i:h_p//2+1+i,-(w_p//2)+j:w_p//2+1+j]*k)
    return d_img[h_i:h_f,w_i:w_f]
def erosion(img,k):
    h,w=img.shape
    h_p,w_p=k.shape[0]-1,k.shape[1]-1
    h_i,h_f=h_p//2,h+h_p//2
    w_i,w_f=w_p//2,w+w_p//2
    e_img=np.zeros([h+h_p,w+w_p])
    n_img=np.zeros([h+h_p,w+w_p])
    n_img[h_i:h_f,w_i:w_f]=img
    for i in range(h_i,h_f):
        for j in range(w_i,w_f):
            e_img[i,j]=np.min((np.delete(n_img[-(h_p//2)+i:h_p//2+1+i,-(w_p//2)+j:w_p//2+1+j]*k,[0,4,20,24])))
    return e_img[h_i:h_f,w_i:w_f]
def opening(img,k):
    return dilation(erosion(img,k),k)
def closing(img,k):
    return erosion(dilation(img,k),k)


# In[22]:


def Gaussian(img,A):
    seed(1)
    h,w=img.shape
    return img+randn(h,w)*A
def SAP(img,t):
    h,w=img.shape
    seed(1)
    noise=rand(h,w)
    n_img=np.copy(img)
    n_img[noise>1-t]=255
    n_img[noise<t]=0
    return n_img


# In[23]:


Gaussian_10=Gaussian(img,10)
Gaussian_30=Gaussian(img,30)
cv2.imwrite("Gaussian_10.bmp",Gaussian_10)
cv2.imwrite("Gaussian_30.bmp",Gaussian_30)
SAT_005=SAP(img,0.05)
SAT_010=SAP(img,0.1)
cv2.imwrite("SAT_005.bmp",SAT_005)
cv2.imwrite("SAT_010.bmp",SAT_010)
noise_img=[Gaussian_10,Gaussian_30,SAT_005,SAT_010]


# In[86]:





# In[24]:


def Box(k): #k*k
    return np.ones([k,k])/k**2


# In[25]:


box_3=Box(3)
box_5=Box(5)
box_list=[]
box_name=["box_3","box_5"]
for i,kernel in enumerate([box_3,box_5]):
    box_app=[]
    for j,img_n in enumerate(noise_img):
        img_o=Convolution1(img_n,kernel)
        cv2.imwrite("%s_%s.bmp"%(box_name[i],j),img_o)
        box_app.append(img_o)
    box_list.append(box_app)


# In[26]:


def median(img,k):
    s=k//2
    img_p=pad(img,s)
    img_o=np.empty([h,w])
    for i in range(s,s+h):
        for j in range(s,s+w):
            img_o[i-s,j-s]=np.median(img_p[i-s:i+s+1,j-s:j+s+1])
    return img_o.astype(np.uint8)


# In[27]:


median_list=[]
median_name=["median_3","median_5"]
for i,ele in enumerate([3,5]):
    median_app=[]
    for j,img_n in enumerate(noise_img):
        img_o=median(img_n,ele)
        cv2.imwrite("%s_%s.bmp"%(median_name[i],j),img_o)
        median_app.append(img_o)
    median_list.append(median_app)


# In[59]:


morph_list=[]
morph_name=["o_c","c_o"]
for i in range(2):
    morph_app=[]
    for j,img_n in enumerate(noise_img):
        if i==0:
            img_o=closing(opening(img_n,k1),k1)
        else:
            img_o=opening(closing(img_n,k1),k1)
        cv2.imwrite("%s_%s.bmp"%(morph_name[i],j),img_o)
        morph_app.append(img_o)
    morph_list.append(morph_app)


# In[29]:


def SNR(img,img_n):
    img=img/255.0
    img_n=img_n/255.0
    mu=np.mean(img)
    VS=np.var(img)
    mu_N=np.mean(img_n-img)
    VN=np.var(img_n-img)
    snr=20*np.log10(np.sqrt(VS)/np.sqrt(VN))
    return snr
    
    
    

# In[77]:


imgs=[noise_img]+box_list+median_list+morph_list


# In[78]:


data=np.empty([7,4])
for i,img_o in enumerate(imgs):
    for j,img_n in enumerate(img_o):
        data[i,j]=SNR(img,img_n)
     


# In[72]:


import pandas as pd
pd.DataFrame(data).to_excel("SNR.xlsx")

for i in range(4):
    I1=np.concatenate([cv2.imread("box_3_%s.bmp"%(i)),cv2.imread("box_5_%s.bmp"%(i)),     
                                                             cv2.imread("median_3_%s.bmp"%(i))],axis=1)
    I2=np.concatenate([cv2.imread("median_5_%s.bmp"%(i)),cv2.imread("o_c_%s.bmp"%(i)),     
                                                             cv2.imread("c_o_%s.bmp"%(i))],axis=1)
    cv2.imwrite("%s.bmp"%(i),np.concatenate([I1,I2],axis=0))
    

