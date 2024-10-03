import unittest
from board import Board
from player import Player
from word import Word

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = Player()
        self.player.letters = list('BANANAGRAMS')

    def test_can_i_spell_1(self):
        self.assertEqual(self.player.can_i_spell('BANANAS'), True, 'word can be spelled')

    def test_can_i_spell_2(self):
        self.assertEqual(self.player.can_i_spell('GRAPES'), False, 'word cannot be spelled')



unittest.main()