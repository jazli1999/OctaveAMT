import sys

from src.amt.amt_symbol import Note, InstrSeq, Score

from src.amt.src_sepa import src_separate
from src.amt.file_gen import midi_generate
from src.amt.onset_detection import onset_detect
from src.amt.pitch_detection import pitch_detect

from src.amt.src_sepa import pseudo_separate


def init_score(cur_score, path='./'):
    cur_score.audio_path = path


def automatic_music_transcription(file_path='./'):
    score = Score()
    init_score(score, file_path)

    src_separate(score)
    onset_detect(score)
    pitch_detect(score)
    midi_generate(score)


def pseudo_amt_for_onset(file_path='./'):
    score = Score()

    score = pseudo_separate(score)
    print('[1] Source Separation finished\n')

    onset_detect(score)
    print('[2] Onset detection finished\n')

    pitch_detect(score)
    print('[3] Pitch detection finished\n')


def pseudo_amt_for_separation(file_path='./resource/Sample.wav'):
    score = Score()
    score.audio_path = file_path
    score.instr_num = 2

    src_separate(score)
    print('[1] Source Separation finished\n')


def pseudo_amt(file_path='./resource/Sample.wav'):
    score = Score()
    score.audio_path = file_path
    score.instr_num = 2

    src_separate(score)
    print('[1] Source Separation finished\n')

    onset_detect(score)
    print('[2] Onset detection finished\n')

    pitch_detect(score)
    print('[3] Pitch detection finished\n')


def note_wide_normalization_test():
    score = Score()
    init_score(score, 'resource/star.wav')

    piano = InstrSeq()
    piano.instr = "piano"
    piano.spec_path = "resource/star.png"

    score.instr_seqs = []
    score.instr_seqs.append(piano)

    pseudo_separate(score)
    onset_detect(score)


if __name__ == '__main__':
    # argv[1] should be the path of the audio source 
    # note_wide_normalization_test()
    pseudo_amt_for_onset('./')
