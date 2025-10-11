BLOCK_TILES = {1}
def is_blocking(tile_id: int) -> bool: return tile_id in BLOCK_TILES
def can_move(grid, x, y) -> bool:
    h = len(grid); w = len(grid[0]) if h else 0
    if x<0 or y<0 or x>=w or y>=h: return False
    return not is_blocking(grid[y][x])