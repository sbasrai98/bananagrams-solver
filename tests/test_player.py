import unittest
from bgsolver.board import Board
from bgsolver.player import Player
from bgsolver.word import Word

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = Player()
        self.player.letters = list('BANANAGRAMS')

    def test_can_i_spell_1(self):
        self.assertEqual(self.player.can_i_spell('BANANAS'), True, 'word can be spelled')

    def test_can_i_spell_2(self):
        self.assertEqual(self.player.can_i_spell('GRAPES'), False, 'word cannot be spelled')
