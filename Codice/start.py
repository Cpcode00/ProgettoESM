# -*- coding: utf-8 -*-
"""
Created on Thu Jun  2 19:54:27 2022

@author: perry
"""

# show images inline
#%matplotlib inline
'''
# automatically reload modules when they have changed
%load_ext autoreload
%autoreload 2
'''
# import keras
from tensorflow import keras

#import
import skimage.io as io
import csv
import math

# import keras_retinanet
from keras_retinanet import models
from keras_retinanet.backend import __init__
from keras_retinanet.utils.image import read_image_bgr, preprocess_image, resize_image
from keras_retinanet.utils.visualization import draw_box, draw_caption
from keras_retinanet.utils.colors import label_color
from keras_retinanet.utils.gpu import setup_gpu

# import miscellaneous modules
import matplotlib.pyplot as plt
import cv2
import os
import numpy as np
import time

def create_list(arr,index):
    d=[]
    for i in arr[index*7:index*7+7]:
        d.append(i)
    return d

def check_value_x(val,img):
    if val<0:
        val=0
    elif val>img.shape[1]:
        val=img.shape[1]
    return val
    
def check_value_y(val,img):
    if val<0:
        val=0
    elif val>img.shape[0]:
        val=img.shape[0]
    return val


def calcola_lista(stringa,arr):
    d=[]
    d.append(stringa)
    img=np.float64(io.imread(stringa))/255
    
    #arr=[0,0,268,564,1032,104,-0.680267]
    length=arr[4]
    height=arr[5]
    phi=-arr[6]
    vertice_x=arr[2]
    vertice_y=arr[3]
    raggio=length/2
    
    centro=[(vertice_x+(length/2)),(vertice_y+(height/2))]
    spigolo_mid_destro=[centro[0]+raggio,centro[1]]
    rotazione=[raggio*math.cos(phi),raggio*math.sin(phi)]
    spigolo_mid_destro_post_rot=[centro[0]+raggio*math.cos(phi),centro[1]-raggio*math.sin(phi)]
    spigolo_mid_sinistro_post_rot=[centro[0]-raggio*math.cos(phi),centro[1]+raggio*math.sin(phi)]
    
    hyp=height/2
    cat1=hyp*math.cos(phi)
    cat2=hyp*math.sin(phi)
    
    vertice_alto_destro=[check_value_x(spigolo_mid_destro_post_rot[0]-cat2,img),check_value_y(spigolo_mid_destro_post_rot[1]-cat1,img)]
    vertice_basso_destro=[check_value_x(spigolo_mid_destro_post_rot[0]+cat2,img),check_value_y(spigolo_mid_destro_post_rot[1]+cat1,img)]
    vertice_alto_sinistro=[check_value_x(spigolo_mid_sinistro_post_rot[0]-cat2,img),check_value_y(spigolo_mid_sinistro_post_rot[1]-cat1,img)]
    vertice_basso_sinistro=[check_value_x(spigolo_mid_sinistro_post_rot[0]+cat2,img),check_value_y(spigolo_mid_sinistro_post_rot[1]+cat1,img)]

    vertice_alto_destro=[int(x) for x in vertice_alto_destro]
    vertice_basso_destro=[int(x) for x in vertice_basso_destro]
    vertice_alto_sinistro=[int(x) for x in vertice_alto_sinistro]
    vertice_basso_sinistro=[int(x) for x in vertice_basso_sinistro]
    
    #costruiamo i vettori delle x e delle y
    x=[vertice_alto_destro[0],vertice_basso_destro[0],
       vertice_alto_sinistro[0],vertice_basso_sinistro[0]]
    #print(x)
    y=[vertice_alto_destro[1],vertice_basso_destro[1],
       vertice_alto_sinistro[1],vertice_basso_sinistro[1]]
    #print(y)

    #nuove coordinate post-rotazione
    min_x=min(x)
    max_x=max(x)
    
    min_y=min(y)
    max_y=max(y)
    
    
    x1=[min_x,min_y]
    x1=[str(x) for x in x1]
    for i in x1:
        d.append(i)
    
    y1=[max_x,max_y]
    y1=[str(x) for x in y1]
    for i in y1:
        d.append(i)
    
    d.append('text')
    return d


