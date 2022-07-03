import os
import random
import time
from typing import Optional


class Checker:
    """class to simulate checkers game where computer play against computer"""
    L1_norm = lambda x, y: abs(x[0] - y[0]) + abs(x[1] - y[1])
    normal_hops = {(1, 1), (-1, -1), (1, -1), (-1, 1)}
    count = {'b': 24, 'w': 24}
    tile = {
        'b': '⚫',
        'B': '⬛',
        'w': '⚪',
        'W': '⬜',
        'r': '🟥',
        'y': '🟨',
        'h': '🟩'
    }

    def __init__(self, sleep: float = 0.0, clear_screen: bool = True) -> None:
        """Constructor

        Args:
            sleep (float, optional): number seconds to Sleep. Defaults to 0.
            clear_screen (bool, optional): if True then clear screen after each new move. Defaults to True.
        """
        self.sleep = sleep
        self.clear_screen = clear_screen
        self.last_move = set()
        self.initiate_peices()
        self.parity = {'w': {0: True, 1: True}, 'b': {0: True, 1: True}}

    def initiate_peices(self) -> None:
        """places the peices on the board"""
        self.peice = dict()
        for c in range(8):
            for r in range(3):
                self.peice[(r, c)] = 'b'
            for r in range(3, 5):
                self.peice[(r, c)] = 'o'
            for r in range(5, 8):
                self.peice[(r, c)] = 'w'

    def print_board(self) -> None:
        """print the board on the terminal"""
        time.sleep(self.sleep)
        if self.clear_screen:
            os.system('clear')

        k = 'r'
        for i in range(8):
            for j in range(7):
                k = 'y' if (i + j) % 2 else 'r'
                p = 'h' if (i, j) in self.last_move else self.peice[(i, j)]
                if p == 'o':
                    p = k
                print(self.tile[p], end=' ')

            k = 'y' if (i + 7) % 2 else 'r'
            p = 'h' if (i, 7) in self.last_move else self.peice[(i, 7)]
            if p == 'o':
                p = k

            print(self.tile[p])

    def move(self, pos: Optional[tuple[int, int]], side: str) -> None:
        """moves the peice according to the sequence of position given to

        Args:
            pos (Optional[tuple[int, int]]): sequence of position to move peice on the board
            side (str): peice is from which side
        """

        self.last_move = set()
        opp_side = 'b' if side == 'w' else 'w'
        mid_rc = lambda x, y: ((x[0] + y[0]) >> 1, (x[1] + y[1]) >> 1)

        if len(pos) == 2 and Checker.L1_norm(pos[0], pos[1]) == 2:
            self.peice[pos[1]] = self.peice[pos[0]].upper(
            ) if pos[1][0] == 7 * (side == 'b') else self.peice[pos[0]]

            self.peice[pos[0]] = 'o'
            self.last_move = {pos[0]}

        else:
            i = 0
            while i + 1 < len(pos):
                if (self.peice[pos[i + 1]] == 'o'
                        and Checker.L1_norm(pos[i + 1], pos[i]) == 4
                        and self.peice[mid_rc(pos[i + 1],
                                              pos[i])].lower() == opp_side):

                    self.peice[mid_rc(pos[i + 1], pos[i])] = 'o'

                    if side == 'b':
                        self.peice[pos[i + 1]] = self.peice[pos[i]].upper(
                        ) if pos[i + 1][0] == 7 else self.peice[pos[i]]
                    else:
                        self.peice[pos[i + 1]] = self.peice[pos[i]].upper(
                        ) if pos[i + 1][0] == 0 else self.peice[pos[i]]

                    self.peice[pos[i]] = 'o'
                    self.count[opp_side] -= 1
                    self.last_move.add(pos[i])

                else:
                    break
                i += 1

    @staticmethod
    def direction(dr: int, dc: int) -> str:
        """returns the direction in which the change is happening

        Args:
            dr (int): change in row
            dc (int): change in column

        Returns:
            str: the direction string
        """
        return ('dl' * (dc < 0) + 'dr' *
                (dc > 0)) * (dr > 0) + ('ul' * (dc < 0) + 'ur' *
                                        (dc > 0)) * (dr < 0)

    def hops(self,
             r: int,
             c: int,
             path: dict = dict(),
             visited: set = set(),
             first: bool = True) -> dict:
        """returns all the hops than can happen from a given position.

        Args:
            r (int): row of the peice
            c (int): column of the peice
            path (dict, optional): container storing the path. Defaults to dict().
            visited (set, optional): visited position. Defaults to set().
            first (bool, optional): True if the hop is first hop. Defaults to True.

        Returns:
            dict: container that contains all the paths
        """

        p = self.peice[(r, c)]
        if p == 'b':
            hops = {(1, 1), (1, -1)}
            allowed = {'w'}
        elif p == 'w':
            hops = {(-1, 1), (-1, -1)}
            allowed = {'b'}
        else:
            hops = self.normal_hops
            if p == 'B':
                allowed = {'w', 'W'}
            else:
                allowed = {'b', 'B'}

        path['coordinate'] = (r, c)
        path['cost'] = path.get('cost', 0)

        for d in {'ur', 'ul', 'dr', 'dl'}:
            path[d] = path.get(d, None)

        if first:
            for dr, dc in hops:
                if 0 <= r + dr < 8 and 0 <= c + dc < 8 and self.peice[(
                        r + dr, c + dc)] == 'o':
                    path[self.direction(dr, dc)] = {
                        'coordinate': (r + dr, c + dc),
                        'ur': None,
                        'ul': None,
                        'dr': None,
                        'dl': None,
                        'cost': 1
                    }

        for dr, dc in hops:
            if 0 <= r + 2 * dr < 8 and 0 <= c + 2 * dc < 8 and (
                    r + 2 * dr, c + 2 * dc) not in visited and self.peice[(
                        r + dr, c + dc)] in allowed and self.peice[(
                            r + 2 * dr, c + 2 * dc)] == 'o':
                path[self.direction(dr, dc)] = {
                    'coordinate': (r + 2 * dr, c + 2 * dc),
                    'ur': None,
                    'ul': None,
                    'dr': None,
                    'dl': None,
                    'cost': 2
                }
                visited.add((r + 2 * dr, c + 2 * dc))
                self.hops(r + 2 * dr, c + 2 * dc, path[self.direction(dr, dc)],
                          visited, False)
        return path

    def deepest_path(self, path: dict) -> Optional[tuple]:
        """returns the deepest path in a tree, if there are more 
        than one then select any one randomly

        Args:
            path (dict): tree in a form of nested dictionaries

        Returns:
            Optional[tuple]: list of all nodes that are on the 
            deepest path in the tree
        """
        if path is None:
            return []

        down_right = self.deepest_path(path['dr'])
        down_left = self.deepest_path(path['dl'])
        up_right = self.deepest_path(path['ur'])
        up_left = self.deepest_path(path['ul'])

        length = [len(down_right), len(down_left), len(up_right), len(up_left)]
        deepest = max(length)

        index = [0, 1, 2, 3]
        i = random.choice(index)

        while length[i] != deepest:
            index.remove(i)
            i = random.choice(index)

        if i == 0:
            down_right.append(path['coordinate'])
        if i == 1:
            down_left.append(path['coordinate'])
        if i == 2:
            up_right.append(path['coordinate'])
        if i == 3:
            up_left.append(path['coordinate'])

        index = [0, 1, 2, 3]
        i = random.choice(index)

        while length[i] != deepest:
            index.remove(i)
            i = random.choice(index)

        if i == 0:
            return down_right
        if i == 1:
            return down_left
        if i == 2:
            return up_right
        if i == 3:
            return up_left

    def paths(self, side: str) -> Optional[Optional[tuple[int, int]]]:
        """returns the deepest path of all peices from side

        Args:
            side (str): the side to find the deepest path of its peices

        Returns:
            Optional[Optional[tuple[int,int]]]: list of a deepest 
            path possible for each peice
        """

        path = []
        self.parity[side] = {0: False, 1: False}
        for r in range(8):
            for c in range(8):
                if self.peice[(r, c)].lower() == side:
                    self.parity[side][(r + c) %
                                      2] = self.parity[side][(r + c) %
                                                             2] or True
                    path.append(self.deepest_path(self.hops(r, c)))
        return path

    def computer_move(self, side: str) -> Optional[tuple[int, int]]:
        """returns the move computer wanna play

        Args:
            side (str): side which computer playing

        Returns:
            Optional[tuple[int, int]]: list of the position to 
            move peice on the board
        """
        path = self.paths(side)
        moves = {}
        jump = 0
        for k in path:
            if len(k) > jump:
                jump = len(k)
            moves[len(k)] = moves.get(len(k), []) + [k]

        if jump == 2:
            beating_hop = list(
                filter(lambda k: Checker.L1_norm(k[0], k[1]) == 4, moves[2]))
            if len(beating_hop) > 0:
                moves[2] = beating_hop
        move = random.choice(moves[jump])

        return move[::-1]

    def start(self) -> None:
        """starts the game"""
        self.print_board()
        side = 'w'
        count = 0
        charge = True
        while self.count['b'] > 0 and self.count['w'] > 0 and charge:
            print('\nBlack: ', self.count['b'])
            print('White: ', self.count['w'])
            print('Move:', count)

            path = self.computer_move(side)
            self.move(path, side)
            self.print_board()

            side = 'b' if side == 'w' else 'w'
            count += 1
            charge = (self.parity['w'][0]
                      and self.parity['b'][0]) or (self.parity['w'][1]
                                                   and self.parity['b'][1])

        if not charge:
            print('Game draws :( in ', end='')
        elif self.count['b'] == 0:
            print('White wins! in ', end='')
        else:
            print('Black wins! in ', end='')
        print(count, 'moves.')


game = Checker()
game.start()
