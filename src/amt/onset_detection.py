"""detect onset for separated instrument sequences"""

from src.amt.amt_symbol import Note, InstrSeq, Score
import numpy as np
import librosa
import matplotlib.pyplot as plt


def onset_detect(cur_score):
    pass


def get_matrix_spec(cur_instr):
    y, sr = librosa.load(cur_instr.audio_path)
    c = np.abs(librosa.cqt(y, sr=sr, hop_length=64, n_bins=84, bins_per_octave=12))

    librosa.display.specshow(c, sr=sr, x_axis='time', y_axis='cqt_note')
    plt.set_cmap('hot')
    plt.savefig(cur_instr.spec_path, format='png', transparent=False, dpi=72, pad_inches=0)

    return c, sr


def denoise(c):
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


def smooth_eu_distance(d):
    alpha = 0.4
    s_d = np.ndarray(d.shape)

    s_d[0] = d[0]
    for i in range(1, d.shape[0]):
        s_d[i] = alpha * d[i] + (1 - alpha) * s_d[i - 1]

    # 双边
    for i in range(1, d.shape[0]):
        s_d[i] = alpha * s_d[i] + (1 - alpha) * s_d[i - 1]

    return s_d


# peak detection
# moving window normalization
# local peak extraction
