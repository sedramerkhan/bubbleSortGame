import copy
import time
from queue import PriorityQueue
import sys
from bottles import Bottles


class Game:

    def __init__(self, max_color, max_bottle, max_length):
        self.bottles = Bottles(max_color, max_bottle, max_length, None)
        self.max_color = max_color
        self.max_bottle = max_bottle
        self.max_length = max_length

        self.start_time = time.time()

        # sys.setrecursionlimit(10000)

    def generate_bottles(self):
        return self.bottles.generate_bottles()

    def move(self, s: int, d: int):
        return self.bottles.move(s, d)

    def check_lose(self):
        states = self.bottles.next_states()
        # print("\n", states, "\n")
        if len(states) == 0:
            return True
        return False

        # def check_win(self):
        #     return True if self.bottles.check_colors_bottles() else False
        #
        # def available_move(self, s: int, d: int):
        #     temp = copy.deepcopy(self.bottles)
        #     temp.update_bottles(s, d)
        #     print(temp)
        #     return temp
        #
        # def next_states(self):
        #     new_states = []
        #     print("Show Next States")
        #     states = self.bottles.next_states()
        #     for i, (s, d) in enumerate(states):
        #         print(f"________{i + 1}_______move {s + 1} to {d + 1}")
        #         new_states.append(self.available_move(s, d))
        #     return new_states
        #     print("**********************")

    def available_move(self, b: Bottles, s: int, d: int):
        if b is None:
            b = self.bottles
        temp = b.deepcopy()
        # temp = b.__deepcopy__()
        temp.parent = b
        temp.update_bottles(s, d)

        if b.parent is Bottles:
            if b.parent.bottles == temp.bottles:
                return None
        else:
            return temp

    def next_states(self, b=None):
        if b is None:
            b = self.bottles
        new_states = []
        # print("Show Next States")
        states = b.next_states()
        for i, (s, d) in enumerate(states):
            # print(f"________{i + 1}_______move {s + 1} to {d + 1}")

            if self.available_move(b, s, d) is not None:
                new_states.append(self.available_move(b, s, d))
        return new_states
        # print("**********************")

    def check_win(self, b: Bottles = None):
        if b is None:
            b = self.bottles
        return True if b.check_colors_bottles() else False

    def bfs(self):
        self.start_time = time.time()
        visited = [self.bottles]
        queue = [self.bottles]

        while queue:
            m = queue.pop(0)
            if self.check_win(m):
                self.print_path("BFS", m, visited)
                return m

            # print("queue len: ",len(queue),"  visited len ",len(visited))
            for neighbour in self.next_states(m):
                if neighbour not in visited and neighbour not in queue:
                    visited.append(neighbour)
                    queue.append(neighbour)
        return None

    def dfs(self):
        self.start_time = time.time()
        visited = []
        stack = [self.bottles]

        while stack:
            m = stack.pop()

            if self.check_win(m):
                self.print_path("DFS", m, visited)
                return m

            if m in visited:
                continue
            visited.append(m)

            for neighbour in self.next_states(m):
                if neighbour not in visited and neighbour not in stack:
                    stack.append(neighbour)

        return None

    def ucs(self):
        self.start_time = time.time()
        visited = []
        queue = [(0, self.bottles)]

        while queue:
            queue = sorted(queue, key=lambda x: x[0], reverse=True)
            cost, node = queue.pop()

            if node not in visited:
                visited.append(node)

                if self.check_win(node):
                    self.print_path("UCS", node, visited)
                    return node

                for i in self.next_states(node):
                    if i not in visited:
                        total_cost = cost + 1
                        queue.append((total_cost, i))
        return None

    def A_star(self):
        self.start_time = time.time()
        visited = [self.bottles]
        queue = [(self.bottles.heuristic(), self.bottles)]
        cost = [self.bottles.heuristic()]
        cost[visited.index(self.bottles)] = self.bottles.heuristic()

        while queue:
            node_cost, node = queue.pop()

            if self.check_win(node):
                self.print_path("A star", node, visited)
                return node

            for i in self.next_states(node):
                i_cost = node_cost - node.heuristic() + i.heuristic()
                if i not in visited:
                    queue.append((i_cost, i))
                    visited.append(i)
                    cost.append(i_cost)
                    continue

                if i_cost + 1 < cost[visited.index(i)]:
                    queue.append((i_cost, i))
                    cost[visited.index(i)] = i_cost
        return None

        # self.start_time = time.time()
        # visited = []
        # queue = [(0, self.bottles)]
        #
        # while queue:
        #     queue = sorted(queue, key=lambda x: x[0], reverse=True)
        #     cost, node = queue.pop()
        #
        #     if node not in visited:
        #         visited.append(node)
        #
        #         if self.check_win(node):
        #             self.print_path("A star", node, visited)
        #             return node
        #         node_cost = cost - node.heuristic()
        #         for i in self.next_states(node):
        #             if i not in visited:
        #                 total_cost = node_cost + 1 + i.heuristic()
        #                 queue.append((total_cost, i))
        # return None

    def hill(self):
        self.start_time = time.time()
        queue = [self.bottles]

        while queue:
            node = queue.pop()

            if self.check_win(node):
                self.print_path("Hill Climbing", node, None)
                return node

            l = []
            for i in self.next_states(node):
                l.append((i.heuristic(), i))
            l = sorted(l, key=lambda x: x[0])
            queue.append(l.pop()[1])

        return None

    def show_path(self, node: Bottles):
        if node.parent is None:
            print(node)
            return
        self.show_path(node.parent)
        print(f"_________{self.i}___________")
        self.i += 1
        print(node)

    def print_path(self, algorithm, node, visited):
        # print("                     *********************win**********************\n")
        print(f"                     *****************Show Path In {algorithm}**********************")
        print("--- %s seconds ---" % (time.time() - self.start_time))

        self.i = 1
        self.show_path(node)
        print(f"total move = {self.i}", end="        ")
        if visited is None:
            print("\n\n")
        else:
            print(f"visited nodes = {len(visited)}\n\n")

    # def heuristic(self,a, b):
    #     # Manhattan distance on a square grid
    #     return abs(a.x - b.x) + abs(a.y - b.y)
