# Checkers-with-AI

[![wakatime](https://wakatime.com/badge/github/MeesumAliQazalbash/Checkers-with-AI.svg)](https://wakatime.com/badge/github/MeesumAliQazalbash/Checkers-with-AI)
![Lines of code](https://img.shields.io/tokei/lines/github/MeesumAliQazalbash/Checkers-with-AI)
![GitHub commit activity](https://img.shields.io/github/commit-activity/y/MeesumAliQazalbash/Checkers-with-AI)

[![Total alerts](https://img.shields.io/lgtm/alerts/g/MeesumAliQazalbash/Checkers-with-AI.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/MeesumAliQazalbash/Checkers-with-AI/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/MeesumAliQazalbash/Checkers-with-AI.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/MeesumAliQazalbash/Checkers-with-AI/context:python)

## Description

Checkers was a first project that I made in my first year of university. It has been really close to my heart. In this project I tried to make a game that is not only a game but also a game that is fun to play. The code is completely new from the scratch. The logic is pretty simple and the game is fun to play.

## Dependencies

`Python3.6` or above and a computer that can run it.

## How to play

Simply enter the coordinates of the board and the piece you want to move. The terminal will show you the board like this, with some extra information.

```shell
0  1  2  3  4  5  6  7
0  ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫
1  ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫
2  ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫
3  🟨 🟥 🟨 🟥 🟨 🟥 🟨 🟥
4  🟥 🟨 🟥 🟨 🟥 🟨 🟥 🟨
5  ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪
6  ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪
7  ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪

Black:  24
White:  24
Move: 0

Enter your move dear human.
```

Now you have to give the moves you want to play. For example I want to move the piece from (5,3) (5th row and 3rd column according to the board) to (4,4). I will write each of them in order and when the I have to stop simply write `q` (short form for quit) in the input.

```shell
Enter your move dear human.
5 3
4 4
q
```

Hit enter the your move will be played by the computer.

```shell
   0  1  2  3  4  5  6  7
0  ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫
1  ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫
2  ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫
3  🟨 🟥 🟨 🟥 🟨 🟥 🟨 🟥
4  🟥 🟨 🟥 🟨 ⚪ 🟨 🟥 🟨
5  ⚪ ⚪ ⚪ 🟩 ⚪ ⚪ ⚪ ⚪
6  ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪
7  ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪

Black:  24
White:  24
Move: 1
```

After this instantly your opponent the might computer will play the move. The board may pass on quickly and to keep the record of which move has been played we added a green sqaure in the path of each hop.

```shell
   0  1  2  3  4  5  6  7
0  ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫
1  ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫
2  🟩 ⚫ ⚫ ⚫ ⚫ ⚫ ⚫ ⚫
3  🟨 ⚫ 🟨 🟥 🟨 🟥 🟨 🟥
4  🟥 🟨 🟥 🟨 ⚪ 🟨 🟥 🟨
5  ⚪ ⚪ ⚪ 🟥 ⚪ ⚪ ⚪ ⚪
6  ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪
7  ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪ ⚪

Black:  24
White:  24
Move: 2

Enter your move dear human.
```

Now you have to enter the move again. The game will keep on going until one of the player wins or game draws.
