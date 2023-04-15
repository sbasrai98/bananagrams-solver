#%%
import pandas as pd
import random
with open('58k-words.txt') as fin:
    word_list = [x.rstrip().upper() for x in fin.readlines()]

pd.set_option('display.max_rows', None,
              'display.max_columns', None,
              'display.width', None)

# unittest
# debugging

#%%
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

class Board:
    all_letters = list('JKQXZ'*2 + 'BCFHMPVWY'*3 + 'G'*4 + 'L'*5 + 'DSU'*6 + \
                       'N'*8 + 'TR'*9 + 'O'*11 + 'I'*12 + 'A'*13 + 'E'*18)
    
    def __init__(self):
        self.board = pd.DataFrame(index=range(-100,100), columns=range(-100,100))
        self.letters = Board.all_letters
        self.words_made = []

    def room_for_word(self, word: Word):        
        must_be_free = []
        must_be_free.extend(word.coordinates)
        if word.overlap:
            must_be_free.pop(must_be_free.index(word.overlap))
            if word.orientation == 'horizontal':
                for row, col in word.coordinates:
                    if col != word.overlap[1]:
                        must_be_free.append((row+1, col))    
                        must_be_free.append((row-1, col))
                first_row, first_col = word.coordinates[0] 
                must_be_free.append((first_row, first_col-1))    
                last_row, last_col = word.coordinates[-1]
                must_be_free.append((last_row, last_col+1))
            else: # word is vertical
                for row, col in word.coordinates:
                    if row != word.overlap[0]:
                        must_be_free.append((row, col+1))    
                        must_be_free.append((row, col-1))
                first_row, first_col = word.coordinates[0] 
                must_be_free.append((first_row-1, first_col))    
                last_row, last_col = word.coordinates[-1]
                must_be_free.append((last_row+1, last_col))
        for row, col in must_be_free:
            if not pd.isna(self.board.at[row, col]):
                return False
        return True

