from queue import PriorityQueue
import time


start_time = time.time()


def start_timer():
    global start_time
    start_time = time.time()


def end_timer():
    global start_time
    return round((time.time() - start_time)*1000)


def dfs(level, start, end):
    stack = [(start, [start])]
    visited = []
    while stack:
        (vertex, path) = stack.pop()
        if vertex not in visited:
            if vertex == end:
                return path, visited
            visited.append(vertex)
            #
            node = [[int(vertex[0]), int(vertex[1] + 1)],
                    [int(vertex[0]), int(vertex[1] - 1)],
                    [int(vertex[0] + 1), int(vertex[1])],
                    [int(vertex[0] - 1), int(vertex[1])]]
            for i in range(4):
                for j in range(2):
                    if node[i][j] == -1:
                        node[i][j] = 20
                    elif node[i][j] == 21:
                        node[i][j] = 0
                if level[node[i][0]][node[i][1]] != 1:
                    stack.append((node[i], path + [node[i]]))


def bfs(level, start, end):
    queue = [[start, [start]]]
    visited = []
    while queue:
        vertex, path = queue.pop(0)
        visited.append(vertex)

        #
        node = [[int(vertex[0] + 1), int(vertex[1])],
                [int(vertex[0] - 1), int(vertex[1])],
                [int(vertex[0]), int(vertex[1] + 1)],
                [int(vertex[0]), int(vertex[1] - 1)]]
        #
        for i in range(4):
            for j in range(2):
                if node[i][j] == -1:
                    node[i][j] = 20
                elif node[i][j] == 21:
                    node[i][j] = 0
            if level[node[i][0]][node[i][1]] != 1:
                if node[i] == end:
                    return path + [end], visited
                else:
                    if node[i] not in visited:
                        visited.append(node[i])
                        queue.append([node[i], path + [node[i]]])


def cost_check(point, end, start):
    # return 1
    return pow(point[0] - end[0], 2) + pow(point[1] - end[1], 2)\
           + (pow(point[0] - start[0], 2) + pow(point[1] - start[1], 2))


def ucs(level, start, end):
    queue = PriorityQueue()
    queue.put((0, [start]))
    visited = []

    while not queue.empty():
        path = queue.get()
        current = path[1][len(path[1]) - 1]

        if current == end:
            return path[1], visited

        cost = path[0]
        node = [[int(current[0]), int(current[1] + 1)],
                [int(current[0]), int(current[1] - 1)],
                [int(current[0] + 1), int(current[1])],
                [int(current[0] - 1), int(current[1])]]
        for i in range(4):
            for j in range(2):
                if node[i][j] == -1:
                    node[i][j] = 20
                elif node[i][j] == 21:
                    node[i][j] = 0
            if level[node[i][0]][node[i][1]] != 1 and node[i] not in visited:
                visited.append(node[i])
                temp = path[1][:]
                temp.append(node[i])
                queue.put((cost + cost_check(node[i], end, start), temp))


def bfs_find_closest_point(level, start):
    queue = [start]
    visited = []
    while queue:
        vertex = queue.pop(0)
        visited.append(vertex)

        #
        node = [[int(vertex[0] + 1), int(vertex[1])],
                [int(vertex[0] - 1), int(vertex[1])],
                [int(vertex[0]), int(vertex[1] + 1)],
                [int(vertex[0]), int(vertex[1] - 1)]]
        #
        for i in range(4):
            for j in range(2):
                if node[i][j] == -1:
                    node[i][j] = 20
                elif node[i][j] == 21:
                    node[i][j] = 0
            if level[node[i][0]][node[i][1]] != 1:
                if level[node[i][0]][node[i][1]] == 2:
                    return node[i]
                else:
                    if node[i] not in visited:
                        visited.append(node[i])
                        queue.append(node[i])


def astar(level, start, end):
    queue = PriorityQueue()
    queue.put((0, [start]))
    visited = []

    while not queue.empty():
        path = queue.get()
        current = path[1][len(path[1]) - 1]

        if current == end:
            return path[1], visited

        cost = path[0]
        node = [[int(current[0]), int(current[1] + 1)],
                [int(current[0]), int(current[1] - 1)],
                [int(current[0] + 1), int(current[1])],
                [int(current[0] - 1), int(current[1])]]
        for i in range(4):
            for j in range(2):
                if node[i][j] == -1:
                    node[i][j] = 20
                elif node[i][j] == 21:
                    node[i][j] = 0
            if level[node[i][0]][node[i][1]] != 1 and node[i] not in visited:
                visited.append(node[i])
                temp = path[1][:]
                temp.append(node[i])
                queue.put((cost_check(node[i], end, start), temp))