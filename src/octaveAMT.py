import sys

from src.amt_symbol import note, instr_seq, score
from src.src_sepa import src_seperate
from src.file_gen import midi_generate
from src.pitch_detection import pitch_detect
from src.onset_detection import onset_detect

def init_score(cur_score, path):
    cur_score.audio_path = path

if __name__ == '__main__':
    # argv[1] should be the path of the audio source 
    cur_score = score()
    init_score(score, path = sys.argv[1])
    src_seperate(cur_score)
    onset_detect(cur_score)
    pitch_detect(cur_score)
    midi_generate(cur_score)