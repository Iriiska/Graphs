"""Практика 4а"""

import sys
sys.setrecursionlimit(10**6)
sys.stdout.reconfigure(encoding='utf-8')


def subtract_row_min(matrix):
    result = []
    for row in matrix:
        max_elem = min(row)
        new_row = [x - max_elem for x in row]
        result.append(new_row)
    return result


def subtract_col_min(matrix):
    result = [row[:] for row in matrix]
    rows = len(matrix)
    cols = len(matrix[0])

    for j in range(cols):
        min_elem = matrix[0][j]
        for i in range(rows):
            if matrix[i][j] < min_elem:
                min_elem = matrix[i][j]
        for i in range(rows):
            result[i][j] = matrix[i][j] - min_elem

    return result

def try_kuhn(u, adj, match, used):
    for v in adj[u]:
        if used[v]:
            continue
        used[v] = True
        if match[v] == -1 or try_kuhn(match[v], adj, match, used):
            match[v] = u
            return True
    return False


def kuhn(L, R, adj):
    match = [-1] * R
    answer = 0
    for u in range(L):
        used = [False] * R
        if try_kuhn(u, adj, match, used):
            answer += 1
    return answer, match

def mark_rows(v, matrix, right, left):
    for i in range(len(matrix[v])):
        if matrix[v][i] == 0:
            if i not in right:
                right.append(i)
                mark_columns(i, matrix, right, left)
    return right, left

def mark_columns(v, matrix, right, left):
    for i in range(len(matrix)):
        if matrix[i][v] == 0:
            if i not in left:
                left.append(i)
                mark_rows(i, matrix, right, left)
    return right, left

def matrix_change(matrix, left, right):
    # Для быстрой проверки принадлежности преобразуем в множества
    left_set = set(left)
    right_set = set(right)

    min = None

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if (i in left_set) and not (j in right_set):
                if min is None or matrix[i][j] < min:
                    min = matrix[i][j]

    for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if (i in left_set) and not (j in right_set):
                    matrix[i][j] -= min
                if not (i in left_set) and (j in right_set):
                    matrix[i][j] += min
    return matrix

if __name__ == "__main__":
    matrix = [
        [11, 7, 8, 9, 11],
        [10, 12, 8, 8, 10],
        [10, 12, 13, 9, 11],
        [7, 12, 7, 5, 9],
        [12, 5, 6, 11, 8]
    ]
    task = "min" # можно заменить на max
    size = 0

    if task == "min":
        new_matrix = matrix
    else:
        max = max(max(row) for row in matrix)
        new_matrix = [[max - x for x in row] for row in matrix]
        print()
        print("Макс - матрица:")
        for row in new_matrix:
            print(row)

    while size != len(new_matrix):
        new_matrix = subtract_row_min(new_matrix)
        print()
        print("После вычитания минимума строки:")
        for row in new_matrix:
            print(row)

        print()
        new_matrix = subtract_col_min(new_matrix)
        print("После вычитания минимума столбца:")
        for row in new_matrix:
            print(row)

        adj = [[] for _ in range(len(matrix))]
        for i in range(len(matrix)):
            for j in range(len(matrix)):
                if new_matrix[i][j] == 0:
                    adj[i].append(j)

        size, match = kuhn(len(new_matrix), len(new_matrix), adj)

        print()
        print("Список смежности (левая вершина: правые вершины):")
        for u in range(len(new_matrix)):
            print(f"{u}: {adj[u]}")

        print()
        print("Максимальное паросочетание:", size)
        print("Пары (левая — правая):")
        for v in range(len(new_matrix)):
            if match[v] != -1:
                print(f"{match[v]} — {v}")
        if size != len(new_matrix):
            right = []
            left = []
            for v in range(len(new_matrix)):
                if match[v] == -1:
                    left.append(v)
            
            for v in left:
                right, left = mark_rows(v, new_matrix, right, left)
            print(left, right)
            new_matrix = matrix_change(new_matrix, left, right)

            print()
            print("Вычитания из строк и прибавления к столбцам")
            for row in new_matrix:
                print(row)
        else:

            weight = 0
            for v in range(len(new_matrix)):
                weight += matrix[match[v]][v]

            print()
            print("Оптимальный вес: ", weight)
        
        

