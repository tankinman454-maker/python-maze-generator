# tests/test_maze_basic.py
from src.maze import carve_maze, bfs_shortest_path, find_goal

def test_maze():
    grid = carve_maze(21, 15, seed=0)
    start = (1,1)
    goal = find_goal(grid)
    path = bfs_shortest_path(grid, start, goal)
    assert path is not None
