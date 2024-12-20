import tkinter as tk
from tkinter import messagebox

class SudokuSolver(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sudoku Solver")
        self.cells = {}
        self.geometry("800x600")
        self.state('zoomed')
        self.configure(bg='orange')
        self.create_grid()
        self.create_buttons()

    def create_grid(self):
        grid_frame = tk.Frame(self, bg='lightgrey')
        grid_frame.place(relx=0.5, rely=0.4, anchor='center')
        colors = ["#D3D3D3", "#90EE90"]
        for row in range(9):
            for col in range(9):
                color = colors[(row // 3 + col // 3) % 2]
                entry = tk.Entry(grid_frame, width=2, font=('Arial', 18), justify='center', bg=color)
                entry.grid(row=row, column=col, padx=5, pady=5)
                self.cells[(row, col)] = entry

    def create_buttons(self):
        button_frame = tk.Frame(self, bg='lightgrey')
        button_frame.place(relx=0.5, rely=0.8, anchor='center')
        solve_button = tk.Button(button_frame, text="Solve", command=self.solve, width=10)
        solve_button.grid(row=0, column=0, padx=10, pady=10)

        clear_button = tk.Button(button_frame, text="Clear", command=self.clear_grid, width=10)
        clear_button.grid(row=0, column=1, padx=10, pady=10)

    def clear_grid(self):
        for entry in self.cells.values():
            entry.delete(0, tk.END)

    def get_grid(self):
        grid = []
        for row in range(9):
            current_row = []
            for col in range(9):
                value = self.cells[(row, col)].get()
                current_row.append(int(value) if value.isdigit() else 0)
            grid.append(current_row)
        return grid

    def is_valid(self, grid, row, col, num):
        if num in grid[row]:
            return False
        if num in [grid[i][col] for i in range(9)]:
            return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if grid[start_row + i][start_col + j] == num:
                    return False
        return True

    def is_initial_valid(self, grid):
        for row in range(9):
            for col in range(9):
                num = grid[row][col]
                if num != 0:
                    grid[row][col] = 0
                    if not self.is_valid(grid, row, col, num):
                        return False
                    grid[row][col] = num
        return True

    def solve_grid(self, grid):
        for row in range(9):
            for col in range(9):
                if grid[row][col] == 0:
                    for num in range(1, 10):
                        if self.is_valid(grid, row, col, num):
                            grid[row][col] = num
                            if self.solve_grid(grid):
                                return True
                            grid[row][col] = 0
                    return False
        return True

    def solve(self):
        grid = self.get_grid()
        if not self.is_initial_valid(grid):
            messagebox.showerror("Error", "Invalid Sudoku board!")
            return
        if self.solve_grid(grid):
            for row in range(9):
                for col in range(9):
                    self.cells[(row, col)].delete(0, tk.END)
                    self.cells[(row, col)].insert(0, str(grid[row][col]))
        else:
            messagebox.showerror("Error", "No solution exists!")

if __name__ == "__main__":
    app = SudokuSolver()
    app.mainloop()
