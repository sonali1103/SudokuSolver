import tkinter as tk
import random

def print_board(board):
    # Helper function to print the Sudoku board
    for i in range(9):
        for j in range(9):
            print(board[i][j], end=" ")
        print()

def is_valid(board, row, col, num):
    # Check if placing 'num' at position (row, col) is valid
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False

    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False

    return True

def solve_sudoku(board):
    # Recursive function to solve the Sudoku puzzle using backtracking
    empty_cell = find_empty_cell(board)
    
    if not empty_cell:
        return True
    
    row, col = empty_cell

    for num in range(1, 10):
        if is_valid(board, row, col, str(num)):
            board[row][col] = str(num)

            if solve_sudoku(board):
                return True

            board[row][col] = '0'

    return False

def find_empty_cell(board):
    # Find an empty cell in the Sudoku board
    for i in range(9):
        for j in range(9):
            if board[i][j] == '0':
                return (i, j)
    return None

def naked_pairs(board):
    # Optimization using naked pairs in rows, columns, and subgrids
    # Find naked pairs in each row
    for row in range(9):
        pairs = {}
        for col in range(9):
            if len(board[row][col]) == 2:
                if board[row][col] not in pairs:
                    pairs[board[row][col]] = [(row, col)]
                else:
                    pairs[board[row][col]].append((row, col))
        
        for pair, positions in pairs.items():
            if len(positions) == 2:
                for other_col in range(9):
                    if other_col not in [positions[0][1], positions[1][1]]:
                        board[positions[0][0]][other_col] = board[positions[0][0]][other_col].replace(pair[0], '')
                        board[positions[0][0]][other_col] = board[positions[0][0]][other_col].replace(pair[1], '')
                        board[positions[1][0]][other_col] = board[positions[1][0]][other_col].replace(pair[0], '')
                        board[positions[1][0]][other_col] = board[positions[1][0]][other_col].replace(pair[1], '')

    # Find naked pairs in each column
    for col in range(9):
        pairs = {}
        for row in range(9):
            if len(board[row][col]) == 2:
                if board[row][col] not in pairs:
                    pairs[board[row][col]] = [(row, col)]
                else:
                    pairs[board[row][col]].append((row, col))
        
        for pair, positions in pairs.items():
            if len(positions) == 2:
                for other_row in range(9):
                    if other_row not in [positions[0][0], positions[1][0]]:
                        board[other_row][positions[0][1]] = board[other_row][positions[0][1]].replace(pair[0], '')
                        board[other_row][positions[0][1]] = board[other_row][positions[0][1]].replace(pair[1], '')
                        board[other_row][positions[1][1]] = board[other_row][positions[1][1]].replace(pair[0], '')
                        board[other_row][positions[1][1]] = board[other_row][positions[1][1]].replace(pair[1], '')

    # Find naked pairs in each 3x3 subgrid
    for start_row in range(0, 9, 3):
        for start_col in range(0, 9, 3):
            pairs = {}
            for i in range(3):
                for j in range(3):
                    row, col = start_row + i, start_col + j
                    if len(board[row][col]) == 2:
                        if board[row][col] not in pairs:
                            pairs[board[row][col]] = [(row, col)]
                        else:
                            pairs[board[row][col]].append((row, col))
            
            for pair, positions in pairs.items():
                if len(positions) == 2:
                    for i in range(3):
                        for j in range(3):
                            row, col = start_row + i, start_col + j
                            if (row, col) not in positions:
                                board[row][col] = board[row][col].replace(pair[0], '')
                                board[row][col] = board[row][col].replace(pair[1], '')

def generate_sudoku():
    # Generate a Sudoku puzzle by solving an empty board and then removing numbers
    empty_board = [['123456789' for _ in range(9)] for _ in range(9)]
    solve_sudoku(empty_board)

    puzzle = [row[:] for row in empty_board]

    # Remove some numbers to create the puzzle
    for _ in range(55):
        row, col = random.randint(0, 8), random.randint(0, 8)
        while puzzle[row][col] == '0':
            row, col = random.randint(0, 8), random.randint(0, 8)
        puzzle[row][col] = '0'

    return puzzle

class SudokuSolverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")

        self.board = [[tk.StringVar() for _ in range(9)] for _ in range(9)]

        self.create_widgets()

    def create_widgets(self):
        # Create the UI with Entry widgets for the Sudoku grid and a Solve button
        for i in range(9):
            for j in range(9):
                entry = tk.Entry(self.root, width=2, font=('Arial', 14), justify='center', textvariable=self.board[i][j], bd=1)
                entry.grid(row=i, column=j)
                
                # Add thicker borders between the 3x3 subgrids
                if (i // 3 == 1 or i // 3 == 2) and (j // 3 == 1 or j // 3 == 2):
                    entry.config(bd=3)

        solve_button = tk.Button(self.root, text="Solve Sudoku", command=self.solve, font=('Arial', 14))
        solve_button.grid(row=9, column=4, pady=10)

    def solve(self):
        # Solve the Sudoku puzzle based on the user's input
        user_solution = [['' for _ in range(9)] for _ in range(9)]

        for i in range(9):
            for j in range(9):
                entry_value = self.board[i][j].get()
                user_solution[i][j] = entry_value if entry_value.isdigit() and 1 <= int(entry_value) <= 9 else '0'

        naked_pairs(user_solution)
        solve_sudoku(user_solution)

        # Update the UI with the solved puzzle
        for i in range(9):
            for j in range(9):
                self.board[i][j].set(str(user_solution[i][j]))

if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuSolverApp(root)
    root.mainloop()
