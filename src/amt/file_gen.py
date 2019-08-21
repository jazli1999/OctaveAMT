"""MIDI and other related format file generation & conversion"""

__author__ = 'Yunfei Song @ BUPT'

from amt_symbol import Note, InstrSeq, Score
import os
import sys
import subprocess
import math

# 转换文件格式和编码方式
def to_lf(path, isLF, encoding = 'utf-8'):
    """
    :param path: 文件路径
    :param isLF: True 转为Unix(LF)  False 转为Windows(CRLF)
    :param encoding: 编码方式，默认utf-8
    :return:
    """
    newline = '\n' if isLF else '\r\n'
    tp = 'Unix(LF)' if isLF else 'Windows(CRLF)'
    with open(path, newline=None, encoding=encoding) as infile:
        str = infile.readlines()
        with open(path, 'w', newline=newline, encoding=encoding) as outfile:
            outfile.writelines(str)


def midi_generate(cur_score):  # cur_score should be a score instance

    melo = open('C:/melo-master/pieces/mymelo.melo','w')

    title = "test"
    composer = "test"
    beats = 4
    tempo = 80

    melo.write("title: " + title + "\n")
    melo.write("composer: " + composer + "\n")
    melo.write("beats: " + beats + "\n")
    melo.write("tempo: " + tempo + "\n")

    for cur_instr in cur_score.instr_seqs:

        count = [0,0,0,0]  # 记录音轨的当前小节的节拍数，假设为4/4拍

        number = [1,1,1,1]  # 记录第几个音符

        if cur_instr.instr == "Piano":
            melo.write("voice " + cur_instr.instr + " { channel: 1 }")  # 写入当前乐器，钢琴

        if cur_instr.instr == "Flute":    #现在假设只有钢琴和长笛两种乐器
            melo.write("voice " + cur_instr.instr + "\n{\n")
            melo.write("    program: 73")
            melo.write("    channel: 2\n")
            melo.write("}\n")

        melo.write("play " + cur_instr.instr + "{" + "\n")  #创建play块

        pitch_num = 1  # 记录最多有多少个音轨的变量

        for cur_note in cur_instr.notes:
            if len(cur_note.pitch) > pitch_num:  # 如果有哪一个note的pitch的元
                pitch_num = len(cur_note.pitch)   # 组数量大于当前pitch_num

        for i in range(0,pitch_num-1):  # 遍历音轨
            melo.write("    :| ")  # 每个音轨开始

            for j in range(0,len(cur_instr.notes)-1):  # 音轨开始
                if cur_instr.notes[j].value / 4 == 4:  # 全音符
                    melo.write(cur_instr.notes[j].pitch[i] + " | ")  # 一个小节完成
                    count[i] = count[i] + 4

                if j == len(cur_instr.notes) - 1:   # 最后一个
                    melo.write(cur_instr.notes[j].pitch[i] + " |\n")
                    count[i] = count[i] + 1 #暂时为1

                else:
                    if cur_instr.notes[j].value / 4 == 2:   # 二分音符
                        melo.write(cur_instr.notes[j].pitch[i] + " . ")
                        count[i] = count[i] + 2

                    if cur_instr.notes[j].value / 4 == 1:   # 四分音符
                        melo.write(cur_instr.notes[j].pitch[i] + " ")
                        count[i] = count[i] + 1

                    if cur_instr.notes[j].value / 4 == 0.75:  # 四分之三拍
                        melo.write(cur_instr.notes[j].pitch[i] + "-. ")
                        count1 = count1 + 0.75

                    if cur_instr.notes[j].value / 4 == 0.5:  # 八分音符
                        melo.write(cur_instr.notes[j].pitch[i] + "- ")
                        count[i] = count[i] + 0.5

                    if cur_instr.notes[j].value / 4 == 0.25:  # 十六分音符
                        melo.write(cur_instr.notes[j].pitch[i] + "-- ")
                        count[i] = count[i] + 0.25

                if count[i] == 4:
                    melo.write("|")
                    count[i] = 0

        melo.write("\n}\n\n")

    order = os.system("melo mid "+"C:/melo-master/pieces/mymelo.melo" + "--output mymelo.mid")

    if __name__ == "__main__":
        midi_generate(cur_score)
