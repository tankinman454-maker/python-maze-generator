# src/main.py
from maze import carve_maze, find_goal, bfs_shortest_path, draw_maze
import os

def ascii_maze(grid, path=None, start=(1,1), goal=None):
    h = len(grid); w = len(grid[0])
    if goal is None:
        goal = find_goal(grid)
    path_set = set(path) if path else set()
    s = ""
    for y in range(h):
        line = ""
        for x in range(w):
            if (x,y)==start:
                line += "S"
            elif (x,y)==goal:
                line += "G"
            elif (x,y) in path_set:
                line += "."
            else:
                line += " " if grid[y][x]==0 else "#"
        s += line + "\n"
    return s

def main():
    width = 41
    height = 25
    grid = carve_maze(width, height, seed=42)
    start = (1,1)
    goal = find_goal(grid)
    path = bfs_shortest_path(grid, start, goal)
    print(ascii_maze(grid, path, start, goal))
    os.makedirs("../examples", exist_ok=True)
    draw_maze(grid, path, start, goal, scale=8, out_path="../examples/maze.png")

if __name__ == "__main__":
    main()
