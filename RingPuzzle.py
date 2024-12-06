import random


class NurikabeSolver():
    def __init__(self, board=None, size=None):
        self.clues = {}
        self.solution = []
        if board:
            self.board = board
            self.size_row = len(board)
            self.size_col = len(board[0])
            for r in range(self.size_row):
                for c in range(self.size_col):
                    if self.board[r][c] != -1:
                        self.clues[(r, c)] = self.board[r][c]
                        self.board[r][c] = 1
        elif size:
            self.size_row, self.size_col = size
            puzzle = self.generate_puzzle(self.size_row, self.size_col)
            print("Generated puzzle:")
            for row in puzzle:
                print(row)
        else:
            raise ValueError("Either board or size must be provided")

    def check_solution(self, completed=True, last_cell=None):
        if completed:
            if not self.check_complete():
                return False
            for (r, c), size in self.clues.items():
                if self.check_island_size(r, c) != size:
                    return False
            if not self.check_no_more_island():
                return False
            if not self.check_ocean_continuous():
                return False
            if not self.check_2x2(self.board):
                return False
            return True
        else:
            for (r, c), size in self.clues.items():
                if self.check_island_size(r, c) > size:
                    return False
            if not self.check_2x2(self.board, last_cell):
                return False
            return True

    def check_2x2(self, board, cell=None):
        if cell:
            for i in [cell[0], (cell[0] - 1)]:
                if i < 0 or i >= (self.size_row - 1):
                    continue
                for j in [cell[1], (cell[1] - 1) % self.size_col]:
                    if board[i][j] == board[i + 1][j] == 0:
                        if board[i][(j + 1) % self.size_col] == board[i + 1][(j + 1) % self.size_col] == 0:
                            return False
            return True
        for i in range(self.size_row - 1):
            for j in range(self.size_col):
                if board[i][j] == board[i + 1][j] == 0:
                    if board[i][(j + 1) % self.size_col] == board[i + 1][(j + 1) % self.size_col] == 0:
                        return False
        return True

    def check_no_more_island(self):
        island_in_clues = 0
        for size in self.clues.values():
            island_in_clues += size

        island_in_board = 0
        for r in range(self.size_row):
            for c in range(self.size_col):
                if self.board[r][c] == 1:
                    island_in_board += 1
        if island_in_board == island_in_clues:
            return True
        else:
            return False

    def check_complete(self):
        for r in range(self.size_row):
            for c in range(self.size_col):
                if self.board[r][c] == -1:
                    return False
        return True

    def dfs(self, row, col, target, visited):
        if (row, col) in visited:
            return 0
        if not (0 <= row < self.size_row):
            return 0
        if self.board[row][col] != target:
            return 0

        visited.add((row, col))
        size = 1
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_row = row + dr
            new_col = (col + dc) % self.size_col
            if (0 <= new_row < self.size_row):
                size += self.dfs(new_row, new_col, target, visited)
        return size

    def check_island_size(self, row, col):
        visited = set()
        return self.dfs(row, col, 1, visited)

    def check_ocean_continuous(self):
        visited = set()
        start = None
        for r in range(self.size_row):
            for c in range(self.size_col):
                if self.board[r][c] == 0:
                    start = (r, c)
                    break
            if start:
                break
        if not start:
            return False

        self.dfs(start[0], start[1], 0, visited)

        for r in range(self.size_row):
            for c in range(self.size_col):
                if self.board[r][c] == 0 and (r, c) not in visited:
                    return False
        return True

    def trackforward(self, row, col):
        if col == self.size_col:
            row += 1
            col = 0
        if row == self.size_row:
            if self.check_solution():
                self.solution.append([row[:] for row in self.board])
                return True
            return False

        if self.board[row][col] != -1:
            return self.trackforward(row, col + 1)

        for value in [0, 1]:
            if len(self.solution) > 1:
                return False
            self.board[row][col] = value
            if self.check_solution(completed=False, last_cell=(row, col)):
                self.trackforward(row, col + 1)
                if len(self.solution) > 1:
                    return True
            self.board[row][col] = -1  # Reset cell

    def prefill(self):
        for (r, c), size in self.clues.items():
            if size == 1:
                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    new_r = r + dr
                    new_c = (c + dc) % self.size_col
                    if 0 <= new_r < self.size_row and self.board[new_r][new_c] == -1:
                        self.board[new_r][new_c] = 0

    def solve(self):
        self.solution = []
        self.prefill()
        self.trackforward(0, 0)
        if len(self.solution) != 0:
            return True
        return False

    def print_solution(self):
        for i in range(len(self.solution)):
            print("Solution", i + 1, ":")
            for row in self.solution[i]:
                print("".join(['#' if x == 1 else '.' if x == 0 else '-' for x in row]))

    def generate_puzzle(self, row, col):
        total_trial = 0
        while True:
            total_trial += 1
            if total_trial % 1 == 0:
                print("Total_trail reached", total_trial)
            solution = [[1 for _ in range(col)] for _ in range(row)]
            self.board = solution
            self.size_row = row
            self.size_col = col
            self.clues = {}
            self.solution = []
            # randomize ocean start point
            start_r = random.randint(0, row - 1)
            start_c = random.randint(0, col - 1)
            solution[start_r][start_c] = 0

            ocean_size = random.randint(max(1, row * col // 4), (3 * row * col // 4))
            current_ocean_size = 1
            ocean = [(start_r, start_c)]
            ocean_freedom = [4]

            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            while current_ocean_size < ocean_size and sum(ocean_freedom) > 0:
                random.shuffle(directions)
                start_r, start_c = random.choices(ocean, weights=ocean_freedom)[0]
                res_ind = ocean.index((start_r, start_c))
                for dr, dc in directions:
                    new_r = start_r + dr
                    new_c = (start_c + dc) % col
                    if 0 <= new_r < row and solution[new_r][new_c] == 1:
                        solution[new_r][new_c] = 0
                        if self.check_2x2(solution):
                            ocean.append((new_r, new_c))
                            ocean_freedom.append(3)
                            current_ocean_size += 1
                            ocean_freedom[res_ind] -= 1
                            break
                        else:
                            ocean_freedom[res_ind] -= 1
                            solution[new_r][new_c] = 1
                    else:
                        ocean_freedom[res_ind] -= 1

            # check if puzzle has one solution
            island_visited = set()
            for r in range(row):
                for c in range(col):
                    if solution[r][c] == 1 and (r, c) not in island_visited:
                        visited = set()
                        island_size = self.dfs(r, c, 1, visited)
                        island_visited.update(visited)
                        self.clues[random.choice(list(visited))] = island_size
                        continue
            for r in range(row):
                for c in range(col):
                    if (r, c) in self.clues:
                        self.board[r][c] = 1
                    else:
                        self.board[r][c] = -1

            self.solve()
            if len(self.solution) > 1:
                print("Multiple solution")
                continue
            elif len(self.solution) == 0:
                print("No solution")
                continue
            else:
                print("Total_trail", total_trial)
                puzzle = [[-1 for _ in range(col)] for _ in range(row)]
                for (r, c), size in self.clues.items():
                    puzzle[r][c] = size
                return puzzle


# Example puzzle input
# puzzle = [
#     [3, -1, -1, -1],
#     [-1, -1, 1, -1],
#     [-1, -1, -1, -1],
#     [-1, -1, -1, 2],
# ]
# puzzle = [
#     [-1, -1, 1],
#     [1, -1, -1],
#     [-1, 1, -1],
# ]
# puzzle = [
#     [3, -1, -1],
#     [-1, -1, -1],
#     [-1, -1, 3],
# ]
puzzle = [
    [-1, -1, -1],
    [-1, 2, -1],
    [-1, -1, -1],
]
# Solve the Nurikabe puzzle
# solver = NurikabeSolver(board=puzzle)

solver = NurikabeSolver(size=(6, 6))


if solver.solve():
    print("Solved puzzle:")
    solver.print_solution()
else:
    print("No solution exists.")