# use this to change which GPU to use
#gpu = 1

# set the modified tf session as backend in keras
#setup_gpu(gpu)

model_path=os.path.join('.','snapshots','EfficientNetB2_csv_01.h5')
#model_path=os.path.join('.','snapshots','resnet101_csv_01.h5')
#model_path=os.path.join('.','snapshots','resnet152_csv_01.h5')

model=models.load_model(model_path,'EfficientNetB2')
#model=models.load_model(model_path,'resnet101')
#model=models.load_model(model_path,'resnet152')

model=models.convert_model(model)

#print(model.summary())

labels_to_names = {0: 'text'}

image = read_image_bgr('./Datasets/MSRA-TD500/train/IMG_0752.JPG')

nomefile_jpg='./Datasets/MSRA-TD500/train/IMG_0752.JPG'
nomefile_gt='./Datasets/MSRA-TD500/train/IMG_0752.gt'
f=open(nomefile_gt,encoding='utf-8')
n=f.read()
l=[]
for t in n.split():
    l.append(float(t))
    
g=int(len(l)/7)
lista_di_liste=[]
for i in range(g):
    d=create_list(l,i)
    lista_di_liste.append(d)
            
for i in range(g):
    lista_di_liste[i]=calcola_lista(nomefile_jpg,lista_di_liste[i])
    
true_box_1=[lista_di_liste[0][1],lista_di_liste[0][2],lista_di_liste[0][3],lista_di_liste[0][4]]
true_box_1=[int(x) for x in true_box_1]
'''
true_box_2=[lista_di_liste[1][1],lista_di_liste[1][2],lista_di_liste[1][3],lista_di_liste[1][4]]
true_box_2=[int(x) for x in true_box_2]

true_box_3=[lista_di_liste[2][1],lista_di_liste[2][2],lista_di_liste[2][3],lista_di_liste[2][4]]
true_box_3=[int(x) for x in true_box_3]

true_box_4=[lista_di_liste[3][1],lista_di_liste[3][2],lista_di_liste[3][3],lista_di_liste[3][4]]

true_box_5=[lista_di_liste[4][1],lista_di_liste[4][2],lista_di_liste[4][3],lista_di_liste[4][4]]

true_box_6=[lista_di_liste[5][1],lista_di_liste[5][2],lista_di_liste[5][3],lista_di_liste[5][4]]

true_box_7=[lista_di_liste[6][1],lista_di_liste[6][2],lista_di_liste[6][3],lista_di_liste[6][4]]

true_box_8=[lista_di_liste[7][1],lista_di_liste[7][2],lista_di_liste[7][3],lista_di_liste[7][4]]

true_box_9=[lista_di_liste[8][1],lista_di_liste[8][2],lista_di_liste[8][3],lista_di_liste[8][4]]
true_box_10=[lista_di_liste[9][1],lista_di_liste[9][2],lista_di_liste[9][3],lista_di_liste[9][4]]
'''
# copy to draw on
draw = image.copy()
draw = cv2.cvtColor(draw, cv2.COLOR_BGR2RGB)

# preprocess image for network
image = preprocess_image(image)
image, scale = resize_image(image)

# process image
start = time.time()
boxes, scores, labels = model.predict_on_batch(np.expand_dims(image, axis=0))
print("processing time: ", time.time() - start)

# correct for image scale
boxes /= scale

