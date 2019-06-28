# OctaveAMT  
---  
Three classes are involved.  
`note` class stands for the **notes** occur concurrently, with detailed information of instrument, onset, pitch and value.  

`instr_seq` class stands for the notes sequence for each instrument, which contains the notes stream and the path of the transformed spectrogram.  

`score` class represents the whole music piece, with the path of the original audio, an `instr_seq` instance list, the tempo of the piece and the path of the generated MIDI file.  

## Class `note`  
```python   
class note(object):
    __slots__ = ('instr', 'onset', 'pitch', 'value')
    # onset is a integer stands for the beat number of the current note,
    # pitch is a integer tuple stands for the poly pitches of the current piece, 
    # value is length (how many beats) of the current piece  

    def __init__(self):
        pass

```  

## Class `instr_seq`  
```python  
class instr_seq(object):
    __slots__ = ('instr', 'spec_path', 'notes')
    # instr is a string stands for the instrument,
    # spec_path is a string stands for the path of the transformed spectrogram,  
    # notes is a note instance list stands for the note stream of the current instrument  
    
    def __init__(self):
        pass
    
```  

## Class `score`  
```python  
class score(object):  
    __slots__ = ('audio_path', 'instr_seqs', 'tempo', 'midi_path')  
    # audio_path is a string stands fot the path of the original audio,  
    # instr_seqs is a instr_seq list  
    # tempo is a integer represented by the length of semiquaver notes is a note instance list,  
    # midi_path is a strign stands for the path of the generated midi file  

```  