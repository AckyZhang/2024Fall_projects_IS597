class NurikabeSolver():
    def __init__(self, board):
        self.board = [[-1 for _ in range(self.size)] for _ in range(self.size)]
        self.size_row = len(board)
        self.size_col = len(board[0])
        self.islands = {((row, col), board[row][col]) for row in range(self.size_row) for col in range(self.size_col) if board[row][col] != 0}
        self.solution = None

    def check_solution(self, board, completed=True):
        check = self.check_2x2(board)
        if not check:
            return False
        if not completed:
            return True
        else:
            for i in range(self.size_row):
                for j in range(self.size_col):
                    if board[i][j] == -1:
                        return False
        return check

    def check_2x2(self, board):
        for i in range(self.size_row - 1):
            for j in range(self.size_col - 1):
                if board[i][j] == board[i + 1][j] == 0:
                    if board[i][(j + 1) % self.size_col] == board[i + 1][(j + 1) % self.size_col] == 0:
                        return False
        return True
    
    # def dfs(self, board, x, y, visited):
    #     if (x, y) in visited or not (0 <= x < len(board) and 0 <= y < len(board[0])) or board[x][y] != 1:
    #         return 0
    #     visited.add((x, y))
    #     directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    #     size = 1
    #     for dx, dy in directions:
    #         size += self.dfs(board, x + dx, y + dy, visited)
    #     return size

    # def is_valid_island(self, board, island_position, island_size):
    #     visited = set()
    #     island_size_found = self.dfs(board,island_position[0], island_position[1],visited)
    #     return island_size_found == island_size

    def trackback(self, row, col):
        if col == self.size_col:
            row += 1
            col = 0
        if row == self.size_row:
            return self.check_solution(self.board)

        if self.board[row][col] != -1:
            return self.trackback(row, col + 1)

        for value in [0, 1]: 
            self.board[row][col] = value
            if self.check_solution(self.board, completed=False):
                if self.trackback(row, col + 1):
                    return True
            self.board[row][col] = -1  # Reset cell

        return False

    def solve(self):
        if self.trackback(0, 0):
            self.solution = self.board
            return True
        return False


