# %%
import re

def encode1(seq):
    seq = re.sub(r'[EAIO]', '1', seq)
    seq = re.sub(r'[TRNDSULG]', '2', seq)
    seq = re.sub(r'[BCFHMPVWY]', '3', seq)
    seq = re.sub(r'[JKQXZ]', '4', seq)
    return seq

def encode2(seq):
    # encode2, w=3, 0.24096269643535118
    seq = re.sub(r'[AEIOU]', '1', seq)
    seq = re.sub(r'[BCFHMPVWYTRNDSLG]', '2', seq)
    seq = re.sub(r'[JKQXZ]', '3', seq)
    return seq

def encode3(seq):
    # encode3, w=3, 0.2431318548515956
    seq = re.sub(r'[AEIOUH]', '1', seq)
    seq = re.sub(r'[BFMPWYTRNDSLG]', '2', seq)
    seq = re.sub(r'[JKQXZCV]', '3', seq)
    return seq




###################
def encode4(seq):
    # encode4, w=3, 0.23499433405680462
    seq = re.sub(r'[AEIOUH]', '1', seq)
    seq = re.sub(r'[MNPSTY]', '2', seq)
    seq = re.sub(r'[BFWRDLG]', '3', seq)
    seq = re.sub(r'[JKQXZCV]', '4', seq)
    return seq

def encode5(seq):
    # encode5, w=3, 0.23426424838003496
    seq = re.sub(r'[AEIOUH]', '1', seq)
    seq = re.sub(r'[MNPSTY]', '2', seq)
    # seq = re.sub(r'[]', '3', seq)
    seq = re.sub(r'[BFWRDLGJKQXZCV]', '4', seq)
    return seq



# def encode4(seq):
#     seq = re.sub(r'[AEIOUHBFMPWYTRNDS]', '1', seq)
#     seq = re.sub(r'[JKQXZCVLG]', '3', seq)
#     return seq

# def encode4(seq):
#     seq = re.sub(r'[AEIOUH]', '1', seq)
#     seq = re.sub(r'[BFMPWYTRNDS]', '2', seq)
#     seq = re.sub(r'[JKQXZCVLG]', '3', seq)
#     return seq

# def encode4(seq):
#     seq = re.sub(r'[HOMNPSEAITY]', '1', seq)
#     seq = re.sub(r'[RWBFDU]', '2', seq)
#     seq = re.sub(r'[KGXLVQCJZ]', '3', seq)
#     return seq