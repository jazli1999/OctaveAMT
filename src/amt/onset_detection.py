"""detect onset for separated instrument sequences"""

from src.amt.amt_symbol import Note, InstrSeq, Score
import numpy as np
import librosa
import matplotlib.pyplot as plt


def onset_detect(cur_score):
    get_score_onset(cur_score)


def get_score_onset(cur_score):
    abs_onsets = []
    abs_values = []
    tempos = []

    for seq in cur_score.instr_seqs:
        onset, value, tempo = get_instr_onset(seq)
        abs_onsets.append(onset)
        abs_values.append(value)
        tempos.append(tempo)

    cur_score.tempo = get_tempo(tempos)

    for i in range(0, len(cur_score.instr_seqs)):
        onset = get_onset(abs_onsets[i], cur_score.tempo)
        value = get_value(cur_score.tempo, abs_values[i])
        notes = note_generation(onset, value)
        cur_score.instr_seqs[i].notes = notes


def get_tempo(tempos):
    tempo = tempos[0]

    return tempo


def note_generation(onset, value):
    notes = ()

    return notes


def get_instr_onset(cur_instr):
    abs_onset = get_abs_onset(cur_instr)
    tempo = get_semiquaver(abs_onset)
    onset = get_onset(abs_onset, tempo)
    value = get_value(abs_onset, tempo)

    return onset, value, tempo


def get_onset(abs_onset, tempo):
    # relevant onset based on tempo, to be filled in the instr_seq.notes
    onset = abs_onset
    return onset


def get_abs_onset(cur_instr):
    y, sr, c = get_matrix_spec(cur_instr)
    c = de_noise(c)
    d = get_eu_distance(c)
    d = smooth_eu_distance(d)
    d = moving_window_normal(y, sr, d)
    p = get_local_peak(d)

    abs_onset_note = []
    abs_value = []
    for i in range(0, p.shape[0]):
        if p[i] == 1:
            abs_onset_note.append(i)

    return abs_onset_note


def get_semiquaver(abs_onset_note):
    abs_value = []
    for i in range(0, len(abs_onset_note) - 1):
        abs_value.append(abs_onset_note[i + 1] - abs_onset_note[i])

    # Get the minimum as semiquaver
    semi = 0
    return semi


def get_value(semi, abs_value):
    value = []
    for i in abs_value:
        value.append(round(i/semi))
    return value


def get_matrix_spec(cur_instr):
    y, sr = librosa.load(cur_instr.audio_path)
    c = np.abs(librosa.cqt(y, sr=sr, hop_length=64, n_bins=84, bins_per_octave=12))

    librosa.display.specshow(c, sr=sr, x_axis='time', y_axis='cqt_note')
    plt.set_cmap('hot')
    plt.savefig(cur_instr.spec_path, format='png', transparent=False, dpi=72, pad_inches=0)

    return y, sr, c


def de_noise(c):
    n_c = c / np.max(c)
    sigma = 0.1
    for i in range(0, c.shape[0]):
        for j in range(0, n_c.shape[1]):
            if n_c[i][j] < sigma:
                n_c[i][j] = 0
    return n_c


def get_eu_distance(c):
    d = np.zeros([c.shape[0] - 1, c.shape[1]])
    for i in range(0, c.shape[0] - 1):
        d[i] = (c[i] - c[i + 1]) * (c[i] - c[i + 1])

    d = d.sum(axis=1)
    return d


def smooth_eu_distance(d):
    alpha = 0.4
    d = np.ndarray(d.shape)

    d[0] = d[0]
    for i in range(1, d.shape[0]):
        d[i] = alpha * d[i] + (1 - alpha) * d[i - 1]

    # 双边
    for i in range(1, d.shape[0]):
        d[i] = alpha * d[i] + (1 - alpha) * d[i - 1]

    return d


# moving window normalization
def moving_window_normal(y, sr, d):
    time = librosa.get_duration(y=y, sr=sr)
    win = int(d.shape[0] / time * 3)
    overlap = int(win / 2)
    hop = win - overlap
    std = 0
    # std for the "extremely large judgement"

    n_d = np.ndarray(d.shape)
    for i in range(0, d.shape[0] - win, hop):
        x = 0
        for j in range(i, i + win):
            if j == d.shape[0]:
                break
            x += d[j] * d[j]
        x = np.sqrt(x)

        for j in range(i, i + win):
            if j == d.shape[0]:
                break
            n_d[j] = d[j] / x
            std += n_d[j]

    # to cut out the "extremely large" parts
    std /= n_d.shape[0]
    std *= 10
    for i in range(0, n_d.shape[0]):
        if n_d[i] > std or n_d[i] < 0:
            n_d[i] = 0

    return n_d


def get_local_peak(d):
    # to cut out the "extremely large" parts
    p = np.ndarray(d.shape)

    p[0] = 0
    sigma = 0
    count = 0
    for i in range(1, p.shape[0] - 1):
        if d[i - 1] <= d[i] and d[i] >= d[i + 1]:
            p[i] = d[i]
            sigma += p[i]
            count += 1
        else:
            p[i] = 0

    sigma = sigma / count * 1.5
    for i in range(1, p.shape[0]):
        if p[i] <= sigma:
            p[i] = 0
        else:
            p[i] = 1
    return p

