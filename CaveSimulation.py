import pygame
import random

grid_height = 50
grid_width = 50
cell_size = 20
density = 0.4
iterations = 2
search_range = 2

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

def get_wall_count(grid, x, y, search_range):
    wall_count = 0
    if search_range < 1:
        start = -1
        end = 2
    else:
        start = -1 - (search_range - 1)
        end = 2 + (search_range - 1)
    for dy in range(start, end):
        for dx in range(start, end):
            nx = x + dx
            ny = y + dy
            if nx < 0 or nx > grid_width - 1 or ny < 0 or ny > grid_height - 1:
                wall_count += 1
            else:
                if (dx != 0 or dy != 0) and grid[ny][nx] == 1:
                    wall_count += 1
    return wall_count

def print_wall_count(grid, search_range):
    for y in range(grid_height):
        row_str = ""
        for x in range(grid_width):
            row_str += str(get_wall_count(grid, x, y, search_range))
        print(row_str)

def simulate_grid_step(grid, search_range):
    max_wall_count = (2 * search_range + 1) ** 2 - 1
    ratio_wall = 0.4
    ratio_open = 0.5
    grid_copy = [[cell for cell in row] for row in grid]
    for y in range(grid_height):
        for x in range(grid_width):
            wall_count = get_wall_count(grid, x, y, search_range)
            threshold_wall = int(max_wall_count * ratio_wall)
            threshold_open = int(max_wall_count * ratio_open)
            if grid[y][x] == 1:  # If the current cell is a wall
                if wall_count > threshold_wall:
                    grid_copy[y][x] = 1
                else:
                    grid_copy[y][x] = 0
            else:  # If the current cell is an open space
                if wall_count > threshold_open:
                    grid_copy[y][x] = 1
                else:
                    grid_copy[y][x] = 0
    return grid_copy

def simulate_grid(grid, iterations, search_range):
    for _ in range(iterations):
        grid = simulate_grid_step(grid, search_range)
    return grid

grid = generate_grid(grid_height, grid_width)
#print_wall_count(grid, search_range)
grid = simulate_grid(grid, iterations, search_range)

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