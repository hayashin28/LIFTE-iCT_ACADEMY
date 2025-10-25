# -*- coding: utf-8 -*-
import os, random
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame
from config import WIDTH, HEIGHT, FPS, TILE_SIZE, TILESET_COLUMNS, MAP_CSV, TILESET_IMAGE, BG, WHITE, YELLOW
from map_loader import load_csv_as_tilemap, load_tileset, draw_tilemap, rect_collides_with_walls
from entities_teacher import Player, Camera, HUD, NPC, DialogBox
def draw_fov_mask(screen, center, radius=140, alpha=180):
    mask = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    mask.fill((0, 0, 0, alpha))
    pygame.draw.circle(mask, (0,0,0,0), center, radius)
    screen.blit(mask, (0,0))
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("RPG Steel MasterD - Day2 (Answer)")
    clock = pygame.time.Clock(); font = pygame.font.SysFont(None, 18)
    grid, rows, cols = load_csv_as_tilemap(MAP_CSV)
    tiles = load_tileset(TILESET_IMAGE, TILE_SIZE, TILESET_COLUMNS)
    player = Player((TILE_SIZE*3, TILE_SIZE*3))
    camera = Camera(screen.get_size()); hud = HUD(); dialog = DialogBox(WIDTH)
    npcs = [NPC((TILE_SIZE*10, TILE_SIZE*6)), NPC((TILE_SIZE*14, TILE_SIZE*8))]
    coins = [pygame.Rect(TILE_SIZE*8, TILE_SIZE*5, 12, 12), pygame.Rect(TILE_SIZE*12, TILE_SIZE*7, 12, 12)]
    coin_count = 0
    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT: running = False
            elif e.type == pygame.KEYDOWN:
                if e.key in (pygame.K_RETURN, pygame.K_SPACE): dialog.advance()
                elif e.key == pygame.K_e and not dialog.active:
                    for npc in npcs:
                        if player.rect.colliderect(npc.rect.inflate(TILE_SIZE, TILE_SIZE)):
                            dialog.open(["鋼の街へようこそ。", "金貨を2枚集めてみよう。", "Eで会話、Shiftで走れるよ。"]); break
        keys = pygame.key.get_pressed(); run_key = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
        player.update(grid, keys, run_key, move_mode="collide", collides_fn=rect_collides_with_walls)
        for npc in npcs: npc.update()
        camera.follow(player.rect)
        # coin pickup
        pre_len = len(coins); coins = [c for c in coins if not player.rect.colliderect(c)]; coin_count += (pre_len - len(coins))
        if pre_len != len(coins): hud.toast(f"金貨を拾った！ x{coin_count}", 90)
        # draw
        screen.fill(BG)
        draw_tilemap(screen, grid, tiles, (int(camera.offset.x), int(camera.offset.y)))
        for c in coins:
            pygame.draw.rect(screen, YELLOW, pygame.Rect(c.x - camera.offset.x, c.y - camera.offset.y, c.w, c.h), border_radius=3)
        for npc in npcs:
            screen.blit(npc.image, (npc.rect.x - camera.offset.x, npc.rect.y - camera.offset.y))
        screen.blit(player.image, (player.rect.x - camera.offset.x, player.rect.y - camera.offset.y))
        draw_fov_mask(screen, (player.rect.centerx - int(camera.offset.x), player.rect.centery - int(camera.offset.y)))
        screen.blit(font.render(f"Coins: {coin_count}", True, WHITE), (16, 12))
        hud.render(screen); dialog.render(screen, h_px=84)
        pygame.display.flip(); clock.tick(FPS)
    pygame.quit()
if __name__ == "__main__":
    main()
