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

'''
Funzione per la creazione di una lista
Input:
    stringa - nome del file .gt (in realtà a noi serve .jpg, quindi dobbiamo cambiare)
    arr - lista da cui prelevare una sottolista
    index - indice di partenza per prendere la sottolista
'''
def create_list(stringa,arr,index):
    d=[]
    d.append(stringa)
    for j in arr[index*7:index*7+7]:
        d.append(j)
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
    nomefile_csv='csv_'+substr+'.csv'
    #Creazione file csv: apertura file csv
    file=open(nomefile_csv,'w',newline='')
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
        #Ci interessa ottenere una lista di stringhe anzichè una stringa: eliminare gli
        #spazi della stringa con il metodo split() della classe string
        l=[]
        for t in n.split():
            l.append(t)
        
        #l è una lista di stringhe, prendiamo lunghezza(l)/7 perche' ogni box ha 7 valori
        g=int(len(l)/7)
        
        #Qui va inserito il codice per effettuare le operazioni sui valori della lista
        #di stringhe l, che va prima portata a float e poi riconvertita a string
        l=[float(x) for x in l]
        
        #Operazioni sulla lista, che è ora di float
        
        
        #Dopo le operazioni riconvertiamo a string per inserire nel .csv
        l=[str(x) for x in l]
        
        #Costruiamo lista_di_boxes come lista di liste: ogni lista è una lista di stringhe
        #che contiene il nome del file seguita dai valori prelevati dal file .gt
        lista_di_boxes=[]
        for i in range(g):
            c=create_list(s,l,i)
            lista_di_boxes.append(c)
        
        #Decommentare la seguente istruzioneper vedere la struttura di lista_di_boxes
        #print(lista_di_boxes)
        
        #Scrittura sul file .csv di lista di liste tramite il metodo writerows dell'oggetto writer
        writer.writerows(lista_di_boxes)
        
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












