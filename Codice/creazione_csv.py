# -*- coding: utf-8 -*-
"""
Created on Fri May 27 11:47:24 2022

@author: perry
"""

import numpy as np
import matplotlib.pyplot as plt
import skimage.io as io
import os
import csv
import math

'''
Funzione per fare verifica valori
Input:
    val - valore da controllare
'''
def check_value_x(val,img):
    if val<0:
        val=0
    elif val>img.shape[1]:
        val=img.shape[1]
    return val
    
'''
Funzione per fare verifica valori
Input:
    val - valore da controllare
'''
def check_value_y(val,img):
    if val<0:
        val=0
    elif val>img.shape[0]:
        val=img.shape[0]
    return val

'''
Funzione per la creazione di una lista
Input:
    arr - lista da cui prelevare una sottolista
    index - indice di partenza per prendere la sottolista
'''
def create_list(arr,index):
    d=[]
    for i in arr[index*7:index*7+7]:
        d.append(i)
    return d

'''
Funzione per il calcolo dei vertici (alto-sinistra, basso-destra) del box box
a partire dalla lista arr
Input:
    stringa - nome del file .gt (in realtà a noi serve .jpg, quindi dobbiamo cambiare)
    arr - lista per il calcolo dei vertici del box
'''
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


'''
Funzione per la creazione di una lista vuota
Input: None
'''
def create_empty_list(stringa):
    d=[]
    d.append(stringa)
    for i in range(5):
        d.append('')
    return d

'''
Funzione per costruire il file .csv
Prende in ingresso:
    substr - stringa per costruire il nome del file
    path - percorso dove trovre i file .gt da inserire nel file csv
    arr - lista di stringhe dove ogni stringa è il nome di un file
'''
def build_csv(substr, path, arr):
    #Salvo nella stringa s1 il percorso dei file .gt
    s1=path
    #Costruisco la stringa del nome del file .csv concatenando 3 pezzi
    file_csv='csv_'+substr+'.csv'
    #Creazione file csv: apertura file csv
    file=open(file_csv,'w',newline='')
    writer=csv.writer(file)
    
    #Ciclo for per scorrere gli elementi dell'array arr passato in ingresso
    for i in range(len(arr)):
        s2=arr[i]
        nomefile_gt=s1+'/'+s2
        nomefile_jpg=nomefile_gt
        nomefile_jpg=nomefile_jpg.replace('.gt','.jpg')
        l=[]
        
        if (os.stat(nomefile_gt).st_size == 0):
            l=create_empty_list(nomefile_jpg)
            writer.writerow(l)
        else:
            #la stringa s contiene il nome completo del file: './Datasets/MSRA-TD500/train/*.gt'
            #apriamo il file .gt con open(), in cui passiamo la stringa del nome file e la codifica
            f=open(nomefile_gt,encoding='utf-8')
            #leggiamo il file .gt con read(), in cui passiamo la stringa del nome file e la codifica
            n=f.read()

            #a questo punto n è una stringa che contiene i valori del file .gt
            #Ci interessa ottenere una lista di stringhe anzichè una stringa: eliminare gli
            #spazi della stringa con il metodo split() della classe string
            for t in n.split():
                l.append(float(t))
        
            #l è una lista di stringhe, prendiamo lunghezza(l)/7 perche' ogni box ha 7 valori
            g=int(len(l)/7)
        
            #Operazioni sulla lista, che è ora di float
            lista_di_liste=[]
            for i in range(g):
                d=create_list(l,i)
                lista_di_liste.append(d)
            
            for i in range(g):
                lista_di_liste[i]=calcola_lista(nomefile_jpg,lista_di_liste[i])
        
            #Decommentare la seguente istruzione per vedere la struttura di lista_di_liste
            #print(lista_di_liste)
        
            #Scrittura sul file .csv di lista di liste tramite il metodo writerows dell'oggetto writer
            writer.writerows(lista_di_liste)
            
            #Chiusura file .gt
            f.close()

    #chiusura file .csv
    file.close()


train_path="./Datasets/MSRA-TD500/train"
arr_gt_train = [x for x in os.listdir(train_path) if x.endswith(".gt")]
#arr_gt_train ha 300 immagini di train. Vogliamo suddividere il train in 250 immagini di train e
#50 immagini di validation
arr_gt_val=arr_gt_train[::6]    #lista di 250 immagini per training
del arr_gt_train[::6]           #lista di 50 immagini per validation

build_csv('train', train_path, arr_gt_train)

#Validazione
build_csv('val', train_path, arr_gt_val)

#Test
test_path="./Datasets/MSRA-TD500/test"
arr_gt_test = [x for x in os.listdir(test_path) if x.endswith(".gt")]
build_csv('test', test_path, arr_gt_test)












