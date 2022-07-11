import json
import os
import random
import time
from itertools import product
from typing import Optional


class Checker:
    """class to simulate checkers game where human/computer play against computer"""

    # normal unit hopes
    normal_unit_hops = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    # tiles used to print the board
    tile = {
        'b': '⚫',
        'B': '⬛',
        'w': '⚪',
        'W': '⬜',
        'r': '🟥',
        'y': '🟨',
        'h': '🟩'
    }

    def __init__(self,
                 human: bool = False,
                 clear_screen: bool = True,
                 delay: float = 0.0) -> None:
        """Constructor

        Args:
            human (bool, optional): if True then human will from white's side. Defaults to False.
            clear_screen (bool, optional): if True then clear screen after each new move. Defaults to True.
            delay (float, optional): delay in number of seconds for next board to appear. Defaults to 0.0."""
        self.human = human
        self.clear_screen = clear_screen
        self.delay = delay
        self.stats = {
            'win': {
                'w': {
                    'avg moves': 0,
                    'count': 0
                },
                'b': {
                    'avg moves': 0,
                    'count': 0
                }
            },
            'draw': 0
        }

    def initiate_pieces(self) -> None:
        """places the pieces on the board"""
        self.piece = dict()
        for c in range(8):
            for r in range(3):
                # placing the black pieces on the upper three rows of the board
                self.piece[(r, c)] = 'b'
                # placing the white pieces on the lower three rows of the board
                self.piece[(7 - r, c)] = 'w'
            for r in range(3, 5):
                # placing the empty pieces on the mid two rows of the board
                self.piece[(r, c)] = 'o'

    def print_screen(self, move_count: int = 0) -> None:
        """print the board on the terminal

        Args:
            move_count (int, optional): move number. Defaults to 0."""
        for i, j in product(range(8), range(8)):
            color = 'y' if (i + j) % 2 else 'r'  # changing the color
            # if piece was in the last move then its 'h' for tiling
            p = 'h' if (i, j) in self.last_move else self.piece[(i, j)]
            if p == 'o':
                p = color  # color for empty piece
            print(self.tile[p], end=None if j == 7 else ' ')
        print('\nBlack: ', self.count['b'])
        print('White: ', self.count['w'])
        print('Move:', move_count, end='\n\n')

    @staticmethod
    def L1_norm(x: tuple[int, int], y: tuple[int, int]) -> int:
        """returns the distance between x and y in L1 norm space.

        Args:
            x (tuple[int, int]): first point.
            y (tuple[int, int]): second point.

        Returns:
            int: distance between x and y in L1 norm space.
        """
        return abs(x[0] - y[0]) + abs(x[1] - y[1])

    def move(self, pos: Optional[tuple[int, int]], side: str) -> None:
        """moves the piece according to the sequence of position given to

        Args:
            pos (Optional[tuple[int, int]]): sequence of position to move piece on the board
            side (str): piece is from which side"""
        # changing the sides
        opp_side = 'b' * (side == 'w') + 'w' * (side == 'b')
        # function to calculate mid of two position
        mid_rc = lambda x, y: ((x[0] + y[0]) >> 1, (x[1] + y[1]) >> 1)

        # if the are only two hops and they are trivial means only
        # hoping to their digonally adjacent neighbours
        if len(pos) == 2 and Checker.L1_norm(pos[0], pos[1]) == 2:
            # checking if horse has to be made
            if pos[1][0] == 7 * (side == 'b'):
                self.piece[pos[1]] = self.piece[pos[0]].upper()
            else:
                self.piece[pos[1]] = self.piece[pos[0]]
            self.piece[pos[0]] = 'o'

        else:
            # if the hop is beating the opposite side pieces
            for i in range(len(pos) - 1):
                if (  # there is always an empty piece after the hop
                        self.piece[pos[i + 1]] == 'o'
                        # the hop must be jumping two squares doiagonally
                        and Checker.L1_norm(pos[i + 1], pos[i]) == 4
                        # there must be a peice of opposite side between the jump and landing position
                        and self.piece[mid_rc(pos[i + 1], pos[i])].lower()
                        == opp_side):

                    self.count[opp_side] -= 1  # reducing the count
                    # setting the middle piece as empty piece
                    self.piece[mid_rc(pos[i + 1], pos[i])] = 'o'

                    # checking if horse has to be made
                    if pos[i + 1][0] == 7 * (side == 'b'):
                        self.piece[pos[i + 1]] = self.piece[pos[i]].upper()
                    else:
                        self.piece[pos[i + 1]] = self.piece[pos[i]]

                    self.piece[pos[i]] = 'o'  # setting middle as empty
                else:
                    # breaking the chain of hopping because we have illegal hops from now
                    break

    @staticmethod
    def direction(dr: int, dc: int) -> str:
        """returns the direction in which the change is happening

        Args:
            dr (int): change in row
            dc (int): change in column

        Returns:
            str: the direction string"""
        return ('dl' * (dc < 0) + 'dr' *
                (dc > 0)) * (dr > 0) + ('ul' * (dc < 0) + 'ur' *
                                        (dc > 0)) * (dr < 0)

    def hops(self,
             r: int,
             c: int,
             p: str,
             steps: Optional[tuple[int, int]],
             allowed: Optional[str],
             path: dict = dict(),
             visited: set = set(),
             first: bool = True) -> dict:
        """returns all the hops than can happen from a given position.

        Args:
            r (int): row of the piece
            c (int): column of the piece
            steps (Optional[tuple[int, int]]): valid hops from a given position.
            allowed (Optional[str]): pieces allowed to be hoped over.
            path (dict, optional): container storing the path. Defaults to dict().
            visited (set, optional): visited position. Defaults to set().
            first (bool, optional): True if the hop is first hop. Defaults to True.

        Returns:
            dict: container that contains all the paths"""

        path['coordinate'] = (r, c)  # adding the coordinates

        for d in ['ur', 'ul', 'dr', 'dl']:
            path[d] = path.get(d, None)  # to avoid any error

        for dr, dc in steps:
            # if it is our first hop only then we can hop onto your diagonal neighbours
            if first:
                r_ = r + dr  # r' = r + Δr
                c_ = c + dc  # c' = c + Δc
                if 0 <= r_ < 8 and 0 <= c_ < 8 and self.piece[(r_, c_)] == 'o':
                    path[self.direction(dr, dc)] = {
                        'coordinate': (r_, c_),
                        'ur': None,
                        'ul': None,
                        'dr': None,
                        'dl': None
                    }

            r_ = r + (dr << 1)  # r' = r + 2 * Δr
            c_ = c + (dc << 1)  # c' = c + 2 * Δc

            if (0 <= r_ < 8 and 0 <= c_ < 8 and (r_, c_) not in visited
                    and self.piece[(r + dr, c + dc)] in allowed
                    and self.piece[(r_, c_)] == 'o'):
                path[self.direction(dr, dc)] = {
                    'coordinate': (r_, c_),
                    'ur': None,
                    'ul': None,
                    'dr': None,
                    'dl': None
                }
                visited.add((r_, c_))  # visiting the position
                # exploring more hops
                self.hops(r_, c_, p, steps, allowed,
                          path[self.direction(dr, dc)], visited, False)
        return path

    def deepest_path(self, path: dict) -> Optional[tuple]:
        """returns the deepest path in a tree, if there are more
        than one then select any one randomly

        Args:
            path (dict): tree in a form of nested dictionaries

        Returns:
            Optional[tuple]: list of all nodes that are on the
            deepest path in the tree"""
        # if there is no way to go more
        if path is None:
            return []

        # exploring path in down right direction
        down_right = self.deepest_path(path['dr'])
        # exploring path in down left direction
        down_left = self.deepest_path(path['dl'])
        # exploring path in up right direction
        up_right = self.deepest_path(path['ur'])
        # exploring path in up left direction
        up_left = self.deepest_path(path['ul'])

        length = [len(down_right), len(down_left), len(up_right), len(up_left)]

        deepest = max(length)

        if length[0] == deepest:
            down_right.append(path['coordinate'])
        if length[1] == deepest:
            down_left.append(path['coordinate'])
        if length[2] == deepest:
            up_right.append(path['coordinate'])
        if length[3] == deepest:
            up_left.append(path['coordinate'])

        # randomly chossing a path from all path

        index = [0, 1, 2, 3]
        i = random.choice(index)
        deepest = max(length)
        while length[i] != deepest:
            index.remove(i)
            i = random.choice(index)

        if i == 0:
            return down_right
        elif i == 1:
            return down_left
        elif i == 2:
            return up_right
        else:
            return up_left

    def paths(self, side: str) -> Optional[Optional[tuple[int, int]]]:
        """returns the deepest path of all pieces from side

        Args:
            side (str): the side to find the deepest path of its pieces

        Returns:
            Optional[Optional[tuple[int,int]]]: list of a deepest 
            path possible for each piece"""
        path = []  # container for all deepest paths from all position
        side_parity = {0: False, 1: False}  # setting parity false for new run
        for r, c in product(range(8), range(8)):
            p = self.piece[(r, c)]
            if p.lower() == side:
                # allowed hops and the pieces to hop on
                if p == 'b':
                    steps = [(1, 1), (1, -1)]
                    allowed = ['w']
                elif p == 'w':
                    steps = [(-1, 1), (-1, -1)]
                    allowed = ['b']
                else:
                    steps = self.normal_unit_hops
                    if p == 'B':
                        allowed = ['w', 'W']
                    else:
                        allowed = ['b', 'B']
                hop = self.hops(r, c, p, steps, allowed, dict(), set(), True)
                # appending the deepest path in the path container
                path.append(self.deepest_path(hop))
                # updating the parity
                side_parity[(r + c) % 2] = side_parity[(r + c) % 2] or True
        self.parity[side] = side_parity  # setting the parity
        return path

    def human_move(self) -> Optional[tuple[int, int]]:
        """collects the move human wants to play

        Returns:
            Optional[tuple[int, int]]: list of moves from human"""
        print('Enter your move dear human.')
        cin = input()  # taking inpurt from human
        pos = (int(cin[0]), int(cin[2]))
        move = [pos]
        while True:
            # if human gives q then stops the input and return the collected moves
            cin = input()
            if cin == 'q':
                break
            pos = (int(cin[0]), int(cin[2]))
            move.append(pos)
        return move

    def computer_move(self, side: str) -> Optional[tuple[int, int]]:
        """returns the move computer wants to play

        Args:
            side (str): side which computer playing

        Returns:
            Optional[tuple[int, int]]: list of the position to 
            move piece on the board"""
        path = self.paths(side)
        moves = {}  # dict for all moves
        jump = 0  # depth of the hop
        for k in path:
            if len(k) > jump:
                jump = len(k)
            moves[len(k)] = moves.get(len(k), []) + [k]

        if jump == 2:  # if we are hoping over once then it must be a beating hop
            beating_hop = list(
                filter(lambda k: Checker.L1_norm(k[0], k[1]) == 4, moves[2]))
            if len(beating_hop) > 0:
                moves[2] = beating_hop

        # randomly chossing one hop from the collection of all deepest hops
        move = random.choice(moves[jump])[::-1]
        self.last_move = move[:-1]
        return move

    def start(self) -> None:
        """starts the game"""
        # parity is True right now
        charge = True
        # number of moves are zero
        move_count = 0
        # set that contain all the last move piece had
        self.last_move = []
        # places the pieces on the board
        self.initiate_pieces()
        # count of the pieces
        self.count = {'b': 24, 'w': 24}
        # randomly selecting side for first move
        side = random.choice(['b', 'w'])
        # parity to avoid the color segeration
        self.parity = {'w': {0: True, 1: True}, 'b': {0: True, 1: True}}

        # self.print_screen()

        while self.count['b'] > 0 and self.count['w'] > 0 and charge:
            if side == 'w':
                # human playing from the side
                if self.human:
                    path = self.human_move()
                else:
                    path = self.computer_move('w')
            else:
                # computer playing from the side
                path = self.computer_move('b')
            self.move(path, side)
            # channging the side for next move
            side = 'b' * (side == 'w') + 'w' * (side == 'b')
            move_count += 1
            # checking the parity
            charge = (self.parity['w'][0]
                      and self.parity['b'][0]) or (self.parity['w'][1]
                                                   and self.parity['b'][1])
            # self.print_screen(move_count)
            time.sleep(self.delay)
            if self.clear_screen:
                os.system('clear')
            # printing the board and count

        if not charge:  # if game draws
            print('Game draws :( in ', end='')
            self.stats['draw'] += 1
        elif self.count['b'] == 0:  # if white wins
            print('White wins! in ', end='')

            self.stats['win']['w']['avg moves'] = (
                self.stats['win']['w']['avg moves'] *
                self.stats['win']['w']['count'] +
                move_count) / (self.stats['win']['w']['count'] + 1)

            self.stats['win']['w']['count'] += 1

        else:  # if black wins
            print('Black wins! in ', end='')

            self.stats['win']['b']['avg moves'] = (
                self.stats['win']['b']['avg moves'] *
                self.stats['win']['b']['count'] +
                move_count) / (self.stats['win']['b']['count'] + 1)

            self.stats['win']['b']['count'] += 1

        print(move_count, 'moves.')

    def save(self) -> None:
        """save the stats of the game into a file"""
        # reading the file
        with open("game_stats.json", "r") as file:
            file = json.load(file)

            # updating the average moves of white
            file['win']['w']['avg moves'] = (
                (file['win']['w']['avg moves'] * file['win']['w']['count']) +
                (self.stats['win']['w']['avg moves'] *
                 self.stats['win']['w']['count'])
            ) / (file['win']['w']['count'] + self.stats['win']['w']['count'])

            # updating the average moves of black
            file['win']['b']['avg moves'] = (
                (file['win']['b']['avg moves'] * file['win']['b']['count']) +
                (self.stats['win']['b']['avg moves'] *
                 self.stats['win']['b']['count'])
            ) / (file['win']['b']['count'] + self.stats['win']['b']['count'])

            # updating the win count of white and black
            file['win']['w']['count'] += self.stats['win']['w']['count']
            file['win']['b']['count'] += self.stats['win']['b']['count']

            # updating the draw count
            file['draw'] += self.stats['draw']

        # dumping the stats in the file
        with open("game_stats.json", "w") as outfile:
            json.dump(file, outfile)


game = Checker(human=False, clear_screen=False, delay=0.0)
for game_no in range(10000):
    print(game_no, end=' ')
    game.start()
game.save()
