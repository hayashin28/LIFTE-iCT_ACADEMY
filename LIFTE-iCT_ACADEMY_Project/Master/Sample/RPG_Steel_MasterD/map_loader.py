# -*- coding: utf-8 -*-
"""
TEACHER版：APIは生徒版と同じ。壁衝突の補助関数も提供。
"""
import csv, pygame
from pygame import Surface, Rect
from config import TILE_SIZE, TILESET_COLUMNS

def load_csv_as_tilemap(csv_path: str):
    grid = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            grid.append([int(x) for x in row])
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    return grid, rows, cols

def load_tileset(image_path: str, tile_size: int, columns: int):
    sheet = pygame.image.load(image_path).convert_alpha()
    w, h = sheet.get_width(), sheet.get_height()
    tiles, rows = [], h // tile_size
    for r in range(rows):
        for c in range(columns):
            x, y = c * tile_size, r * tile_size
            tile = Surface((tile_size, tile_size), pygame.SRCALPHA)
            tile.blit(sheet, (0, 0), Rect(x, y, tile_size, tile_size))
            tiles.append(tile)
    return tiles

def draw_tilemap(screen: Surface, grid, tiles, camera_offset):
    tile = TILE_SIZE
    start_c = max(0, camera_offset[0] // tile)
    start_r = max(0, camera_offset[1] // tile)
    view_cols = screen.get_width() // tile + 2
    view_rows = screen.get_height() // tile + 2
    for r in range(start_r, start_r + view_rows):
        if r < 0 or r >= len(grid): continue
        for c in range(start_c, start_c + view_cols):
            if c < 0 or c >= len(grid[r]): continue
            tid = grid[r][c]
            if 0 <= tid < len(tiles):
                sx = c * tile - camera_offset[0]
                sy = r * tile - camera_offset[1]
                screen.blit(tiles[tid], (sx, sy))

def rect_collides_with_walls(rect, grid, wall_ids=(1,)):
    tile = TILE_SIZE
    min_c = max(0, rect.left // tile)
    max_c = min(len(grid[0]) - 1, rect.right // tile)
    min_r = max(0, rect.top // tile)
    max_r = min(len(grid) - 1, rect.bottom // tile)
    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            if grid[r][c] in wall_ids:
                wall = pygame.Rect(c * tile, r * tile, tile, tile)
                if rect.colliderect(wall):
                    return True
    return False
