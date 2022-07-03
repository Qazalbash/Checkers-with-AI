import os
import random
import time
from typing import Optional


class Checker(object):
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

    def __init__(self) -> None:
        self.last_move = set()
        self.initiate_peices()

    def initiate_peices(self) -> None:
        self.peice = dict()
        for c in range(8):
            for r in range(3):
                self.peice[(r, c)] = 'b'
            for r in range(3, 5):
                self.peice[(r, c)] = 'o'
            for r in range(5, 8):
                self.peice[(r, c)] = 'w'

    def draw_board(self) -> None:
        # time.sleep(0.5)
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
        return ('dl' * (dc < 0) + 'dr' *
                (dc > 0)) * (dr > 0) + ('ul' * (dc < 0) + 'ur' *
                                        (dc > 0)) * (dr < 0)

    def hops(self,
             r: int,
             c: int,
             p: str,
             path: dict,
             visited: set,
             first: bool = True) -> dict:

        if p == 'b':
            hops = {(1, 1), (1, -1)}
        elif p == 'w':
            hops = {(-1, 1), (-1, -1)}
        else:
            hops = self.normal_hops

        op = 'w' if p.lower() == 'b' else 'b'

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
                        r + dr, c + dc)].lower() == op and self.peice[(
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
                self.hops(r + 2 * dr, c + 2 * dc, p,
                          path[self.direction(dr, dc)], visited, False)
        return path

    def deepest_path(self, path: dict) -> Optional[tuple]:
        if path is None:
            return []

        down_right = self.deepest_path(path['dr'])
        down_left = self.deepest_path(path['dl'])
        up_right = self.deepest_path(path['ur'])
        up_left = self.deepest_path(path['ul'])

        length = [len(down_right), len(down_left), len(up_right), len(up_left)]

        index = [0, 1, 2, 3]
        i = random.choice(index)

        while length[i] != max(length):
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

        while length[i] != max(length):
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

    def possible_paths(self, side: str) -> Optional[dict]:
        path = []
        for r in range(8):
            for c in range(8):
                if self.peice[(r, c)].lower() == side:
                    path.append(
                        self.deepest_path(
                            self.hops(r, c, self.peice[(r, c)], {}, set())))
        return path

    def computer_move(self, side: str) -> Optional[tuple[int, int]]:
        path = self.possible_paths(side)
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
        self.draw_board()
        side = 'w'
        count = 0
        while self.count['b'] > 0 and self.count['w'] > 0:
            print('\nBlack: ', self.count['b'])
            print('White: ', self.count['w'])

            path = self.computer_move(side)
            self.move(path, side)
            self.draw_board()

            side = 'b' if side == 'w' else 'w'
            count += 1

        if self.count['b'] == 0:
            print('White wins! in ', end="")
        else:
            print('Black wins! in ', end='')
        print(count, 'moves.')


b = Checker()
b.start()
