
import numpy as np 
import cv2
def pad(img,num):
    h,w=img.shape
    img_n=np.zeros([h+2*num,w+2*num])
    img_n[num:h+num,num:w+num]=img
    return img_n
def Convolution(img,K):
    a=K.shape[0]
    s=a//2
    h,w=img.shape
    img_p=pad(img,s)
    img_o=np.empty([h,w])
    if a%2:
        for i in range(s,s+h):
            for j in range(s,s+w):
                img_o[i-s,j-s]=np.sum(img_p[i-s:i+s+1,j-s:j+s+1]*K)
        return img_o
    else:
        for i in range(s,s+h):
            for j in range(s,s+w):
                img_o[i-s,j-s]=np.sum(img_p[i:i+a,j:j+a]*K)
        return img_o
img = cv2.imread("lena.bmp")
h,w,l=img.shape
img=img.astype(img.dtype)[:,:,1]
def process(img,kernels,t):
    for i,k in enumerate(kernels):
        if i==0:
            out=np.power(Convolution(img,k),2)
        else:
            out+=np.power(Convolution(img,k),2)
    out=np.sqrt(out)
    out=255*((~(out>t)).astype("int"))
    return out

Rob=np.array([[[-1,0],[0,1]],[[0,-1],[1,0]]])
img_R=process(img,Rob,12)  
cv2.imwrite("Robert.bmp",img_R)
Pre=np.array([[[-1,-1,-1],[0,0,0],[1,1,1]],[[-1,0,1],[-1,0,1],[-1,0,1]]])
img_P=process(img,Pre,24)
cv2.imwrite("Prewitt.bmp",img_P)
Sob=np.array([[[-1,-2,-1],[0,0,0],[1,2,1]],[[-1,0,1],[-2,0,2],[-1,0,1]]])
img_S=process(img,Sob,38)  
cv2.imwrite("Sobel.bmp",img_S)
FaC=np.array([[[-1,-np.sqrt(2),-1],[0,0,0],[1,np.sqrt(2),1]],[[-1,0,1],[-np.sqrt(2),0,np.sqrt(2)],[-1,0,1]]])
img_F=process(img,FaC,30)  
cv2.imwrite("FaC.bmp",img_F)

def conpass(img,kernels,t):
    for i,k in enumerate(kernels):
        if i==0:
            out=Convolution(img,k)
        else:
            out=np.max([out,Convolution(img,k)],axis=0)
    out=255*((~(out>t)).astype("int"))
    return out
Kir=np.array([[[-3,-3,5],[-3,0,5],[-3,-3,5]],
                [[-3,5,5],[-3,0,5],[-3,-3,-3]],
                [[5,5,5],[-3,0,-3],[-3,-3,-3]],
                [[5,5,-3],[5,0,-3],[-3,-3,-3]],
                [[5,-3,-3],[5,0,-3],[5,-3,-3]],
                [[-3,-3,-3],[5,0,-3],[5,5,-3]],
                [[-3,-3,-3],[-3,0,-3],[5,5,5]],
                [[-3,-3,-3],[-3,0,5],[-3,5,5]]])
img_K=conpass(img,Kir,150)
cv2.imwrite("Kirsch.bmp",img_K)
Robin=np.array([[[-1,0,1],[-2,0,2],[-1,0,1]],
                [[0,1,2],[-1,0,1],[-2,-1,0]],
                [[1,2,1],[0,0,0],[-1,-2,-1]],
                [[2,1,0],[1,0,-1],[0,-1,-2]],
                [[1,0,-1],[2,0,-2],[1,0,-1]],
                [[0,-1,-2],[1,0,-1],[2,1,0]],
                [[-1,-2,-1],[0,0,0],[1,2,1]],
                [[-2,-1,0],[-1,0,1],[0,1,2]],
               ])
img_Ro=conpass(img,Robin,50)
cv2.imwrite("Robinson.bmp",img_Ro)
NaB=100*np.array([np.array([np.ones(5),np.ones(5),np.zeros(5),-np.ones(5),-np.ones(5)]),
              np.array([[-1,-1,0,1,1],[-1,-1,0,1,1],[-1,-1,0,1,1],[-1,-1,0,1,1],[-1,-1,0,1,1]]),
              np.array([[1,1,1,.32,-1],[1,1,.92,-.78,-1],[1,1,0,-1,-1],[1,.78,-.92,-1,-1],[1,-.32,-1,-1,-1]]),
              np.array([np.ones(5),[1,1,1,.78,-.32],[1,.92,0,-.92,-1],[.32,-.78,-1,-1,-1],-np.ones(5)]),
              np.array([[-1,.32,1,1,1],[-1,-.78,.92,1,1],[-1,-1,0,1,1],[-1,-1,-.92,.78,1],[-1,-1,-1,-.32,1]]),
              np.array([np.ones(5),[-.32,.78,1,1,1],[-1,-.92,0,.92,1],[-1,-1,-1,-.78,.32],-np.ones(5)])
              
               ])
img_NaB=conpass(img,NaB,11000)
cv2.imwrite("NaB.bmp",img_NaB)

for i,ele in enumerate(["Robert","Prewitt","Sobel","FaC","Kirsch","Robinson","NaB"]):
    if i%4==0:
        out=cv2.imread(ele+".bmp")
    else:
        out=np.concatenate([out,cv2.imread(ele+".bmp")],axis=1)
    if i==3 or i==6:
        cv2.imwrite("%d.bmp"%(i//3),out)
    
        
    
