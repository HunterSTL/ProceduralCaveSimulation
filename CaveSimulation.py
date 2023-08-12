import pygame
import random

grid_height = 50
grid_width = 50
cell_size = 10
density = 0.6

def generate_grid(grid_height, grid_width):
    grid = []
    for _ in range(grid_height):
        row = []
        for _ in range(grid_width):
            value = random.random()
            if value < density:
                row.append(1)
            else:
                row.append(0)
        grid.append(row)
    return grid

def get_wall_count(grid, x, y):
    wall_count = 0
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            nx = x + dx
            ny = y + dy
            if nx < 0 or nx > grid_width - 1 or ny < 0 or ny > grid_height - 1:
                wall_count += 1
            else:
                if (dx != 0 or dy != 0) and grid[ny][nx] == 1:
                    wall_count += 1
    return wall_count

def print_wall_count(grid):
    for y in range(grid_height):
        row_str = ""
        for x in range(grid_width):
            row_str += str(get_wall_count(grid, x, y))
        print(row_str)

def simulate_grid_step(grid):
    grid_copy = [[cell for cell in row] for row in grid]
    for y in range(grid_height):
        for x in range(grid_width):
            wall_count = get_wall_count(grid, x, y)
            if wall_count > 4:
                grid_copy[y][x] = 1
            else:
                grid_copy[y][x] = 0
    return grid_copy

def simulate_grid(grid, iterations):
    for _ in range(iterations):
        grid = simulate_grid_step(grid)
    return grid

grid = generate_grid(grid_height, grid_width)
grid = simulate_grid(grid, 5)

pygame.init()
window_size = (grid_width * cell_size, grid_height * cell_size)
window = pygame.display.set_mode(window_size)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for y in range(grid_height):
        for x in range(grid_width):
            color = (255, 255, 255) if grid[y][x] == 0 else (0, 0, 0)
            pygame.draw.rect(window, color, (x * cell_size, y * cell_size, cell_size, cell_size))
    pygame.display.flip()

pygame.quit()