# src/maze.py
import random
from collections import deque
from PIL import Image, ImageDraw

def make_grid(w, h):
    return [[1]*w for _ in range(h)]

def neighbors(cell, w, h):
    x,y = cell
    dirs = [(2,0),(-2,0),(0,2),(0,-2)]
    for dx,dy in dirs:
        nx,ny = x+dx, y+dy
        if 0 < nx < w and 0 < ny < h:
            yield (nx,ny)

def carve_maze(w, h, seed=None):
    if seed is not None:
        random.seed(seed)
    grid = make_grid(w,h)
    start = (1,1)
    grid[start[1]][start[0]] = 0
    stack = [start]
    while stack:
        cell = stack[-1]
        neighs = [n for n in neighbors(cell,w,h) if grid[n[1]][n[0]]==1]
        if neighs:
            n = random.choice(neighs)
            between = ((cell[0]+n[0])//2, (cell[1]+n[1])//2)
            grid[between[1]][between[0]] = 0
            grid[n[1]][n[0]] = 0
            stack.append(n)
        else:
            stack.pop()
    return grid

def bfs_shortest_path(grid, start, goal):
    h = len(grid); w = len(grid[0])
    q = deque([start])
    prev = {start: None}
    while q:
        cur = q.popleft()
        if cur == goal:
            break
        x,y = cur
        for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            nx,ny = x+dx, y+dy
            if 0<=nx<w and 0<=ny<h and grid[ny][nx]==0 and (nx,ny) not in prev:
                prev[(nx,ny)] = cur
                q.append((nx,ny))
    if goal not in prev:
        return None
    path = []
    cur = goal
    while cur:
        path.append(cur)
        cur = prev[cur]
    path.reverse()
    return path

def find_goal(grid):
    h=len(grid); w=len(grid[0])
    for yy in range(h-2,0,-1):
        for xx in range(w-2,0,-1):
            if grid[yy][xx]==0:
                return (xx,yy)
    return None

def draw_maze(grid, path=None, start=(1,1), goal=None, scale=8, out_path=None):
    h = len(grid); w = len(grid[0])
    img = Image.new("RGB", (w*scale, h*scale), "white")
    draw = ImageDraw.Draw(img)
    for y in range(h):
        for x in range(w):
            if grid[y][x]==1:
                draw.rectangle([x*scale, y*scale, (x+1)*scale-1, (y+1)*scale-1], fill="black")
    if path:
        for (x,y) in path:
            draw.rectangle([x*scale, y*scale, (x+1)*scale-1, (y+1)*scale-1], fill=(180,180,180))
    draw.rectangle([start[0]*scale, start[1]*scale, (start[0]+1)*scale-1, (start[1]+1)*scale-1], fill=(0,200,0))
    if goal:
        draw.rectangle([goal[0]*scale, goal[1]*scale, (goal[0]+1)*scale-1, (goal[1]+1)*scale-1], fill=(200,0,0))
    if out_path:
        img.save(out_path)
    return img
