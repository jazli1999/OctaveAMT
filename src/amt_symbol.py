'container for classes needed'

__author__ = 'OctaveAMT @ BUPT'

class note(object):
    __slots__ = ('onset', 'pitch', 'value')
    # onset is a integer stands for the beat number of the current note,
    # pitch is a integer tuple stands for the poly pitches of the current piece, 
    # value is length (how many beats) of the current piece  

    def __init__(self):
        pass


class instr_seq(object):
    __slots__ = ('instr', 'spec_path', 'notes')
    # instr is a string stands for the instrument,
    # spec_path is a string stands for the path of the transformed spectrogram,  
    # notes is a note instance list stands for the note stream of the current instrument 

    def __init__(self):
        pass

class score(object):
    __slots__ = ('audio_path', 'instr_seqs', 'tempo', 'midi_path')
    # audio_path is a string stands fot the path of the original audio,  
    # instr_seqs is a instr_seq list  
    # tempo is a integer represented by the length of semiquaver notes is a note instance list,  
    # midi_path is a strign stands for the path of the generated midi file  
    
    def __init__(self):
        pass

    