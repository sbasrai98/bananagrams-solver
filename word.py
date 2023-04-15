with open('58k-words.txt') as fin:
    WORD_LIST = [x.rstrip().upper() for x in fin.readlines()]

class Word:
    def __init__(self, word, coordinates, orientation, overlap):
        self.word = word # string
        self.coordinates = coordinates # list of tuples
        self.orientation = orientation # 'horizontal' / 'vertical'
        self.overlap = overlap # tuple of slot overlapping with existing word

    # LEN, get_item -> iter -> contains

def word_priority(word: Word):
    difficulty_order = 'QJZXVKWYFBGHMPDUCLSNTOIRAE'
    score = 1
    for i, l in enumerate(difficulty_order):
        if l in word.word:
            score *= 1000*i
            break
    score -= len(word.word)
    return score
