# -*- coding: utf-8 -*-
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame
from config import WIDTH, HEIGHT, FPS, TILE_SIZE, TILESET_COLUMNS, MAP_CSV, TILESET_IMAGE, BG
from map_loader import load_csv_as_tilemap, load_tileset, draw_tilemap
from entities_teacher import Player, Camera, HUD
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("RPG Steel MasterD - Day1 (Answer)")
    clock = pygame.time.Clock()
    grid, rows, cols = load_csv_as_tilemap(MAP_CSV)
    tiles = load_tileset(TILESET_IMAGE, TILE_SIZE, TILESET_COLUMNS)
    map_w_px, map_h_px = cols*TILE_SIZE, rows*TILE_SIZE
    player = Player((TILE_SIZE*2, TILE_SIZE*2))
    camera = Camera(screen.get_size())
    hud = HUD(); hud.toast("Shift走る／慣性＋摩擦／端Clamp", 180)
    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT: running = False
        keys = pygame.key.get_pressed()
        run_key = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
        player.update(grid, keys, run_key, move_mode="free", bounds_px=(map_w_px, map_h_px))
        camera.follow(player.rect)
        screen.fill(BG)
        draw_tilemap(screen, grid, tiles, (int(camera.offset.x), int(camera.offset.y)))
        screen.blit(player.image, (player.rect.x - camera.offset.x, player.rect.y - camera.offset.y))
        hud.render(screen)
        pygame.display.flip(); clock.tick(FPS)
    pygame.quit()
if __name__ == "__main__":
    main()
