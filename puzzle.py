import random

# 격자 생성 (크기는 size 값으로 변경 가능)
def generate_grid(size=4):
    # 인접 셀과 같은 수가 안 되도록
    def random_except(exceptions, low=1, high=9):
        while True:
            n = random.randint(low, high)
            if n not in exceptions:
                return n

    grid = [[0] * size for _ in range(size)]
    for i in range(size):
        for j in range(size):
            neighbors = []
            if i > 0:
                neighbors.append(grid[i-1][j])
            if j > 0:
                neighbors.append(grid[i][j-1])
            grid[i][j] = random_except(neighbors)
    return grid

# 셀과 셀 사이의 자연수 사칙연산 생성
def calculate_operations(grid):
    size = len(grid)
    # 가로세로 방향 나눠 연산을 각각 생성
    horizontal_ops = [["" for _ in range(size - 1)] for _ in range(size)]
    vertical_ops = [["" for _ in range(size)] for _ in range(size - 1)]

    for i in range(size):
        for j in range(size):
            if j < size - 1:
                horizontal_ops[i][j] = choose_operation(grid[i][j], grid[i][j + 1])
            if i < size - 1:
                vertical_ops[i][j] = choose_operation(grid[i][j], grid[i + 1][j])

    return horizontal_ops, vertical_ops

# 두 셀 값을 주어주면 그 사이의 자연수 사칙연산을 생성
def choose_operation(a, b, prob=0.7):
    if a % b == 0 and random.random() < prob:
        return f"÷{a // b}"
    elif b % a == 0 and random.random() < prob:
        return f"×{b // a}"
    elif a > b:
        return f"-{a - b}"
    else:
        return f"+{b - a}"

# 퍼즐 출력 (hide_numbers=True가 되면 답을 숨김)
def print_puzzle(grid, horizontal_ops, vertical_ops, hide_numbers=False):
    size = len(grid)
    for i in range(size):
        row = []
        for j in range(size):
            if hide_numbers:
                row.append("[ ]")
            else:
                row.append(f"[{grid[i][j]}]")
            if j < size - 1:
                row.append(horizontal_ops[i][j])
        print(" ".join(row))
        if i < size - 1:
            row = []
            for j in range(size):
                row.append(vertical_ops[i][j])
                if j < size - 1:
                    row.append(" ")
            print("  ".join(row))

# 퍼즐 생성, 정답출력, 퍼즐출력
def main(size=4):
    grid = generate_grid(size)
    horizontal_ops, vertical_ops = calculate_operations(grid)
    print("Puzzle with answer:")
    print_puzzle(grid, horizontal_ops, vertical_ops)
    print("\n\n" + "- " * 10 + "\n\n")
    print("Puzzle without answer:")
    print_puzzle(grid, horizontal_ops, vertical_ops, hide_numbers=True)

if __name__ == "__main__":
    main(4)
