# -*- coding: utf-8 -*-
import pygame, random
from pygame import Surface
from config import (
    TILE_SIZE, PLAYER_SPEED, RUN_MULTIPLIER, PLAYER_ACCEL, PLAYER_FRICTION,
    WHITE, BLUE, GREEN, YELLOW, RED, FONT_SIZE
)
class Player(pygame.sprite.Sprite):
    def __init__(self, pos_px):
        super().__init__()
        self.image = Surface((TILE_SIZE-6, TILE_SIZE-6), pygame.SRCALPHA)
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(topleft=pos_px)
        self.vel = pygame.math.Vector2(0, 0)
    def handle_input(self, keys, running: bool):
        dir = pygame.math.Vector2(0, 0)
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:  dir.x -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: dir.x += 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:    dir.y -= 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:  dir.y += 1
        if dir.length_squared() > 0:
            dir = dir.normalize()
        speed = PLAYER_SPEED * (RUN_MULTIPLIER if running else 1.0)
        self.vel.x = self.vel.x*(1-PLAYER_ACCEL) + dir.x*speed*PLAYER_ACCEL
        self.vel.y = self.vel.y*(1-PLAYER_ACCEL) + dir.y*speed*PLAYER_ACCEL
        self.vel *= PLAYER_FRICTION
    def move_free(self, bounds_px):
        self.rect.x += int(self.vel.x)
        self.rect.y += int(self.vel.y)
        max_x = bounds_px[0] - self.rect.width
        max_y = bounds_px[1] - self.rect.height
        self.rect.x = max(0, min(self.rect.x, max_x))
        self.rect.y = max(0, min(self.rect.y, max_y))
    def move_with_collision(self, grid, collides_fn):
        self.rect.x += int(self.vel.x)
        if collides_fn(self.rect, grid):
            self.rect.x -= int(self.vel.x)
        self.rect.y += int(self.vel.y)
        if collides_fn(self.rect, grid):
            self.rect.y -= int(self.vel.y)
    def update(self, grid, keys, running, move_mode="free", **kw):
        self.handle_input(keys, running)
        if move_mode == "free":
            bounds_px = kw.get("bounds_px", (1024, 768))
            self.move_free(bounds_px)
        else:
            collides_fn = kw.get("collides_fn")
            self.move_with_collision(grid, collides_fn)
class Camera:
    def __init__(self, screen_size):
        self.offset = pygame.math.Vector2(0, 0)
        self.screen_w, self.screen_h = screen_size
    def follow(self, target_rect):
        self.offset.x = max(0, target_rect.centerx - self.screen_w//2)
        self.offset.y = max(0, target_rect.centery - self.screen_h//2)
class HUD:
    def __init__(self):
        self.font = pygame.font.SysFont(None, FONT_SIZE)
        self.msg = ""; self.timer = 0
    def toast(self, text, frame=120):
        self.msg = text; self.timer = frame
    def render(self, screen):
        if self.timer > 0 and self.msg:
            surf = self.font.render(self.msg, True, WHITE)
            screen.blit(surf, (16, 12))
            self.timer -= 1
class DialogBox:
    def __init__(self, width_px):
        self.font = pygame.font.SysFont(None, FONT_SIZE+2)
        self.lines = []; self.active = False; self.width = width_px
    def open(self, lines):
        self.lines = list(lines); self.active = True
    def advance(self):
        if not self.active: return
        if self.lines: self.lines.pop(0)
        if not self.lines: self.active = False
    def render(self, screen, h_px=80):
        if not self.active: return
        import pygame
        pad = 12
        box = pygame.Surface((self.width, h_px), pygame.SRCALPHA)
        box.fill((0, 0, 0, 160))
        if self.lines:
            surf = self.font.render(self.lines[0], True, WHITE)
            box.blit(surf, (pad, pad))
        screen.blit(box, (0, screen.get_height()-h_px))
class NPC(pygame.sprite.Sprite):
    def __init__(self, pos_px):
        super().__init__()
        self.image = Surface((TILE_SIZE-6, TILE_SIZE-6), pygame.SRCALPHA)
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(topleft=pos_px)
        self.vel = pygame.math.Vector2(0, 0); self.timer = 0
    def update(self):
        import random
        self.timer -= 1
        if self.timer <= 0:
            self.timer = random.randint(30, 120)
            self.vel.xy = (random.choice([-1,0,1]), random.choice([-1,0,1]))
        self.rect.x += self.vel.x; self.rect.y += self.vel.y
