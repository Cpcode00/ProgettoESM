# -*- coding: utf-8 -*-
"""
Created on Wed May 18 09:38:29 2022

@author: perry
"""

import numpy as np
import matplotlib.pyplot as plt
import skimage.io as io
import os
import csv

#funzione che costruisce una lista in cui ci sono due tipi di variabili: stringa e lista.
#Per ogni immagine di una data cartella, la lista contiene nella stringa il numero dell'immagine
#seguita da tante liste quanti sono i box di testo individuati in un'immagine
def build_lista_di_boxes(path, lista_di_boxes, arr):
    #lista_di_boxes=[]
    s1= path
    f=open('csv_train.csv','w')
    writer=csv.writer(f)
    #Ciclo for per scorrere gli elementi dell'array arr passato in ingresso
    for i in range(len(arr)):
        s2=arr[i]
        s=s1+'/'+s2
        #la stringa s contiene il nome completo del file: './Datasets/MSRA-TD500/train/*.gt'
        #apriamo il file .gt con open(), in cui passiamo la stringa del nome file e la codifica
        f=open(s,encoding='utf-8')
        #leggiamo il file .gt con read(), in cui passiamo la stringa del nome file e la codifica
        n=f.read()

        #a questo punto n è una stringa che contiene i valori del file .gt
        #Ci interessa ottenere una lista di float anzichè una stringa: eliminare gli spazi della stringa
        #con il metodo split() della classe string
        l=[]
        s=n.split()
        for t in n.split():
            l.append(float(t))
        
        #l è una lista di float, prendiamo lunghezza(l)/7 perche' ogni box ha 7 valori
        g=int(len(l)/7)
        
        #costruiamo lista_di_boxes come lista che contiene stringa del nome file seguita da
        #tante liste quanti sono i box testo
        '''
        lista_di_boxes.append(s2[4:8])
        for i in range(g):
            lista_di_boxes.append(l[i*7:i*7+7])
        '''
        row=[s2,]
        for i in range(g):
            val0,val1,val2,val3,val4,val5,val6=l[i*7:i*7+7]
            s0=str(val0)
            row.append(s0)
            s1=str(val1)
            row.append(s1)
            s2=str(val2)
            row.append(s2)
            s3=str(val3)
            row.append(s3)
            s4=str(val4)
            row.append(s4)
            s5=str(val5)
            row.append(s5)
            s6=str(val6)
            row.append(s6)
            writer.writerow(row)
    
    f.close()


#funzione che costruisce una lista in cui ci sono due tipi di variabili: stringa e lista.
#Per ogni immagine di una data cartella, la lista contiene nella stringa il numero dell'immagine
#seguita da tante liste quanti sono i box di testo individuati in un'immagine
def build_csv(path, arr):
    #lista_di_boxes=[]
    s1=path
    file=open('csv_train.csv','w')
    writer=csv.writer(file)
    #Ciclo for per scorrere gli elementi dell'array arr passato in ingresso
    for i in range(len(arr)):
        s2=arr[i]
        s=s1+'/'+s2
        #la stringa s contiene il nome completo del file: './Datasets/MSRA-TD500/train/*.gt'
        #apriamo il file .gt con open(), in cui passiamo la stringa del nome file e la codifica
        f=open(s,encoding='utf-8')
        #leggiamo il file .gt con read(), in cui passiamo la stringa del nome file e la codifica
        n=f.read()

        #a questo punto n è una stringa che contiene i valori del file .gt
        #Ci interessa ottenere una lista di float anzichè una stringa: eliminare gli spazi della stringa
        #con il metodo split() della classe string
        l=[]
        #s=n.split()
        for t in n.split():
            l.append(float(t))
        
        #l è una lista di float, prendiamo lunghezza(l)/7 perche' ogni box ha 7 valori
        g=int(len(l)/7)
        
        #costruiamo lista_di_boxes come lista che contiene stringa del nome file seguita da
        #tante liste quanti sono i box testo
        
        for i in range(g):
            row=[s2,]
            val0,val1,val2,val3,val4,val5,val6=l[i*7:i*7+7]
            s0=str(val0)
            row.append(s0)
            s1=str(val1)
            row.append(s1)
            s2=str(val2)
            row.append(s2)
            s3=str(val3)
            row.append(s3)
            s4=str(val4)
            row.append(s4)
            s5=str(val5)
            row.append(s5)
            s6=str(val6)
            row.append(s6)
            writer.writerow(row)
    
    file.close()


