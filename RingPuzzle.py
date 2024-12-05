import random

class NurikabeSolver():
    def __init__(self, board):
        self.board = board
        self.size_row = len(board)
        self.size_col = len(board[0])
        self.islands = {((row, col), board[row][col]): [(row, col)] for row in range(self.size_row) for col in range(self.size_col) if board[row][col] != 0}
        self.clues = {}
        self.solution = []
        for r in range(self.size_row):
            for c in range(self.size_col):
                if self.board[r][c] != -1:
                    self.clues[(r,c)] = self.board[r][c]
                    self.board[r][c] = 1

    def check_solution(self, completed=True):
        if completed:
            if not self.check_complete():
                return False
            for (r,c), size in self.clues.items():
                if self.check_island_size(r,c) != size:
                    return False
            if not self.check_no_more_island():
                return False
            if not self.check_ocean_continuous():
                return False
            if not self.check_2x2(self.board):
                return False
            return True          
        else:
            for (r,c), size in self.clues.items():
                if self.check_island_size(r,c) > size:
                    return False
            if not self.check_2x2(self.board):
                return False
            return True
    
    def check_2x2(self, board):
        for i in range(self.size_row - 1):
            for j in range(self.size_col - 1):
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
    
    def dfs(self, row, col, target, visited, state):
        state[row][col] = 1
        if (row,col) in visited:
            return 0
        if not (0 <= row < self.size_row):
            return 0
        if self.board[row][col] != target:
            return 0
        
        visited.add((row,col))
        size = 1
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            new_row = row + dr
            new_col = (col + dc) % self.size_col
            if (0 <= new_row < self.size_row):
                if state[new_row][new_col] == 0:
                    size += self.dfs(new_row, new_col, target, visited,state)
        return size


    def check_island_size(self,row,col):
        visited = set()
        state = [[0 for _ in range(self.size_col)] for _ in range(self.size_row)]
        return self.dfs(row, col, 1,visited,state)

    def check_ocean_continuous(self):
        visited = set()
        start = None
        state = [[0 for _ in range(self.size_col)] for _ in range(self.size_row)]
        for r in range(self.size_row):
            for c in range(self.size_col):
                if self.board[r][c] == 0:
                    start = (r,c)
                    break
            if start:
                break
        if not start:
            return False
        
        self.dfs(start[0],start[1], 0, visited, state)

        for r in range(self.size_row):
            for c in range(self.size_col):
                if self.board[r][c] == 0 and (r,c) not in visited:
                    return False
        return True

    def trackback(self, row, col):
        if col == self.size_col:
            row += 1
            col = 0
        if row == self.size_row:
            if self.check_solution():
                self.solution.append([row[:] for row in self.board])
                return True
            return False

        if self.board[row][col] != -1:
            return self.trackback(row, col + 1)

        for value in [0, 1]: 
            self.board[row][col] = value
            if self.check_solution(completed=False):
                self.trackback(row, col + 1)
            self.board[row][col] = -1  # Reset cell

    def solve(self):
        self.solution = []
        self.trackback(0, 0)
        if len(self.solution) != 0:
            return True
        return False

    def print_solution(self):
        for i in range(len(self.solution)):
            print("Solution",i+1, ":")
            for row in self.solution[i]:
                print("".join(['#' if x == 1 else '.' if x == 0 else '-' for x in row]))
        

    def generate_puzzle(self, row, col):
        while True:    
            solution = [[random.choice([0, 1]) for _ in range(col)] for _ in range(row)]
            self.board = solution
            self.size_row = row
            self.size_col = col
            self.clues = {}
            self.solution = []
            if not self.check_ocean_continuous():
                continue
            if not self.check_2x2(solution):
                continue

            # check if puzzle has one solution
            state = [[0 for _ in range(col)] for _ in range(row)]
            for r in range(row):
                for c in range(col):
                    if solution[r][c] == 1 and state[r][c] == 0:
                        visited = set()
                        island_size = self.dfs(r,c,1,visited,state)
                        self.clues[(r,c)] = island_size
                        # self.clues[random.choice(list(visited))] = island_size
                        continue
            for r in range(row):
                for c in range(col):
                    if (r,c) in self.clues:
                        self.board[r][c] = 1
                    else:
                        self.board[r][c] = -1
            
            self.solve()
            if len(self.solution) != 1:
                continue
            else:
                puzzle = [[-1 for _ in range(col)] for _ in range(row)]
                for (r,c), size in self.clues.items():
                    puzzle[r][c] = size
                return puzzle




# Example puzzle input
# puzzle = [
#     [3, -1, -1, -1],
#     [-1, -1, 1, -1],
#     [-1, -1, -1, -1],
#     [-1, -1, -1, 2],
# ]
puzzle = [
    [-1, -1, 1],
    [1, -1, -1],
    [-1, 1, -1],
]

# Solve the Nurikabe puzzle
solver = NurikabeSolver(puzzle)

puzzle_new = solver.generate_puzzle(3,3)
for row in puzzle_new:
    print(row)


if solver.solve():
    print("Solved puzzle:")
    solver.print_solution()
else:
    print("No solution exists.")
    
    
