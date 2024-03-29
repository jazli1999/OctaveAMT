"""container for classes needed"""

__author__ = 'OctaveAMT @ BUPT'


VALUES_A = (1, 2, 4, 8, 16)
VALUES_B = (3, 6, 12)


class Note(object):
    __slots__ = ('onset', 'pitch', 'value')
    # onset is a integer stands for the beat number of the current note,
    # pitch is a integer tuple stands for the poly pitches of the current piece, 
    # value is length (how many beats) of the current piece  

    def __init__(self):
        pass


class InstrSeq(object):
    __slots__ = ('instr', 'cqt_matrix', 'spec_path', 'notes')
    # instr is a string stands for the instrument,
    # cqt_matrix is a np.array stands for the CQT coefficient matrix,
    # audio_path is a string stands for the path of separated audio sequence,
    # spec_path is a string stands for the path of the transformed spectrogram,  
    # notes is a note instance list stands for the note stream of the current instrument 

    def __init__(self):
        pass


class Score(object):
    __slots__ = ('audio_path', 'instr_num', 'instr_seqs', 'tempo', 'midi_path', 'sr')
    # audio_path is a string stands fot the path of the original audio,
    # instr_num is a integer stands for the number of instruments needed to be separated
    # instr_seqs is a instr_seq list  
    # tempo is a integer represented by the length of semiquaver notes is a note instance list,  
    # midi_path is a string stands for the path of the generated midi file
    # sr is a integer stands for the sample rate of the audio
    
    def __init__(self):
        pass
