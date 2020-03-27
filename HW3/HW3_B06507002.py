import numpy as np 
import cv2
import matplotlib.pyplot as plt 
img = cv2.imread("lena.bmp")
h,w,l=img.shape
img=img.astype(img.dtype)[:,:,1]
def plot_hist(img,name):
    x=np.arange(0,256,1)
    y=np.zeros([256])
    for i in range(h):
        for j in range(w):
            y[img[i,j]]+=1
    plt.bar(x,y,align='center')
    plt.xlim(0,256)
    plt.xlabel("Gray Level")
    plt.ylabel("Number of pixels")
    plt.title(name)
    plt.savefig(name+".png",dpi=500)
    plt.clf()
    return x,y
img_d=(img/3).astype(img.dtype)
cv2.imwrite("Lena_d.bmp",img_d)
plot_hist(img,"Lena Histogram")
x,y=plot_hist(img_d,"Dark Lena Histogram")
n=h*w
s={}
tot=0
for k in range(len(y)):
    tot+=y[k]/n*255
    s[x[k]]=tot
img_s=np.empty([h,w])
for i in range(h):
    for j in range(w):
        img_s[i,j]=s[img_d[i,j]]
img_s=img_s.astype(img.dtype)
cv2.imwrite("Lena_s.bmp",img_s)
plot_hist(img_s,"High Contrast Lena Histogram")






