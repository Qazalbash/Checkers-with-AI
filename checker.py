import random
from pprint import pprint
from typing import Optional
import os
import time


class Checker(object):
    difference = lambda x, y: (x[0] - y[0], x[1] - y[1])
    L1_norm = lambda x, y: abs(x[0] - y[0]) + abs(x[1] - y[1])
    normal_hops = {(1, 1), (-1, -1), (1, -1), (-1, 1)}
    double_hops = {(2, 2), (-2, -2), (2, -2), (-2, 2)}
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
        self.black_path = list()
        self.white_path = list()

    def initiate_peices(self) -> None:
        self.peice = dict()
        for c in range(8):
            for r in range(3):
                self.peice[(r, c)] = 'b'
            for r in range(3, 5):
                self.peice[(r, c)] = 'o'
            for r in range(5, 8):
                self.peice[(r, c)] = 'w'

    def draw(self) -> None:
        time.sleep(1)
        os.system('clear')
        k = 'r'
        print(' ', end=' ')

        for header in range(0, 7):
            print(header, end='  ')
        print(7)

        for i in range(8):
            print(i, end=' ')
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

        if self.peice[pos[0]].lower() == side:
            if len(pos) == 2 and (Checker.L1_norm(pos[0], pos[1]) == 2
                                  or Checker.L1_norm(pos[0], pos[1]) == 4):
                self.peice[pos[1]] = self.peice[
                    pos[0]] if pos[1][0] else self.peice[pos[0]].upper()
                self.peice[pos[0]] = 'o'
                self.last_move = {pos[0]}
                if Checker.L1_norm(pos[0], pos[1]) == 4:
                    self.peice[mid_rc(pos[0], pos[1])] = 'o'

            else:
                i = 0
                while i + 1 < len(pos):
                    if (self.peice[pos[i + 1]] == 'o'
                            and Checker.L1_norm(pos[i + 1], pos[i]) == 4
                            and self.peice[mid_rc(
                                pos[i + 1], pos[i])].lower() == opp_side):

                        self.peice[mid_rc(pos[i + 1], pos[i])] = 'o'

                        self.peice[pos[i + 1]] = self.peice[pos[i]] if pos[
                            i + 1][0] else self.peice[pos[i]].upper()

                        self.peice[pos[i]] = 'o'
                        self.count[opp_side] -= 1
                        self.last_move.add(pos[i])
                        self.last_move.add(pos[i + 1])

                    else:
                        self.last_move.remove(pos[i + 1])
                        break
                    i += 1

    def start(self) -> None:
        self.draw()
        side = 'w'

        count = 0

        while self.count['b'] > 0 and self.count['w'] > 0 and count < 20:
            print('\nBlack: ', self.count['b'])
            print('White: ', self.count['w'])
            # print(
            #     f'\nEnter the position of the {side} piece you want to move: ')
            if side == 'w':
                # cin = input()
                # path = [(int(cin[0]), int(cin[2]))]
                # while True:
                #     cin = input()
                #     if cin == 'q':
                #         break
                #     pos = (int(cin[0]), int(cin[2]))
                #     path.append(pos)
                path = self.computer_move('w')
            else:
                path = self.computer_move('b')

            self.move(path, side)
            self.draw()
            side = 'b' if side == 'w' else 'w'
            count += 1

        if self.count['b'] == 0:
            print('White wins!')
        else:
            print('Black wins!')

    def possible_paths(self, side: str) -> Optional[dict]:
        path = []
        for r in range(8):
            for c in range(8):
                if self.peice[(r, c)].lower() == side:
                    path.append(self.hops(r, c, self.peice[(r, c)], {}, set()))
        return path

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

    # def find_paths(self, side: str) -> list:
    #     paths = []
    #     for r in range(8):
    #         for c in range(8):
    #             if self.peice[(r, c)].lower() == side:
    #                 paths.append(
    #                     self.dfs(r, c, self.peice[(r, c)], [], set(), []))
    #     return paths

    # def dfs(self,
    #         r: int,
    #         c: int,
    #         p: str,
    #         path: list,
    #         visited: set,
    #         first: bool = True) -> list:
    #     if p == 'b':
    #         hops = {(1, 1), (1, -1)}
    #     elif p == 'w':
    #         hops = {(-1, 1), (-1, -1)}
    #     else:
    #         hops = self.normal_hops

    #     op = 'w' if p.lower() == 'b' else 'b'

    #     path.append((r, c))
    #     visited.add((r, c))

    #     for dr, dc in hops:
    #         if 0 <= r + dr < 8 and 0 <= c + dc < 8 and self.peice[(
    #                 r + dr, c + dc)] == 'o' and first:
    #             path.append((r + dr, c + dc))

    #         elif 0 <= r + 2 * dr < 8 and 0 <= c + 2 * dc < 8 and (
    #                 r + 2 * dr, c + 2 * dc) not in visited and self.peice[(
    #                     r + dr, c + dc)].lower() == op and self.peice[(
    #                         r + 2 * dr, c + 2 * dc)] == 'o':
    #             path = self.dfs(r + 2 * dr, c + 2 * dc, p, path, visited,
    #                             False)

    #     return path

    def best_path(self, path: dict, path_list: list, path_cost: int) -> list:
        if path['ur'] == None and path['ul'] == None and path[
                'dr'] == None and path['dl'] == None:

            return path_list + [path['coordinate']], path_cost + path['cost']
        else:
            # path_list.append(path['coordinate'])
            # path_cost += path['cost']
            if path['ur'] != None:
                return self.best_path(path['ur'],
                                      path_list[:] + [path['coordinate']],
                                      path_cost + path['cost'])
            if path['ul'] != None:
                return self.best_path(path['ul'],
                                      path_list[:] + [path['coordinate']],
                                      path_cost + path['cost'])
            if path['dr'] != None:
                return self.best_path(path['dr'],
                                      path_list[:] + [path['coordinate']],
                                      path_cost + path['cost'])
            if path['dl'] != None:
                return self.best_path(path['dl'],
                                      path_list[:] + [path['coordinate']],
                                      path_cost + path['cost'])

    def computer_move(self, side: str) -> Optional[tuple[int, int]]:
        path = [self.best_path(i, [], 0) for i in self.possible_paths(side)]
        # pprint(path)

        moves = {2: [], 1: [], 0: []}

        for k, v in path:
            moves[v] = moves.get(v, []) + [k]

        if moves[2] != []:
            move = random.choice(moves[2])
        elif moves[1] != []:
            move = random.choice(moves[1])
        elif moves[0] != []:
            move = random.choice(moves[0])

        return move


b = Checker()
b.start()
