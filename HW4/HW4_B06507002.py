import numpy as np 
import cv2

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
            if n_img[i,j]==1:
                d_img[-(h_p//2)+i:h_p//2+1+i,-(w_p//2)+j:w_p//2+1+j]=np.logical_or(d_img[-(h_p//2)+i:h_p//2+1+i,-(w_p//2)+j:w_p//2+1+j],k)
    return d_img[h_i:h_f,w_i:w_f]

def erosion(img,k):
    h,w=img.shape
    h_p,w_p=k.shape[0]-1,k.shape[1]-1
    h_i,h_f=h_p//2,h+h_p//2
    w_i,w_f=w_p//2,w+w_p//2
    e_img=np.zeros([h+h_p,w+w_p])
    n_img=np.zeros([h+h_p,w+w_p])
    n_img[h_i:h_f,w_i:w_f]=img
    element=np.sum(k)
    for i in range(h_i,h_f):
        for j in range(w_i,w_f):
            if np.sum(n_img[-(h_p//2)+i:h_p//2+1+i,-(w_p//2)+j:w_p//2+1+j]*k)==element:
                e_img[i,j]=1
    return e_img[h_i:h_f,w_i:w_f]

def opening(img,k):
    return dilation(erosion(img,k),k)
def closing(img,k):
    return erosion(dilation(img,k),k)
def HAM(img,ki,kj):
    return (erosion(img,ki)+erosion(abs(img-1),kj))//2
img = cv2.imread("lena.bmp")
h,w,l=img.shape
img=img.astype(img.dtype)[:,:,1]
t=128
t_img=np.empty([h,w]).astype("int")
for i in range(h):
    for j in range(w):
        if img[i,j]<128:
            t_img[i,j]=0
        else:
            t_img[i,j]=1
k1=np.array([
[0,1,1,1,0],
[1,1,1,1,1],
[1,1,1,1,1],
[1,1,1,1,1],
[0,1,1,1,0]])
cv2.imwrite("lena_t.bmp",t_img*255)
d_img=dilation(t_img,k1)
cv2.imwrite("lena_d.bmp",d_img*255)        
e_img=erosion(t_img,k1)
cv2.imwrite("lena_e.bmp",e_img*255)        
o_img=opening(t_img,k1)
cv2.imwrite("lena_o.bmp",o_img*255)        
c_img=closing(t_img,k1)
cv2.imwrite("lena_c.bmp",c_img*255)        
ham=HAM(t_img,np.array([[0,0,0],
                        [1,1,0],
                        [0,1,0]]),
        np.array([[0,1,1],
                  [0,0,1],
                  [0,0,0]]))
cv2.imwrite("lena_h.bmp",ham*255)      



