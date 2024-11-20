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
