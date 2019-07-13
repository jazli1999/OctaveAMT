"""module for poly pitch detection"""

__author__ = 'Baoyu Tang @ BUPT'

from src.amt.amt_symbol import Note, InstrSeq, Score
import cv2
import math
import matplotlib.pyplot as plt
import numpy as np
from skimage import transform
from keras.models import load_model


def pitch_detect(score):
    print('Pitch detecting...')
    cnn_process(score)


def cnn_process(sc):
    pm = "./cnn/CNN.model"  # temp
    ps = "./cut/"
    classes = ['48', '53', '55', '57', '59', '60', '62', '64', '65', '72', '74', '76', '77', '79', '81']  # temp
    best_threshold = [0.1 for i in range(15)]  # temp
    model = load_model(pm)

    for i1,instr_seq in enumerate(sc.instr_seqs):
        img = cv2.imread(instr_seq.spec_path, 1)
        # print(instr_seq.spec_path)
        # plt.imshow(img)
        valueto = math.ceil((instr_seq.notes[0].onset - 1) * sc.tempo)
        # print(valueto)

        for i2,note in enumerate(instr_seq.notes):
            onset = valueto
            valueto = math.ceil(onset + math.ceil(note.value * sc.tempo))
            # print(onset,valueto)
            imgtest = img[:, onset:valueto]
            filename=("%d"+"."+"%d")%(i1,i2)+".jpg"
            cv2.imwrite(ps+filename,imgtest)
            # plt.imshow(imgtest)
            imgtest = transform.resize(imgtest, (100, 100))
            imgtest = imgtest.transpose((2, 0, 1))
            imgtest = np.expand_dims(imgtest, axis=0)
            proba = model.predict(imgtest)
            y_pred = np.array([1 if proba[0, i] >= best_threshold[i] else 0 for i in range(15)])
            # show the probabilities for each of the individual labels
            result_tuple = []
            # print(y_pred)
            for i in range(15):
                if y_pred[i] == 1:
                    result_tuple.append(classes[i])
            print(result_tuple)
            note.pitch = result_tuple

    return sc
