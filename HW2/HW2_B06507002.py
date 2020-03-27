import numpy as np 
import cv2
import matplotlib.pyplot as plt 
img = cv2.imread("lena.bmp")
h,w,l=img.shape
img=img.astype(img.dtype)[:,:,1]

#Part 1
x=np.arange(0,256,1)
y=np.zeros([256])
for i in range(h):
    for j in range(w):
        y[img[i,j]]+=1
plt.bar(x,y,align='center')
plt.xlabel("Gray Level")
plt.ylabel("Number of pixels")
plt.title("Lena Histogram")
plt.savefig("Lena Histogram.png",dpi=500)

#Part 2
t=128
t_img=np.empty([h,w])
for i in range(h):
    for j in range(w):
        if img[i,j]<128:
            t_img[i,j]=0
        else:
            t_img[i,j]=255
cv2.imwrite("Lena_t.bmp",t_img)    

#Part 3
def compare(nb1,nb2):
    s1=p[nb1].s
    s2=p[nb2].s
    if s1==s2:
        p[now]=P(now,s1)
        s1.AP(p[now])
    elif s1.ind<s2.ind:
        p[now]=P(now,s1)
        s1.AP(p[now])
        s1.AN(s2)
        s2.AN(s1) 
    else:
        p[now]=P(now,s2)
        s2.AP(p[now])
        s1.AN(s2)
        s2.AN(s1) 
class P():
    def __init__ (self,pos,s):
        self.pos=pos
        self.s=s
class S():
    def __init__(self,ind):
        self.comp=[]
        self.neigh=set()
        self.ind=c
    def AP(self,point):
        self.comp.append(point)
    def AN(self,n):
        self.neigh.add(n)
    

n_img=np.zeros([h+2,w+2])
n_img[1:h+1,1:w+1]=t_img

p={}
s={}
c=0
for i in range(1,h+1):
    for j in range(1,w+1):
        now=i,j
        nb1=i-1,j
        nb2=i,j-1
        if n_img[now]!=0:
            if nb1 in p :
                if nb2 in p:
                    compare(nb1,nb2)
                else:
                    s1=p[nb1].s
                    p[now]=P(now,s1)
                    s1.AP(p[now])
            elif nb2 in p:
                s2=p[nb2].s
                p[now]=P(now,s2)
                s2.AP(p[now])
            else:
                s[c]=S(c)
                p[now]=P(now,s[c])
                s[c].AP(p[now])
            c+=1

so={}
while len(s.keys())!=0:
    i=list(s.keys())[0]
    s1=s[i]
    while len(list(s1.neigh))!=0:
        
        s2=s1.neigh.pop()
        s2.neigh-={s1}
        s1.neigh=s1.neigh.union(s2.neigh)
        for poi in s2.comp:
            poi.s=s1
            s1.AP(poi)    
        while (len(list(s2.neigh)))!=0:
            n=s2.neigh.pop()
            n.neigh-={s2}
            n.neigh=n.neigh.union({s1})
            s1.neigh=s1.neigh.union({n})
        del s[s2.ind]
        del s2
        
    del s[s1.ind]
    so[i]=s1
    
def find_min_max(o_img,so,so_id):
    for i,ele in enumerate(so[so_id].comp):
        y_now,x_now=so[so_id].comp[i].pos
        if i==0:
            x_b=x_now;y_b=y_now
            y_min,x_min=y_now,x_now
            y_max,x_max=y_now,x_now
        else:
            x_b+=x_now;y_b+=y_now
            if x_now<x_min:
                x_min=x_now
            elif x_now>x_max:
                x_max=x_now
            if y_now<y_min:
                y_min=y_now
            elif y_now>y_max:
                y_max=y_now
    x_b=(x_b-(i+1))//(i+1);y_b=(y_b-(i+1))//(i+1)
    x_min-=1;y_min-=1;x_max-=1;y_max-=1
    return cv2.rectangle(o_img, (x_min, y_min), (x_max, y_max), (255, 0, 0), 2),x_b,y_b
    
nn_img=np.zeros([h,w])
o_img=np.empty([l,h,w])
for i in range(3):
    o_img[i]=t_img
o_img=o_img.transpose(1,2,0).astype(np.uint8)
for key in so.keys():
    if len(so[key].comp)>=500:
        o_img,x_b,y_b=find_min_max(o_img,so,key)
        o_img=cv2.line(o_img,(x_b-5, y_b), (x_b+5, y_b), (0, 0, 255), 1)
        o_img=cv2.line(o_img,(x_b, y_b-5), (x_b, y_b+5), (0, 0, 255), 1)
cv2.imwrite("OutImage.bmp",o_img)