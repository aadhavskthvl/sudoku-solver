def isValid(sudoku):
    for row in sudoku:
        numbers = []
        for cell in row:
            if cell != 0 and cell in numbers:
                return False
            numbers.append(cell)
    
    for i in range(9):
        numbers = []
        for j in range(9):
            cell = sudoku[i][j] 
            if cell != 0 and cell in numbers:
                return False
            numbers.append(cell)
    
    grids = {(i,j):[] for i in range(3) for j in range(3)}

    for i in range(9):
        for j in range(9):
            cell = sudoku[i][j]
            if cell != 0 and cell in grids[(i//3, j//3)]:
                return False
            grids[(i//3, j//3)].append(cell)
    return True

def sudoku_solver(sudoku):
    if not isValid(sudoku):
        return np.full((9, 9), -1)

    # possible values in each row, col and 3x3 grid
    rows, cols, grids = [], [], []
    # list of all the empty cells
    empty = []
    for i in range(9):
        rows.append({n for n in range(1, 10)})
        cols.append({n for n in range(1, 10)})
    for i in range(3):
        for j in range(3):
            grids.append({n for n in range(1, 10)})

    empty_num = 0
    for i in range(9):
        for j in range(9):
            if sudoku[i, j] != 0:
                if sudoku[i, j] in rows[i]:
                    rows[i].remove(sudoku[i, j])
                if sudoku[i, j] in cols[j]:
                    cols[j].remove(sudoku[i, j])
                if sudoku[i, j] in grids[(i//3)*3 + j//3]:
                    grids[(i//3)*3 + j//3].remove(sudoku[i, j])
            else:
                empty_num += 1
                empty.append((i, j))

    def solve(empty_index):
        if empty_index == empty_num:
            return True

        min_index = empty_index
        # finds possible values for a given cell
        min_values = rows[empty[empty_index][0]] & cols[empty[empty_index][1]] & grids[(empty[empty_index][0]//3)*3 + empty[empty_index][1]//3]
        for i in range(empty_index, empty_num):
            possible_values = rows[empty[i][0]] & cols[empty[i][1]] & grids[(empty[i][0]//3)*3 + empty[i][1]//3]
            if len(possible_values) < len(min_values):
                min_values = possible_values
                min_index = i

        empty[empty_index], empty[min_index] = empty[min_index], empty[empty_index]

        i, j = empty[empty_index]
        for num in min_values:
            #tries value and to solve with it
            rows[i].remove(num)
            cols[j].remove(num)
            grids[(i//3)*3 + j//3].remove(num)
            sudoku[i, j] = num
            if solve(empty_index + 1):
                return True
            # if it doesn't work, backtracks and solves using the next value in the list
            rows[i].add(num)
            cols[j].add(num)
            grids[(i//3)*3 + j//3].add(num)
        return False

    if not solve(0):
        return np.full((9, 9), -1)
    return sudoku

