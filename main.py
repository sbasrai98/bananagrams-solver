# %%

# %%
import random
import time
from board import Board
from word import Word
from player import Player
import pandas as pd
import os

pd.set_option('display.max_rows', None,
              'display.max_columns', None,
              'display.width', None)

GAMES_DIR_A = '/Users/sbasrai/Desktop/projects/bananagrams-solver/games/'
GAMES_DIR_B = '/Users/sbasrai/Desktop/projects/bananagrams-solver/fails/'

myletters = ['D','E','X','T','E','R','O','U','S','L', 'Y','W', 'Q', 'G', 'V', 'W', 'Q', 'T', 'E', 'Y', 'D']
myletters = ['U', 'U', 'U', 'A', 'W', 'W', 'A', 'R', 'M', 'R', 'S', 'A', 'I', 'S', 'F', 'I', 'X', 'A', 'T', 'I', 'V', 'E']

def save_game(board: Board, total_time, game_lost):
    cur_time = time.gmtime()
    hr, mn, sec = cur_time.tm_hour, cur_time.tm_min, cur_time.tm_sec
    lastword = board.words_made[0].word
    newdir = GAMES_DIR_A+f'{lastword}_{hr}_{mn}_{sec}/'
    if game_lost:
        newdir = GAMES_DIR_B+f'{lastword}_{hr}_{mn}_{sec}/'
    os.mkdir(newdir)
    with open(newdir+'total_time.txt', 'w') as fout:
        fout.write(str(total_time)+'\n')
        fout.write(''.join(board.letter_feed)+'\n')
    with open(newdir+'time_steps.txt', 'w') as fout:
        for t in board.time_steps:
            fout.write(str(t)+'\n')
        fout.write('\n')
    with open(newdir+'words.txt', 'w') as fout:
        for w in board.words_made:
            fout.write(w.word+'\n')

def game_loop():
    board = Board()
    player = Player()
    start = board.start
    
    # choose first 21 letters
    player.letters = random.sample(board.letters, 21)
    # player.letters = myletters

    # remove from board's letters
    for l in player.letters:
        board.letters.remove(l)
        board.letter_feed.append(l)

    # downsample board
    # board.letters = random.sample(board.letters, 0)

    while True: 
        ctime = time.time() - start
        print('#####',
              f'letters remaining: {len(board.letters)}',
              f'time: {ctime}',
              '#####', sep='\n')

        original_count = len(player.letters)
        word = player.choose_word(board)
        if word:
            player.make_word(word, board)
        if len(player.letters) == 0:
            if not player.get_letters(board):
                total_time = time.time() - start
                print(total_time)
                save_game(board, total_time, game_lost=False)
                break
        elif len(player.letters) == original_count:
            # stuck with leftover letter. try reordering
            if player.reorder(board):
                pass # player has used all letters, next iter will ask for more
            else:
                # reorder() returned False, stuck in infinite loop
                total_time = time.time() - start
                print(total_time)
                save_game(board, total_time, game_lost=True)
                break 

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

if __name__ == '__main__':
    game_loop()
