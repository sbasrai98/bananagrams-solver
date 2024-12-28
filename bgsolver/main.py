import time
import random
import pandas as pd
from bgsolver.board import Board
from bgsolver.word import Word
from bgsolver.player import Player

pd.set_option('display.max_rows', None,
              'display.max_columns', None,
              'display.width', None)

def game_manual():
    board = Board()
    player = Player()
    while True: 
        original_count = len(player.letters)
        word = player.choose_word(board)
        if word:
            player.make_word(word, board)
        if len(player.letters) == 0:
            if not player.get_letters(board): break
        elif len(player.letters) == original_count:
            # stuck with leftover letter. try reordering
            if player.reorder(board):
                pass # player has used all letters, next iter will ask for more
            else:
                if not player.get_letters(board): break # player must have cancelled reorder() to input new letters

def game_auto(seed=random.randint(0,10000)):
    board = Board()
    player = Player()
    start = time.time()
    random.seed(seed)

    # choose first 21 letters
    player.letters = random.sample(board.letters, 21)
    # remove from board's letters
    for l in player.letters:
        board.letters.remove(l)
        # board.letter_feed.append(l)
    
    while True: 
        current_time = time.time() - start
        print('#####',
              f'letters remaining: {len(board.letters)}',
              f'time: {current_time}',
              '#####', sep='\n')

        original_count = len(player.letters)
        word = player.choose_word(board)
        if word:
            player.make_word(word, board)
        if len(player.letters) == 0:
            if not player.get_letters(board, mode='auto'):
                total_time = time.time() - start
                print(f'Total time: {total_time}')
                break
        elif len(player.letters) == original_count:
            # stuck with leftover letter. try reordering
            if player.reorder(board, mode='auto'):
                pass # player has used all letters, next iter will ask for more
            else:
                # reorder() returned False, stuck in infinite loop
                print('BGSolver was unable to resolve the board.')
                total_time = time.time() - start
                print(f'Total time: {total_time}')
                break

def main():
    mode = input('Select game mode:\n')
    if mode == '1':
        game_manual()
    else:
        game_auto(int(mode))

myword = Word('FLABBERGASTED',
              [(0, i) for i in range(len('FLABBERGASTED'))],
              'horizontal',
              None)
next = Word('A',
            [(0,-2)],
            'horizontal',
            (5,5))

if __name__ == '__main__':
    main()
