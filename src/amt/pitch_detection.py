"""module for poly pitch detection"""

__author__ = 'Baoyu Tang @ BUPT'

from src.amt.amt_symbol import Note, InstrSeq, Score
import cv2
import matplotlib.pyplot as plt
import numpy as np
from skimage import io,transform
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D
from keras.optimizers import SGD
from keras.callbacks import ModelCheckpoint
from sklearn.metrics import matthews_corrcoef
from sklearn.metrics import hamming_loss
from keras import backend as K
K.set_image_dim_ordering('th')
from keras.preprocessing.image import img_to_array
from keras.models import load_model
import math
import pickle
import skimage
import os
from amt_symbol import Note, InstrSeq, Score


def pitch_detect(sc):
    
    pm="./CNN.model"###temp
    pl="./mlb.pickle"####temp
    classes = ['60','62','64','65','67','69']####temp
    best_threshold=[0.1,0.1,0.1,0.1,0.1,0.1]####temp

    model = load_model(pm)
   
    for instr_seq in sc.instr_seqs:
        
        img=cv2.imread(instr_seq.spec_path,1)
        print(instr_seq.spec_path)
        #plt.imshow(img) 
        valueto=math.ceil((instr_seq.notes[0].onset-1)*sc.tempo)
        print(valueto)
        for note in instr_seq.notes:
            
            label=[]
            onset=valueto
            valueto=math.ceil(onset+math.ceil(note.value*sc.tempo))
            #print(onset,valueto)
            imgtest = img[:,onset:valueto]
            plt.imshow(imgtest) 
            imgtest=transform.resize(imgtest,(100,100))
            imgtest = imgtest.transpose((2,0,1))
            imgtest = np.expand_dims(imgtest,axis=0)
            proba = model.predict(imgtest)
            y_pred = np.array([1 if proba[0,i]>=best_threshold[i] else 0 for i in range(6)])
# show the probabilities for each of the individual labels
            result_tuple=[]
            #print(y_pred)
            for i in range(6):
                if y_pred[i]==1:
                        result_tuple.append(classes[i])
            print(result_tuple)
            note.pitch=result_tuple
    return sc
