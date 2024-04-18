import matplotlib.pyplot as plt

# Sudoku grid
sudoku_grid = [
    [0, 4, 0, 0, 3, 2, 0, 0, 0],
    [7, 3, 1, 0, 8, 6, 5, 9, 0],
    [2, 0, 9, 0, 1, 5, 4, 8, 3],
    [0, 7, 0, 0, 9, 0, 0, 0, 0],
    [0, 0, 0, 1, 4, 0, 9, 2, 0],
    [1, 0, 0, 5, 0, 0, 0, 3, 6],
    [0, 0, 0, 3, 0, 0, 6, 0, 0],
    [0, 5, 7, 0, 0, 0, 0, 4, 9],
    [9, 0, 6, 0, 5, 0, 0, 0, 0]
]

# Copy the original sudoku grid to the user sudoku grid
user_sudoku_grid = []
for row in sudoku_grid:
    user_sudoku_grid.append(row.copy())

light_grey = "#d3d3d3"

# Set the overall figure size
fig_size = 6  # Adjust this as needed
fig, axes = plt.subplots(9, 9, figsize=(fig_size, fig_size))

def update_cell(pos, num = None, facecolor = "white"):
    i, j = pos
    ax = axes[i, j]
    ax.clear()
    ax.set_facecolor(facecolor)
    if num:
        ax.text(0.5, 0.5, str(num), fontsize=12, ha='center', va='center', color="black")

# Adjusting each subplot's aspect ratio and hiding coordinates
for i in range(9):
    for j in range(9):
        axes[i, j].set_aspect('equal', adjustable='box')
        axes[i, j].tick_params(labelleft=False, labelbottom=False, left=False, bottom=False)  # Hide tick labels and ticks
        spines = axes[i, j].spines
        if i != 8:
            spines['bottom'].set_visible(False)
        if i % 3 != 0:
            spines['top'].set_color(light_grey)

        if j != 8:
            spines['right'].set_visible(False)
        if j % 3 != 0:
            spines['left'].set_color(light_grey)

        # Plotting the sudoku grid
        if sudoku_grid[i][j] != 0:
            update_cell((i, j), sudoku_grid[i][j])

plt.subplots_adjust(wspace=0, hspace=0)

fig.suptitle('Sudoku Game', fontsize=20, fontweight='bold')

wait_for_key = False    # Flag to wait for the user to enter a digit
focused_cell_i, focused_cell_j = None, None # Store the indices of the focused cell waiting for user input digit
duplicated_cells_indice = [] # Store the indices of duplicated cells with user input digit

def update_duplicated_cells(hightlight):
    global duplicated_cells_indice

    facecolor = "red" if hightlight else "white"

    for i, j in duplicated_cells_indice:
        update_cell((i, j), user_sudoku_grid[i][j], facecolor = facecolor)

    if not hightlight: # Clear the duplicated cells
        duplicated_cells_indice = []

# Mouse event handler
def on_click(event):
    global focused_cell_i, focused_cell_j
    global wait_for_key
    global duplicated_cells_indice
   
    def get_cell_indice(grid, ax):
        for i in range(9):
            for j in range(9):
                if grid[i][j] == ax:
                    return i, j
        return None, None
    
    i, j = get_cell_indice(axes, event.inaxes)
    if i is None or j is None:
        return
    print(f"Clicked on cell ({i}, {j})")

    if user_sudoku_grid[i][j] == 0: # is an blank cell
        if wait_for_key:
            update_cell((focused_cell_i, focused_cell_j))
            update_duplicated_cells(False)

        # Focus on the clicked blank cell
        focused_cell_i, focused_cell_j = i, j
        axes[focused_cell_i, focused_cell_j].set_facecolor(light_grey)
        fig.canvas.draw_idle()

        wait_for_key = True

def on_key(event):
    global wait_for_key
    if not wait_for_key:
        return
    
    if not event.key.isdigit() or event.key == '0':
        return
    
    num = int(event.key)
    print(f"Entered number: {num}")

    update_duplicated_cells(False)

    # Check if the entered number is duplicated in the row, column, or 3x3 grid
    global duplicated_cells_indice
    for i in range(9):
        if user_sudoku_grid[i][focused_cell_j] == num:
            duplicated_cells_indice.append((i, focused_cell_j))
            break

    for j in range(9):
        if user_sudoku_grid[focused_cell_i][j] == num:
            duplicated_cells_indice.append((focused_cell_i, j))
            break

    i_start, j_start = 3 * (focused_cell_i // 3), 3 * (focused_cell_j // 3)
    for i in range(i_start, i_start + 3):
        for j in range(j_start, j_start + 3):
            if user_sudoku_grid[i][j] == num and (i, j) not in duplicated_cells_indice:
                duplicated_cells_indice.append((i, j))
                break

    if len(duplicated_cells_indice) > 0:
        update_duplicated_cells(True)
        update_cell((focused_cell_i, focused_cell_j), num, facecolor = "red")
    else:
        update_cell((focused_cell_i, focused_cell_j), num, "white")
        user_sudoku_grid[focused_cell_i][focused_cell_j] = num
        wait_for_key = False

    fig.canvas.draw_idle()

# Respond to the user's input
click_cid = fig.canvas.mpl_connect('button_press_event', on_click)
key_press_cid = fig.canvas.mpl_connect('key_press_event', on_key)

plt.show()
