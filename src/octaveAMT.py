import sys

from src.amt.amt_symbol import Note, InstrSeq, Score

from src.amt.src_sepa import src_separate
from src.amt.file_gen import midi_generate
from src.amt.onset_detection import onset_detect
from src.amt.pitch_detection import pitch_detect


def init_score(cur_score, path='./'):
    cur_score.audio_path = path


if __name__ == '__main__':
    # argv[1] should be the path of the audio source 
    score = Score()

    if len(sys.argv) > 1:
        init_score(cur_score=score, path=sys.argv[1])
    else:
        init_score(cur_score=score)
    src_separate(score)

    onset_detect(score)
    pitch_detect(score)
    midi_generate(score)
