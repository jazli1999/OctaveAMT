"""Separate the mixed audio source to individual instrument"""

from src.amt.amt_symbol import Note, InstrSeq, Score
from sklearn.decomposition import NMF
from librosa.core import cqt, icqt
from scipy.io.wavfile import write

import matplotlib.pyplot as plt
import numpy as np
import librosa.display
import librosa.util


def src_separate(cur_score):
    nmf_src_separate(cur_score)


def nmf_src_separate(cur_score):
    y, sr, c, phase = load_audio(cur_score.audio_path)
    w, h, re_error = default_nmf_model(c, cur_score.instr_num)
    n_spec, n_wav = reconstruct(w, h, cur_score.instr_num, sr, phase)
    cur_score = instr_seqs_generate(cur_score, n_spec, n_wav, sr)

    return cur_score


def load_audio(path):
    y, sr = librosa.load(path)
    complex_c = cqt(y, sr=sr, hop_length=64, n_bins=84, bins_per_octave=12)
    c, phase = librosa.magphase(complex_c)

    return y, sr, c, phase


def default_nmf_model(c, n_components):
    nmf_model = NMF(n_components=n_components, init='random', max_iter=2000, alpha=0, l1_ratio=0.0)
    w = nmf_model.fit_transform(c)
    h = nmf_model.components_
    
    return w, h, nmf_model.reconstruction_err_


def reconstruct(w, h, n_components, sr, phase):
    # n_s for all specs
    # n_c for all synthesis audios
    n_spec = []
    n_wav = []
    for i in range(0, n_components):
        w = w[:, i:i + 1]
        h = h[i:i + 1, :]
        s = np.multiply(w, h)
        c = s * phase
        wav = icqt(c, sr=sr, hop_length=64)

        n_spec.append(s)
        n_wav.append(wav)

    return n_spec, n_wav


def instr_seqs_generate(cur_score, n_spec, n_wav, sr):
    instr_seqs = []
    path_prefix = cur_score.audio_path.split('.')[0] + '_'

    for spec, wav, index in zip(n_spec, n_wav, range(0, cur_score.instr_num)):
        instr_seq = InstrSeq()
        instr_seq.cqt_matrix = spec

        instr_seq.spec_path = path_prefix + str(index) + '.wav'
        save_matrix_spec(instr_seq.spec_path, spec, sr)

        instr_seq.audio_path = path_prefix + str(index) + '.wav'
        write(instr_seq.audio_path, wav, sr)

        instr_seqs.append(instr_seq)

    cur_score.instr_seqs = instr_seqs
    return cur_score


# TODO add new instrument_recognition module

def save_matrix_spec(path, c, sr):
    spec_c = remove_zeros(c)
    librosa.display.specshow(spec_c, sr=sr, x_axis='time', y_axis='cqt_note')
    plt.set_cmap('hot')
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().yaxis.set_major_locator(plt.NullLocator())
    plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
    plt.margins(0, 0)
    plt.savefig(path, format='png', transparent=False, dpi=72, pad_inches=0)


def remove_zeros(c):
    zero_continues = True
    spec_c = np.array(c)
    db = librosa.amplitude_to_db(spec_c)
    count = 0
    while zero_continues:
        cur_frame = db[:, 0]
        for elem in cur_frame:
            if elem > 0:
                zero_continues = False
                break
        if zero_continues:
            spec_c = spec_c[:, 1:]
            db = db[:, 1:]
            count += 1
        else:
            break

    return spec_c