draw_box(draw, true_box_1, color=(255,0,0))
'''
draw_box(draw, true_box_2, color=(255,0,0))

draw_box(draw, true_box_3, color=(255,0,0))

draw_box(draw, true_box_4, color=(255,0,0))

draw_box(draw, true_box_5, color=(255,0,0))

draw_box(draw, true_box_6, color=(255,0,0))

draw_box(draw, true_box_7, color=(255,0,0))

draw_box(draw, true_box_8, color=(255,0,0))

draw_box(draw, true_box_9, color=(255,0,0))
draw_box(draw, true_box_10, color=(255,0,0))
'''

# visualize detections
for box, score, label in zip(boxes[0], scores[0], labels[0]):
    # scores are sorted so we can break
    
    if score < 0.3:
        break
        
    color = label_color(label)
    
    b = box.astype(int)
    #print(b)
    draw_box(draw, b, color=color)
    
    caption = "{} {:.3f}".format(labels_to_names[label], score)
    draw_caption(draw, b, caption)
    
plt.figure(figsize=(15, 15))
plt.axis('off')
plt.imshow(draw)
plt.show()


'''
def calcolo(v1,v2):
    mid1=(v2[0]-v1[0])**2
    mid2=(v2[1]-v1[0])**2
    return math.sqrt(mid1+mid2)

def check_distance(b1, b2):
    box1_x=[b1[0],b1[2]]
    box1_y=[b1[1],b1[3]]
    alto1_sx=[box1_x[0],box1_y[0]]
    alto1_dx=[box1_x[1],box1_y[0]]
    basso1_sx=[box1_x[0],box1_y[1]]
    basso1_dx=[box1_x[1],box1_y[1]]
    
    box2_x=[b2[0],b2[2]]
    box2_y=[b2[1],b2[3]]
    alto2_sx=[box2_x[0],box2_y[0]]
    alto2_dx=[box2_x[1],box2_y[0]]
    basso2_sx=[box2_x[0],box2_y[1]]
    basso2_dx=[box2_x[1],box2_y[1]]
    
    calc1=calcolo(alto1_sx,alto2_sx)
    calc2=calcolo(alto1_dx,alto2_dx)
    calc3=calcolo(basso1_sx,basso2_sx)
    calc4=calcolo(basso1_dx,basso2_dx)
    
    return calc1+calc2+calc3+calc4

# visualize detections
vettore_box=[]
vettore_dist_1=[]
vettore_dist_2=[]
vettore_dist_3=[]
vettore_score=[]

for box, score, label in zip(boxes[0], scores[0], labels[0]):
    # scores are sorted so we can break  
    
    if score < 0.3:
        break
        
    color = label_color(label)
    
    b = box.astype(int)
    vettore_box.append(b)
    print(b)
    
    print(check_distance(b, true_box_1))
    if (check_distance(b, true_box_1)<1000):
        draw_box(draw, b, color=color)
    
        caption = "{} {:.3f}".format(labels_to_names[label], score)
        draw_caption(draw, b, caption)
    vettore_dist_1.append(check_distance(b, true_box_1))
    
    print(check_distance(b, true_box_2))
    if (check_distance(b, true_box_2)<1000):
        draw_box(draw, b, color=color)
    
        caption = "{} {:.3f}".format(labels_to_names[label], score)
        draw_caption(draw, b, caption)
    vettore_dist_2.append(check_distance(b, true_box_2))
    
    print(check_distance(b, true_box_3))
    if (check_distance(b, true_box_3)<1000):
        draw_box(draw, b, color=color)
    
        caption = "{} {:.3f}".format(labels_to_names[label], score)
        draw_caption(draw, b, caption)
    vettore_dist_3.append(check_distance(b, true_box_2))
    vettore_score.append(score)
    
min_vettore_dist_1=min(vettore_dist_1)
min_vettore_dist_2=min(vettore_dist_2)
min_vettore_dist_3=min(vettore_dist_3)
min_vettore_score=min(vettore_score) 

plt.figure(figsize=(15, 15))
plt.axis('off')
plt.imshow(draw)
plt.show()

'''


