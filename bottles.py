
import random


from utils import COLORS_CONSOLE


class Bottles:

    def __init__(self, max_color, max_bottle, max_length, parent):
        self.max_color = max_color
        self.max_bottle = max_bottle
        self.max_length = max_length
        self.bottles = []

        self.parent = parent

    """Check"""

    def is_empty(self, b):
        return True if len(self.bottles[b]) == 0 else False

    def check_size_bottle(self, b: int):
        return True if len(self.bottles[b]) < self.max_length else False

    def check_last_elements_colors(self, s, d):
        return True if not self.is_empty(d) and self.bottles[s][-1] != self.bottles[d][-1] else False

    def check_colors_bottles(self):
        for b in range(len(self.bottles)):
            if self.is_empty(b):
                continue
            if not self.check_colors_bottle(b):
                return False
        return True

    def check_colors_bottle(self, b):
        bottle = self.bottles[b]
        if self.check_size_bottle(b):
            return False
        for i in range(1, len(bottle)):
            if bottle[i] != bottle[i - 1]:
                return False
        return True

    """Update"""

    def update_bottles(self, s, d):
        ball = self.bottles[s].pop()
        self.bottles[d].append(ball)

    """Move"""

    def move(self, s, d):
        can_move = self.can_move(s, d)
        if can_move == 4:
            self.update_bottles(s, d)
            print(f"____move {s + 1} to {d + 1}")
            print(self)
        return can_move

    """Generate"""

    def generate_bottles(self):
        dic = {}
        self.bottles = []
        for _ in range(self.max_bottle):
            bottle = []
            j = 0
            while j < self.max_length:
                rand = random.randrange(0, self.max_color)
                dic[rand] = dic.get(rand, 0) + 1
                j += 1
                if dic[rand] <= self.max_length:
                    bottle.append(rand)
                else:
                    j -= 1
            self.bottles.append(bottle)
            print(bottle)
        # self.bottles = [[0, 0, 0, 1], [1, 1, 0, 1], [2, 2, 2, 2], [3, 3, 3, 4], [4, 4, 4, 3]]
        # self.bottles = [[0,0,1,1],[0,0,1,1],[2,2,2,2]]
        self.bottles.extend([[], []])

        # self.__str__()
        print(self)
        return self.bottles

    def can_move(self, start: int, end: int):
        if self.is_empty(start):
            return 0
        if self.check_colors_bottle(start):
            return 2
        if not self.check_size_bottle(end):
            return 1
        if self.check_last_elements_colors(start, end):
            return 3
        return 4

    def next_states(self):
        states = []
        length = len(self.bottles)
        for i in range(length):
            for j in range(i + 1, length):
                if self.can_move(i, j) == 4:
                    states.append((i, j))

        for i in range(length)[::-1]:
            for j in range(i - 1, -1, -1):
                if self.can_move(i, j) == 4:
                    states.append((i, j))
        return states

    # def heuristic(self):
    #     count = 0
    #     for b in range(len(self.bottles)):
    #         if not self.check_size_bottle(b) and self.check_colors_bottle(b):
    #             count += 1
    #
    #     return self.max_bottle - 2 - count

    def heuristic(self) -> int:
        count: int = 0
        for b in self.bottles:
            if len(b) < 2:
                continue
            for i in range(1, len(b)):
                if b[i - 1] == b[i]:
                    count += 1
                else:
                    break
        # print(count,end=" ")
        return count

    def __eq__(self, other):
        return self.bottles == other.bottles

    def deepcopy(self):
        b = Bottles(self.max_color, self.max_bottle, self.max_length, self)
        temp = []
        for bottle in self.bottles:
            t = []
            for bo in bottle:
                t.append(bo)
            temp.append(t)
        b.bottles = temp
        # b.bottles = copy.deepcopy(self.bottles)
        return b

    # def __hash__(self):
    #     c = 0
    #     for bottle in self.bottles:
    #         for b in range(len(bottle)):
    #             c += (bottle[b] + 1) * b
    #     return c

    def __str__(self):
        print()
        # for i in reversed(range(self.max_length)):
        for i in range(self.max_length)[::-1]:
            print(end='                ')
            for bottle in self.bottles:
                if i < len(bottle):
                    color = COLORS_CONSOLE[bottle[i]]
                    print('|{:^8}|'.format(color), end='   ')
                else:
                    print('|{:8}|'.format(''), end="   ")
            print()
        return ""


"""
[2, 2, 3, 1]
[3, 3, 0, 0]
[2, 3, 1, 1]
[1, 0, 2, 0]
[4, 4, 4, 4]

[3, 4, 2, 3]
[0, 4, 4, 2]
[1, 2, 3, 1]
[2, 4, 0, 0]
[3, 0, 1, 1]
"""