#Descrizione di come si ricava la lista dei nomi dei file con estensione .gt contenuti in una cartella
train_path="./Datasets/MSRA-TD500/train"
arr_gt_train = [x for x in os.listdir(train_path) if x.endswith(".gt")]
#arr_gt_train ha 300 immagini di train. Vogliamo suddividere il train in 250 immagini di train e
#50 immagini di validation
arr_gt_val=arr_gt_train[::6]    #lista di 250 immagini per training
del arr_gt_train[::6]           #lista di 50 immagini per validation

'''
lista_di_boxes_train = []
lista_di_boxes_train = build_lista_di_boxes(train_path, lista_di_boxes_train, arr_gt_train)
#lunghezza_lista_di_boxes_train=len(lista_di_boxes_train)
'''

#build_csv(train_path, arr_gt_train)

s1=train_path
file=open('csv_train.csv','w', newline='')
writer=csv.writer(file)
'''
#Ciclo for per scorrere gli elementi dell'array arr passato in ingresso
for i in range(len(arr_gt_train)):
    s2=arr_gt_train[i]
    s=s1+'/'+s2
    #la stringa s contiene il nome completo del file: './Datasets/MSRA-TD500/train/*.gt'
    #apriamo il file .gt con open(), in cui passiamo la stringa del nome file e la codifica
    f=open(s,encoding='utf-8')
    #leggiamo il file .gt con read()
    n=f.read()

    #a questo punto n è una stringa che contiene i valori del file .gt
    #Ci interessa ottenere una lista di float anzichè una stringa: eliminare gli spazi della stringa
    #con il metodo split() della classe string
    l=[]
    for t in n.split():
        l.append(float(t))
        
    #l è una lista di float, prendiamo lunghezza(l)/7 perche' ogni box ha 7 valori
    g=int(len(l)/7)
        
    #costruiamo lista_di_boxes come lista che contiene stringa del nome file seguita da
    #tante liste quanti sono i box testo
    
    
    
    for i in range(g):
        row=[s2,]
        [val0,val1,val2,val3,val4,val5,val6]=l[i*7:i*7+7]
        st0=str(val0)
        row.append(st0)
        st1=str(val1)
        row.append(st1)
        st2=str(val2)
        row.append(st2)
        st3=str(val3)
        row.append(st3)
        st4=str(val4)
        row.append(st4)
        st5=str(val5)
        row.append(st5)
        st6=str(val6)
        row.append(st6)
        writer.writerow(row)
    

file.close()
'''

    #la stringa s contiene il nome completo del file: './Datasets/MSRA-TD500/train/*.gt'
    #apriamo il file .gt con open(), in cui passiamo la stringa del nome file e la codifica
f=open('./Datasets/MSRA-TD500/train/IMG_0064.gt',encoding='utf-8')
    #leggiamo il file .gt con read()
n=f.read()

    #a questo punto n è una stringa che contiene i valori del file .gt
    #Ci interessa ottenere una lista di float anzichè una stringa: eliminare gli spazi della stringa
    #con il metodo split() della classe string
l=[]
for t in n.split():
    l.append(float(t))
        
    #l è una lista di float, prendiamo lunghezza(l)/7 perche' ogni box ha 7 valori
g=int(len(l)/7)
        
    #costruiamo lista_di_boxes come lista che contiene stringa del nome file seguita da
    #tante liste quanti sono i box testo
    
    
s2='MSRA-TD500/train/IMG_0064.gt'
for i in range(g):
    row=[s2,]
    [val0,val1,val2,val3,val4,val5,val6]=l[i*7:i*7+7]
    st0=str(val0)
    row.append(st0)
    st1=str(val1)
    row.append(st1)
    st2=str(val2)
    row.append(st2)
    st3=str(val3)
    row.append(st3)
    st4=str(val4)
    row.append(st4)
    st5=str(val5)
    row.append(st5)
    st6=str(val6)
    row.append(st6)
    writer.writerow(row)
    


'''

lista_di_boxes_val = []
lista_di_boxes_val = build_lista_di_boxes(train_path, lista_di_boxes_val,arr_gt_val)
#lunghezza_lista_di_boxes_val=len(lista_di_boxes_val)

#Facciamo la stessa cosa per il test
test_path="./Datasets/MSRA-TD500/test"
arr_gt_test = [x for x in os.listdir(test_path) if x.endswith(".gt")]
#arr_gt_test e' una lista di 200 immagini per test
lista_di_boxes_test = []
lista_di_boxes_test = build_lista_di_boxes(test_path, lista_di_boxes_test, arr_gt_test)

'''





