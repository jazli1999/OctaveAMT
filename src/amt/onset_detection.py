"""detect onset for separated instrument sequences"""

from src.amt.amt_symbol import Note, InstrSeq, Score, VALUES_A, VALUES_B
import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt


def onset_detect(cur_score):
    get_score_onset(cur_score)


def get_score_onset(cur_score):
    abs_onsets = []
    abs_values = []
    tempos = []

    for seq in cur_score.instr_seqs:
        abs_onset, abs_value, tempo = get_instr_onset(seq)
        abs_onsets.append(abs_onset)
        abs_values.append(abs_value)
        tempos.append(tempo)

    cur_score.tempo = get_tempo(tempos, abs_values)

    for i in range(0, len(cur_score.instr_seqs)):
        onset = get_onset(abs_onsets[i], cur_score.tempo)
        value = get_value(onset)

        # the last onset is actually an offset
        onset.pop()

        notes = note_generation(onset, value)
        cur_score.instr_seqs[i].notes = notes


def get_instr_onset(cur_instr):
    abs_onset = get_abs_onset(cur_instr)
    # debug
    print(abs_onset)

    abs_value = get_abs_value(abs_onset)
    # debug
    print(abs_value)

    tempo = min(abs_value)
    # debug
    print(tempo)

    return abs_onset, abs_value, tempo


def get_tempo(tempos, abs_values):
    remains = [0, 0]

    avg = round(np.average(tempos))
    mini = round(min(tempos))

    remains[0] = get_remain(avg, abs_values)
    remains[1] = get_remain(mini, abs_values)

    if remains[0] < remains[1]:
        tempo = avg
    else:
        tempo = mini

    return tempo


def get_remain(num, array):
    remain = 0

    for n in array[0]:
        remain += (n % num)

    return remain


def note_generation(onset, value):
    notes = []

    for i in range(0, len(onset)):
        note = Note()
        note.onset = onset[i]
        note.value = value[i]
        notes.append(note)

    return notes


def get_abs_onset(cur_instr):
    y, sr, c = get_matrix_spec(cur_instr)
    c = de_dimension(c)
    c = de_noise(c)
    d = get_eu_distance(c)
    d = smooth_eu_distance(d)
    # d = moving_window_normal(y, sr, d)
    p = get_local_peak(d)

    abs_onset_note = []
    for i in range(0, p.shape[0]):
        if p[i] == 1:
            abs_onset_note.append(i)

    return abs_onset_note


def get_abs_value(abs_onset):
    abs_value = []
    for i in range(0, len(abs_onset)-1):
        abs_value.append(abs_onset[i+1] - abs_onset[i])

    return abs_value


def get_onset(abs_onset, tempo):
    # relevant onset based on tempo, to be filled in the instr_seq.notes
    onset = abs_onset

    for i in range(0, len(onset)):
        onset[i] = round(onset[i] / tempo)

    return onset


def get_value(onset):
    value = []

    for i in range(0, len(onset)-1):
        value.append(onset[i+1] - onset[i])

    for i in range(0, len(value)):
        match_a, bias_a = value_match(value[i], VALUES_A)
        match_b, bias_b = value_match(value[i], VALUES_B)

        if bias_a <= bias_b:
            value[i] = match_a
        else:
            value[i] = match_b

    return value


def value_match(v, v_tuple):
    match = v
    bias = 0

    if v in v_tuple:
        return match, bias
    else:
        match = v_tuple[0]
        bias = abs(v-v_tuple[0])

        for i in range(0, len(v_tuple)):
            new_bias = abs(v-v_tuple[i])
            if new_bias < bias:
                match = v_tuple[i]
                bias = new_bias

        return match, bias


def get_matrix_spec(cur_instr):
    y, sr = librosa.load(cur_instr.audio_path)
    c = np.abs(librosa.cqt(y, sr=sr, hop_length=64, n_bins=84, bins_per_octave=12))

    librosa.display.specshow(c, sr=sr, x_axis='time', y_axis='cqt_note')
    plt.set_cmap('hot')
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().yaxis.set_major_locator(plt.NullLocator())
    plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
    plt.margins(0, 0)
    plt.savefig(cur_instr.spec_path, format='png', transparent=False, dpi=72, pad_inches=0)

    return y, sr, c


def de_dimension(c):
    d_c = np.zeros([1, c.shape[0]])
    local_sum = np.zeros([1, c.shape[0]])
    # 84*1

    i = 0
    de_di_rate = 8
    for i in range(0, c.shape[1]):
        if (i + 1) % de_di_rate != 0:
            local_sum += c[:, i]
        else:
            local_sum /= de_di_rate
            d_c = np.r_[d_c, local_sum]
            local_sum = np.zeros([1, c.shape[0]])

    if (i + 1) % de_di_rate != 0:
        local_sum /= (i + 1) % de_di_rate
        d_c = np.r_[d_c, local_sum]

    return d_c


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
    s_d = np.ndarray(d.shape)

    s_d[0] = d[0]
    for i in range(1, d.shape[0]):
        s_d[i] = alpha * d[i] + (1 - alpha) * s_d[i - 1]

    # 双边
    for i in range(1, d.shape[0]):
        s_d[i] = alpha * s_d[i] + (1 - alpha) * s_d[i - 1]

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
