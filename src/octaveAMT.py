import sys

from src.amt.amt_symbol import Note, InstrSeq, Score

from src.amt.src_sepa import src_separate
from src.amt.file_gen import midi_generate
from src.amt.onset_detection import onset_detect
from src.amt.pitch_detection import pitch_detect


def init_score(cur_score, path='./'):
    cur_score.audio_path = path


def automatic_music_transcription(filepath='./'):
    score = Score()
    init_score(score, filepath)

    src_separate(score)
    onset_detect(score)
    pitch_detect(score)
    midi_generate(score)


def pseudo_amt(filepath='./'):
    score = Score()
    init_score(score, filepath)

    piano = InstrSeq()
    piano.instr = "piano"
    piano.audio_path = "1.wav"

    score.instr_seqs = []
    score.instr_seqs.append(piano)
    onset_detect(score)


if __name__ == '__main__':
    # argv[1] should be the path of the audio source 

    if len(sys.argv) > 1:
        pseudo_amt(sys.argv[1])
    else:
        pseudo_amt()