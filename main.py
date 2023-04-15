from board import Board
from word import Word
from player import Player
import pandas as pd
pd.set_option('display.max_rows', None,
              'display.max_columns', None,
              'display.width', None)

def game_loop():
    board = Board()
    player = Player()
    while True: 
        original_count = len(player.letters)
        word = player.choose_word(board)
        if word:
            player.make_word(word, board)
        if len(player.letters) == 0:
            if not player.get_letters(): break
        elif len(player.letters) == original_count:
            # stuck with leftover letter. try reordering
            if player.reorder(board):
                pass # player has used all letters, next iter will ask for more
            else:
                if not player.get_letters(): break # player must have cancelled reorder() to input new letters

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