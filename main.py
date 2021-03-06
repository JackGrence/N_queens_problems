import time
import random


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def main():
    global restart_time
    find_correct_board = False
    while not find_correct_board:
        board, queens_pos = get_board()
        print_board(board)

        next_board = get_next_board(board)
        while next_board is not None:
            board = next_board
            print_board(board)
            next_board = get_next_board(board)

        conflict_len = len(get_conflict(board))
        if conflict_len == 0:
            find_correct_board = True
            break
        restart_time += 1

    global debug_print
    debug_print = True
    print_board(board)
    print("restart:", restart_time)


def get_next_board(board):
    queens_pos = get_queens_pos(board)
    conflict_pos = get_conflict(board, queens_pos)
    if len(conflict_pos) == 0:
        return None

    has_smaller = False
    min_conflict_board = board
    min_conflict_num = len(conflict_pos)
    for i in range(n):
        for j in range(i + 1, n):
            tmp_board = [i[:] for i in board]
            tmp_board[i], tmp_board[j] = tmp_board[j], tmp_board[i]
            conflict_pos = get_conflict(tmp_board)
            if len(conflict_pos) < min_conflict_num:
                has_smaller = True
                min_conflict_num = len(conflict_pos)
                min_conflict_board = [i[:] for i in tmp_board]

    return min_conflict_board if has_smaller else None


def get_board():
    board = [[0 for i in range(n)] for j in range(n)]
    queens_pos = [i for i in range(n)]
    random.shuffle(queens_pos)
    for i, element in enumerate(queens_pos):
        board[i][element] = 1
    return board, None


def get_conflict(board, queens_pos=None):
    if queens_pos is None:
        queens_pos = get_queens_pos(board)

    chk_ary = [[0 for i in range(n)] for j in range(n)]
    conflict_pos = []
    for ind, pos_i in enumerate(queens_pos[:-1]):
        for pos_j in queens_pos[ind + 1:]:
            row = abs(pos_i[0] - pos_j[0])
            col = abs(pos_i[1] - pos_j[1])
            if row == 0 and col == 0:
                continue
            if row == 0 or col == 0 or row == col:
                chk_ary[pos_i[0]][pos_i[1]] = 1
                chk_ary[pos_j[0]][pos_j[1]] = 1
    conflict_pos = get_queens_pos(chk_ary)
    return conflict_pos


def is_conflict(pos, board):
    for direct in directions:
        row = pos[0] + direct[0]
        col = pos[1] + direct[1]
        while row >= 0 and row < n and col >= 0 and col < n:
            if board[row][col]:
                return True
            row += direct[0]
            col += direct[1]
    return False


def get_queens_pos(board):
    queens_pos = []
    for row_ind, row in enumerate(board):
        for col_ind, col in enumerate(row):
            if col == 1:
                queens_pos.append([row_ind, col_ind])
    return queens_pos


def print_board(board):
    if not debug_print:
        return
    time.sleep(sleep_time)
    print_str = ''
    for i in board:
        for j in i:
            s = '▮ '
            if j == 1:
                s = bcolors.OKGREEN + s + bcolors.ENDC
            print_str += s
        print_str += '\n'
    print(print_str)


if __name__ == '__main__':
    directions = [[-1, 0], [1, 0], [0, -1], [0, 1],
                  [-1, 1], [1, 1], [-1, -1], [1, -1]]

    n = 20  # n queens
    sleep_time = 0
    debug_print = True
    restart_time = 0
    main()
