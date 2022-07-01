from typing import Optional


class Checker(object):

    difference = lambda x, y: (x[0] - y[0], x[1] - y[1])
    L1_norm = lambda x, y: abs(x[0] - y[0]) + abs(x[1] - y[1])

    def __init__(self) -> None:
        # self.turn = np.random.choice(['w', 'b'], p=[0.5, 0.5])
        # self.initiate_board()
        self.initiate_peices()
        self.count = {'b': 24, 'w': 24}
        self.tile = {
            "b": "⚫",
            "B": "⬛",
            "w": "⚪",
            "W": "⬜",
            "r": "🟥",
            "y": "🟨",
            "h": "🟩"
        }
        self.last_move = set()

    def initiate_board(self) -> None:
        steps = {(1, 1), (-1, -1), (1, -1), (-1, 1)}
        self.board = {}
        for r in range(8):
            for c in range(8):
                self.board[(r, c)] = {(r + dr, c + dc)
                                      for dr, dc in steps
                                      if 0 <= r + dr <= 7 and 0 <= c + dc <= 7}

    def initiate_peices(self) -> None:
        self.peice: dict[tuple:str] = {}
        for c in range(8):
            for r in range(3):
                self.peice[(r, c)] = 'b'
            for r in range(3, 5):
                self.peice[(r, c)] = 'o'
            for r in range(5, 8):
                self.peice[(r, c)] = 'w'

    def draw(self) -> None:
        k = 'r'
        print(" ", end=" ")
        for header in range(0, 7):
            print(header, end="  ")
        print(7)
        for i in range(8):
            print(i, end=" ")
            for j in range(7):
                k = 'y' if (i + j) % 2 else 'r'
                p = self.peice[(i, j)]
                if p == 'o':
                    p = k
                if (i, j) in self.last_move:
                    p = 'h'
                print(self.tile[p], end=" ")
            p = self.peice[(i, 7)]
            k = 'y' if (i + 7) % 2 else 'r'
            if p == 'o':
                p = k
            if (i, 7) in self.last_move:
                p = 'h'
            print(self.tile[p])

    def move(self, pos: Optional[tuple[int, int]], side: str) -> None:

        self.last_move = set()

        opp_side = 'b' if side == 'w' else 'w'

        if self.peice[pos[0]] == side or self.peice[pos[0]] == side.upper():

            if len(pos) == 2 and Checker.L1_norm(pos[0], pos[1]) == 2:
                self.peice[pos[1]] = self.peice[
                    pos[0]] if pos[1][0] else self.peice[pos[0]].upper()
                self.peice[pos[0]] = 'o'
                self.last_move = set(pos[:-1])

            else:
                mid_rc = lambda x, y: ((x[0] + y[0]) >> 1, (x[1] + y[1]) >> 1)

                for i in range(len(pos) - 1):
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
                        break
                self.last_move.remove(pos[i + 1])
            print(self.last_move)

    def start(self) -> None:
        self.draw()
        side = 'w'

        while self.count['b'] > 0 and self.count['w'] > 0:
            print("\nBlack: ", self.count['b'])
            print("White: ", self.count['w'])
            print(
                f"\nEnter the position of the {side} piece you want to move: ")

            path = []

            while True:

                cin = input()
                if cin == 'q':
                    break
                pos = cin.split()
                pos = (int(pos[0]), int(pos[1]))
                path.append(pos)

            self.move(path, side)
            self.draw()

            side = 'b' if side == 'w' else 'w'

        if self.count['b'] == 0:
            print("White wins!")
        else:
            print("Black wins!")


b = Checker()

s = [(1, 4), (0, 3)]
for i in s:
    b.peice[i] = 'o'

s = [(4, 5)]
for i in s:
    b.peice[i] = 'b'
b.start()
