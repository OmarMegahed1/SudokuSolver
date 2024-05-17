import pygame
import numpy as np
import time

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 580, 600
SIZE = 60
BOARD_POS = (20, 20)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

# Set up the display
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku Solver")  # Corrected method name

# Initialize board
board = np.zeros((9, 9), dtype=int)

# Function to draw grid lines
def draw_grid(win):
    for i in range(10):
        thickness = 1 if i % 3 != 0 else 3
        pygame.draw.line(win, BLACK, (BOARD_POS[0], BOARD_POS[1] + i * SIZE), (BOARD_POS[0] + 9 * SIZE, BOARD_POS[1] + i * SIZE), thickness)
        pygame.draw.line(win, BLACK, (BOARD_POS[0] + i * SIZE, BOARD_POS[1]), (BOARD_POS[0] + i * SIZE, BOARD_POS[1] + 9 * SIZE), thickness)

# Function to draw numbers
def draw_numbers(win, bo):
    font = pygame.font.SysFont(None, 40)
    for i in range(9):
        for j in range(9):
            if bo[i][j] != 0:
                num_text = font.render(str(bo[i][j]), True, BLACK)
                win.blit(num_text, (BOARD_POS[0] + j * SIZE + 20, BOARD_POS[1] + i * SIZE + 10))

# Function to draw solving time
def draw_time(win, time_taken):
    font = pygame.font.SysFont(None, 40)
    time_text = font.render(f"Time: {time_taken:.2f}s", True, BLACK)
    win.blit(time_text, (BOARD_POS[0], BOARD_POS[1] + 9 * SIZE + 10))

# Function to draw everything
def draw(win, bo, time_taken=None):
    win.fill(WHITE)
    draw_grid(win)
    draw_numbers(win, bo)
    if time_taken is not None:
        draw_time(win, time_taken)
    pygame.display.update()

# Function to find empty cells
def find_empty(bo):
    for i in range(9):
        for j in range(9):
            if bo[i][j] == 0:
                return (i, j)
    return None

# Function to check if a number is valid
def valid(bo, num, pos):
    row, col = pos
    # Check row
    if num in bo[row]:
        return False
    # Check column
    if num in bo[:, col]:
        return False
    # Check box
    box_x, box_y = col // 3, row // 3
    if num in bo[box_y*3:box_y*3+3, box_x*3:box_x*3+3]:
        return False
    return True

# Backtracking solver
def solve(bo):
    find = find_empty(bo)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1, 10):
        if valid(bo, i, (row, col)):
            bo[row][col] = i

            if solve(bo):
                return True

            bo[row][col] = 0

    return False

# Function to solve the board and measure the time taken
def solve_and_measure_time(bo):
    start_time = time.time()
    solve(bo)
    end_time = time.time()
    return end_time - start_time

# Main function
def main():
    run = True
    selected = None
    key = None
    clock = pygame.time.Clock()
    solving_time = None

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if BOARD_POS[0] < pos[0] < BOARD_POS[0] + 9 * SIZE and BOARD_POS[1] < pos[1] < BOARD_POS[1] + 9 * SIZE:
                    selected = ((pos[1] - BOARD_POS[1]) // SIZE, (pos[0] - BOARD_POS[0]) // SIZE)
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_0]:
                    key = int(event.unicode)
                if event.key == pygame.K_RETURN:
                    solving_time = solve_and_measure_time(board)

        if selected and key is not None:
            board[selected[0]][selected[1]] = key
            key = None

        draw(WIN, board, solving_time)
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()

