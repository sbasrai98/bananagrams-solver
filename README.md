# Bananagrams Solver

This program plays the word game [Bananagrams](https://en.wikipedia.org/wiki/Bananagrams).

![](https://github.com/sbasrai98/bananagrams-solver/blob/simulation/bgsolver.gif)

It was originally designed for a competition in which players move the pieces in real life but use their programs to dictate their moves. Thus, it offers you opportunities to cancel reorder attempts (if, for example, your opponent has called "peel" and you would like to enter the new letter). You can also have the program play automatically without user input. With option 1, it will randomly draw letters without replacement from the set of 144 letters in the game, either completing the game (about 77.5% of the time, see analysis below) or getting stuck in an infinite loop due to a hard scramble (no "dumps" allowed!). With option 2, it will randomly draw letters with replacement indefinitely.
