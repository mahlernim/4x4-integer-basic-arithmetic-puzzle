from flask import Flask, render_template, request
import random

application = Flask(__name__)

# 격자 생성 (크기는 size 값으로 변경 가능)
def generate_grid(size=4):
    numbers = list(range(1, size * size + 1))
    random.shuffle(numbers)

    grid = [[0] * size for _ in range(size)]
    for i in range(size):
        for j in range(size):
            grid[i][j] = numbers.pop()

    return grid

# 셀과 셀 사이의 자연수 사칙연산 생성
def calculate_operations(grid, prob):
    size = len(grid)
    # 가로세로 방향 나눠 연산을 각각 생성
    horizontal_ops = [["" for _ in range(size - 1)] for _ in range(size)]
    vertical_ops = [["" for _ in range(size)] for _ in range(size - 1)]

    for i in range(size):
        for j in range(size):
            if j < size - 1:
                horizontal_ops[i][j] = choose_operation(grid[i][j], grid[i][j + 1], prob)
            if i < size - 1:
                vertical_ops[i][j] = choose_operation(grid[i][j], grid[i + 1][j], prob)

    return horizontal_ops, vertical_ops

# 두 셀 값을 주어주면 그 사이의 자연수 사칙연산을 생성
def choose_operation(a, b, prob=0.7):
    if a % b == 0 and random.random() < prob:
        op = f"÷{a // b}"
    elif b % a == 0 and random.random() < prob:
        op = f"×{b // a}"
    elif a > b:
        op = f"-{a - b}"
    else:
        op = f"+{b - a}"
    return op

# 퍼즐 출력 (hide_numbers=True가 되면 답을 숨김)
def html_puzzle(grid, horizontal_ops, vertical_ops, hide_numbers=False, prob=0.5):
    html = "<table>"
    size = len(grid)
    flat_grid = [i for row in grid for i in row]
    mapping = {flat_grid[i]:chr(65 + i) for i in range(len(flat_grid))}
    for i in range(size):
        row = ""
        for j in range(size):
            if hide_numbers:
                row += f"<td class='num'>{mapping[grid[i][j]]}</td>"
            else:
                row += f"<td class='num'>{grid[i][j]}</td>"
            if j < size - 1:
                op = horizontal_ops[i][j]
                if hide_numbers and random.random() < prob:
                    op =  op.strip()[0] + mapping[int(op.strip()[1:])]
                row += f"<td class='ver'><span>{op}</span></td>"
        html += f"<tr>{row}</tr>"
        if i < size - 1:
            row = ""
            for j in range(size):
                op = vertical_ops[i][j]
                if hide_numbers and random.random() < prob:
                    op = op.strip()[0] + mapping[int(op.strip()[1:])]
                row += f"<td class='hor'><span>{op}</span></td>"
                if j < size - 1:
                    row += "<td class='nil'></td>"
            html += f"<tr>{row}</tr>"
    html += "</table>"
    return html

def count_muldiv(horizontal_ops, vertical_ops):
  ops = "".join([i for row in horizontal_ops for i in row] + [i for row in vertical_ops for i in row])
  return ops.count('×')+ops.count('÷')


# 퍼즐 생성, 정답출력, 퍼즐출력
@application.route('/')
def index():
    if len(request.args.to_dict()) == 0:
        return render_template("menu.html")
    
    else:
        # 변수처리
        size = int(request.args.to_dict()['size'])
        if size < 3 or size > 5:
            size = 4
        difficulty = int(request.args.to_dict()['difficulty'])
        if difficulty < 1 or difficulty > 3:
            difficulty = 2
        prob1 = [1, 1, 0.85, 0.7][difficulty]
        prob2 = [0.5, 0.5, 0.7, 0.9][difficulty]
        size = int(size)
        if size < 3 or size > 5:
            size = 4

        # 생성시작
        puzzle = ""
        muldiv = 0
        # 승제가 충분하도록
        while(muldiv < size + 1):
          grid = generate_grid(size)
          horizontal_ops, vertical_ops = calculate_operations(grid, prob1)
          muldiv = count_muldiv(horizontal_ops, vertical_ops)
        puzzle += "<div class='puzzle'>"
        puzzle += html_puzzle(grid, horizontal_ops, vertical_ops, hide_numbers=True, prob=prob2)
        puzzle += "</div>\n"
        puzzle += "<div class='separator'></div>\n"
        puzzle += "<div class='answer'>Answer:"
        puzzle += html_puzzle(grid, horizontal_ops, vertical_ops)
        puzzle += "</div>\n"
        return render_template("index.html", size=size, puzzle=puzzle)

if __name__ == '__main__':
    application.run()