class Player:

    def __init__(self, letters=[]):
        self.letters = letters
        self.history = []

    def get_letters(self, letters=''): # should be taken from board..
        new_letters = letters
        while not(new_letters.isalpha() and new_letters.isupper()):
            new_letters = input('Enter letters:\n')
            if new_letters.isalpha() and new_letters.isupper():
                self.letters.extend(list(new_letters))
            elif new_letters == 'stop':
                return True
            else:
                print('Invalid.')
        return False
        # print(self.letters)
    
    def can_i_spell(self, word: str):
        for l in set(word):
            if word.count(l) > self.letters.count(l):
                return False
        return True

    def possible_words(self, board: Board):
        # return list of words possible given players letters and words
        # currently on the board
        possible_words = []
        if board.words_made == []:
            for w in word_list:
                if self.can_i_spell(w):
                    new_coords = list(zip([0]*len(w), range(len(w))))
                    possible_words.append(Word(w, new_coords, 'horizontal', None))
        else:    
            for w in board.words_made:
                for pos, l in zip(w.coordinates, w.word):
                    self.letters.append(l)
                    new_words = [word for word in word_list \
                                if l in word and self.can_i_spell(word)]
                    self.letters.pop(-1)
                    for word in new_words:
                        idx = word.index(l)
                        if w.orientation == 'horizontal':
                            new_orient = 'vertical'
                            new_coords = list(zip(
                                range(pos[0]-idx, pos[0]-idx+len(word)),
                                [pos[1]]*len(word)))
                        else:
                            new_orient = 'horizontal'
                            new_coords = list(zip([pos[0]]*len(word),
                                    range(pos[1]-idx, pos[1]-idx+len(word))))
                        possible_words.append(Word(word, new_coords,
                                                new_orient, pos))
        return [w for w in possible_words if board.room_for_word(w)]

    def choose_word(self, board: Board, priority=False):
        choices = self.possible_words(board)
        if choices == []:
            return None
        if priority:
            choices.sort(key=word_priority)
        else:
            choices.sort(key=lambda x: -len(x.word))
        #return random.choice(choices)
        return choices[0]
    
    def make_word(self, word: Word, board: Board):
        if board.room_for_word(word):
            for pos, l in zip(word.coordinates, word.word):
                if pd.isna(board.board.at[pos[0], pos[1]]):
                    board.board.at[pos[0], pos[1]] = l
                    self.letters.pop(self.letters.index(l))
            board.words_made.append(word)
            print('Making', word.word, 'at position', word.coordinates[0])
            print('\n')
            print(board.board.dropna(axis=0, how='all').dropna(axis=1, how='all').fillna(' '))
            print(self.letters)
            return word

    def break_word(self, board: Board): # the last word made
        last_word = board.words_made.pop(-1)
        for row, col in last_word.coordinates:
            if (row, col) != last_word.overlap:
                self.letters.append(board.board.at[row, col])
                board.board.at[row, col] = pd.NA
        print('Breaking', last_word.word, 'at position',
              last_word.coordinates[0])
        print('\n')
        print(board.board.dropna(axis=0, how='all').dropna(axis=1, how='all').fillna(' '))
        print(self.letters)
        return last_word

    def reorder(self, board: Board):
        # stuck with leftover letter. how to deal?
        # break last word, apply priority word building, see if resolves.
        # if not, reset. break last 2 words, apply priority building, see if resolves.
        # repeat until resolved. but after each iteration, stop and ask user if it should keep trying.
        #  (user would answer no if new letters have come in from someone calling peel)
        #  so if answer is no, should return the player to game loop, leading to get_letters call
        original_self_letters = self.letters[:]
        original_board = board.board.copy()
        original_words_made = board.words_made[:]
        print('Attempting to reorder the board...')

        break_words = 1
        while self.letters != []:
            for i in range(break_words):
                self.break_word(board)

            while self.letters != []:
                new = self.choose_word(board, priority=True)
                if new:
                    self.make_word(new, board)
                elif break_words == len(original_words_made): 
                    # whole board has been broken. 
                    # try reordering the board from its current state...
                    if input('Whole board has been broken. Attempt reordering from new state?\n') != '':
                        return
                    else:
                        self.reorder(board)
                        return


                else:
                    break

            if self.letters != []:
            # tried breaking last and fixing, didnt work, stuck with leftover letter and no words to make again.
            # reset, try the whole process with 2 breaks this time
                
                

                
                self.letters = original_self_letters[:]
                board.board = original_board.copy()
                board.words_made = original_words_made[:]
                break_words += 1

                if input('Continue trying to reorder? (iter=%d)\n' % break_words) != '':
                    # user doesn't want to keep trying, function returns
                    return False # was reorder attempt successful? no. 
                                 #  but player prob has more letters to input and is cancelling the attempt
                
            # otherwise, attempt to reorder was successful, letters == [], loop will end now
        
        print('Reorder attempt successful!')
        return True # reorder attempt succesful
    
def game_loop():
    board = Board()
    player = Player()
    last_made_word = Word('',(0,0),'horizontal',None)
    while True: 
        #board.board.dropna(axis=0, how='all').dropna(axis=1, how='all')
        original_count = len(player.letters)
        word = player.choose_word(board) #, contains=priority
        if word:
            last_made_word = player.make_word(word, board)
            
        # if len(player.letters) == original_count:
        if len(player.letters) == 0:
            stop = player.get_letters()
            if stop:
                break
        elif len(player.letters) == original_count:
            # stuck with leftover letter. try breaking
            if player.reorder(board):
                pass # player has used all letters, next iter will ask for more
            else:
                player.get_letters() # player must have cancelled reorder() since new letters came

        #     priority = player.letters[0]
        #     print('\n')
        #     print(board.board.dropna(axis=0, how='all').dropna(axis=1, how='all').fillna(' '))
        #     print(player.letters)

myword = Word('FLABBERGASTED',
              [(0, i) for i in range(len('FLABBERGASTED'))],
              'horizontal',
              None)
next = Word('A',
            [(0,-2)],
            'horizontal',
            (5,5))

#GTRXAEBHIOULAPO

b = Board()
#b.board.at[0,2] = 'F'
#p = Player(letters=list('FLABBERGASTEDI'))
p = Player()
#tst = p.choose_word(b)

# print(b.room_for_word(myword))
# p.make_word(myword, b)
# print(p.letters)
# # print(b.room_for_word(next))
# # p.place_word(next, b)

# b.board.dropna(axis=0, how='all').dropna(axis=1, how='all')

game_loop()

# %%
