def is_valid_placement(board, row, col, number):
    if number in board[row]:
        return False
    if number in [board[y][col] for y in range(9)]:
        return False
    x, y = row//3*3, col//3*3
    if number in [board[i][j] for i in range(x, x+3) for j in range(y, y+3)]:
        return False
    return True


def limit_recursion(limit):
    def inner(func):
        func.count = 0
        def wrapper(*args, **kwargs):
            func.count += 1
            if func.count < limit:
                result = func(*args, **kwargs)
            else:
                result = None
                raise Exception("Invalid Board")
            func.count -= 1
            return result
        return wrapper
    return inner


@limit_recursion(limit=20)
def solver(board, row=0, col=0):
    if row == 9:
        return True
    if col == 9:
        return solver(board, row=row + 1, col=0)
    if board[row][col] != 0:
        return solver(board, row=row, col=col + 1)
    else:
        for num in range(1, 10):
            if is_valid_placement(board, row, col, num):
                board[row][col] = num
                if solver(board, row, col + 1):
                    return True
                board[row][col] = 0
        return False


def print_grid(board):
    for row in board:
        print(row)


def solve(board):
    if solver(board):
        return board
    else:
        return -1

if __name__ == '__main__':
    grid =[
            [7, 8, 0, 4, 0, 0, 1, 2, 0],
            [6, 0, 0, 0, 7, 5, 0, 0, 9],
            [0, 0, 0, 6, 0, 1, 0, 7, 8],
            [0, 0, 7, 0, 4, 0, 2, 6, 0],
            [0, 0, 1, 0, 5, 0, 9, 3, 0],
            [9, 0, 4, 0, 6, 0, 0, 0, 5],
            [0, 7, 0, 3, 0, 0, 0, 1, 2],
            [1, 2, 0, 0, 0, 7, 4, 0, 0],
            [0, 4, 9, 2, 0, 6, 0, 0, 7]
        ]
    solver(grid)
    print_grid(grid)



