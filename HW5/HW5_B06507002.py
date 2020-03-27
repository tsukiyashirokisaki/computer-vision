import numpy as np 
import cv2
img = cv2.imread("lena.bmp")
h,w,l=img.shape
img=img.astype(img.dtype)[:,:,1]
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

k1=np.array([
[0,1,1,1,0],
[1,1,1,1,1],
[1,1,1,1,1],
[1,1,1,1,1],
[0,1,1,1,0]])


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


d_img=dilation(img,k1)
cv2.imwrite("lena_d.bmp",d_img)
e_img=erosion(img,k1)
cv2.imwrite("lena_e.bmp",e_img)
o_img=opening(img,k1)
cv2.imwrite("lena_o.bmp",o_img)        
c_img=closing(img,k1)
cv2.imwrite("lena_c.bmp",c_img) 

