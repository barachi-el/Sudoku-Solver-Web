from flask import Flask, render_template, request

app = Flask(__name__)

def board_disp(b):
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print('- - - - - - - - - - - - - - - - ')
        for j in range(len(b[i])):
            if j % 3 == 0 and j != 0:
                print(" | ", end=" ")
            if j == 8:
                print(b[i][j])
            else:
                print(str(b[i][j]) + ' ', end=" ")

def search_empty(b):
    for i in range(len(b)):
        for j in range(len(b[0])):
            if b[i][j] == 0:
                return (i, j)
    return None

def check(b, n, p):
    for i in range(len(b[0])):
        if (b[p[0]][i] == n and p[1] != i):
            return False
    for i in range(len(b)):
        if b[i][p[1]] == n and p[0] != i:
            return False
    b_x = p[1]//3
    b_y = p[0]//3
    for i in range(b_y*3, b_y*3 + 3):
        for j in range(b_x*3, b_x*3+3):
            if b[i][j] == n and (i,j) != p:
                return False
    return True

def solve(b):
    find = search_empty(b)
    if not find:
        return True
    else:
        row, col = find
    for i in range(1, 10):
        if check(b, i, (row, col)):
            b[row][col] = i
            if solve(b):
                return True
            b[row][col] = 0
    return False

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        board = []
        for i in range(9):
            row = request.form[f"row_{i + 1}"]
            board.append([int(num) for num in row])

        solved = solve(board)  # Checks if the Sudoku puzzle is solvable.

        return render_template("index.html", board=board, solved=solved)

    return render_template("index.html", board=None, solved=False)
