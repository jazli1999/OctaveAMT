import sys

from amt.amt_symbol import Note, InstrSeq, Score

from amt.src_sepa import src_separate
from amt.file_gen import midi_generate
from amt.onset_detection import onset_detect
from amt.pitch_detection import pitch_detect


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
