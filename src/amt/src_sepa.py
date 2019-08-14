"""Separate the mixed audio source to individual instrument"""

from src.amt.amt_symbol import Note, InstrSeq, Score
from sklearn.decomposition import NMF
from librosa.core import cqt, icqt

import numpy as np
import librosa.display
import librosa.util


def src_separate(cur_score):
    nmf_src_separate(cur_score)


def pseudo_separate(cur_score):
    cur_score.audio_path = 'resource/star.wav'

    cur_score.instr_seqs = []
    cur_score.instr_seqs.append(InstrSeq())
    cur_score.instr_seqs[0].instr = 'piano'
    cur_score.instr_seqs[0].spec_path = 'resource/star.png'

    y, sr = librosa.load(cur_score.audio_path)
    c = abs(cqt(y, sr=sr, hop_length=64, n_bins=84, bins_per_octave=12))
    cur_score.sr = sr
    cur_score.instr_seqs[0].cqt_matrix = c

    return cur_score


def nmf_src_separate(cur_score):
    y, sr, c, phase = load_audio(cur_score.audio_path)
    cur_score.sr = sr

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


def reconstruct(n_w, n_h, n_components, sr, phase):
    # n_s for all specs
    # n_c for all synthesis audios
    n_spec = []
    n_wav = []
    for i in range(0, n_components):
        w = n_w[:, i:i + 1]
        h = n_h[i:i + 1, :]
        s = np.multiply(w, h)
        c = s * phase
        wav = icqt(c, sr=sr, hop_length=64)

        n_spec.append(s)
        n_wav.append(wav)

    return n_spec, n_wav


def instr_seqs_generate(cur_score, n_spec, n_wav, sr):
    instr_seqs = []
    path_prefix = cur_score.audio_path.split('.wav')[0] + '_'

    for spec, wav, index in zip(n_spec, n_wav, range(0, cur_score.instr_num)):
        instr_seq = InstrSeq()
        instr_seq.cqt_matrix = spec
        instr_seq.spec_path = path_prefix + str(index) + '.png'

        instr_seqs.append(instr_seq)

    cur_score.instr_seqs = instr_seqs
    return cur_score


# TODO add new instrument_recognition module
