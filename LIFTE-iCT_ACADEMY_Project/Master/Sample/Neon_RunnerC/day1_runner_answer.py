# -*- coding: utf-8 -*-
"""
Neon_RunnerC — Day1 模範（教師用／厚手コメント）
- 追加済：二段ジャンプ／長押しジャンプ／着地フラッシュ
- 授業ではここから不要部分を削って見せるのも可
"""
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame
from config import WIDTH, HEIGHT, FPS, GROUND_Y, \
                   PLAYER_W, PLAYER_H, PLAYER_COLOR, \
                   GRAVITY, JUMP_VELOCITY, BG, FG, NEON1

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Neon_RunnerC - Day1 (Answer)")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)

    # --- 地面（2枚スクロール） ---
    ground = pygame.Surface((WIDTH, HEIGHT - GROUND_Y), pygame.SRCALPHA)
    ground.fill((20, 24, 34))
    pygame.draw.line(ground, NEON1, (0, 0), (WIDTH, 0), 3)
    g_x1, g_x2 = 0, WIDTH
    speed = 6

    # --- プレイヤ状態 ---
    px = WIDTH * 0.25
    py = GROUND_Y - PLAYER_H
    vy = 0.0
    on_ground = True
    can_double = True          # ★空中で一度だけジャンプを許可
    jump_hold = 0              # ★長押しの保持カウンタ（フレーム）
    JUMP_HOLD_MAX = 10         # ★押し続けて効果がある上限フレーム
    landing_flash = 0          # ★着地フラッシュ（色変化の残りフレーム）

    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.KEYDOWN:
                if e.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
                    if on_ground:
                        # 1段目のジャンプ開始
                        vy = JUMP_VELOCITY
                        on_ground = False
                        can_double = True
                        jump_hold = 0
                    elif can_double:
                        # 2段目（低め）
                        vy = JUMP_VELOCITY * 0.85
                        can_double = False
                        jump_hold = 0
            elif e.type == pygame.KEYUP:
                if e.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
                    jump_hold = JUMP_HOLD_MAX  # 以後の長押し効果を止める

        # --- 長押しジャンプ：押している間だけ重力を弱めて“ふわっ”と ---
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]:
            if not on_ground and jump_hold < JUMP_HOLD_MAX and vy < 0:
                vy += GRAVITY * (-0.5)  # 重力を相殺して上昇を少し延長
                jump_hold += 1

        # --- 物理 ---
        vy += GRAVITY
        py += vy

        # --- 接地処理（境界で吸着＋着地フラッシュ） ---
        was_air = not on_ground
        if py >= GROUND_Y - PLAYER_H:
            py = GROUND_Y - PLAYER_H
            vy = 0.0
            on_ground = True
            if was_air:
                landing_flash = 6  # 着地瞬間だけ色を明るく
        else:
            on_ground = False

        # --- 地面スクロール ---
        g_x1 -= speed; g_x2 -= speed
        if g_x1 + WIDTH <= 0: g_x1 = g_x2 + WIDTH
        if g_x2 + WIDTH <= 0: g_x2 = g_x1 + WIDTH

        # --- 描画 ---
        screen.fill(BG)
        screen.blit(ground, (g_x1, GROUND_Y))
        screen.blit(ground, (g_x2, GROUND_Y))

        # プレイヤ矩形（着地フラッシュ）
        color = PLAYER_COLOR if landing_flash == 0 else (min(255, PLAYER_COLOR[0]+70), min(255, PLAYER_COLOR[1]+70), min(255, PLAYER_COLOR[2]+70))
        if landing_flash > 0:
            landing_flash -= 1
        rect = pygame.Rect(int(px), int(py), PLAYER_W, PLAYER_H)
        pygame.draw.rect(screen, color, rect, border_radius=6)

        # UI
        tip = "二段・長押し・着地演出を実装済（授業では片方だけでもOK）"
        screen.blit(font.render(tip, True, FG), (16, 14))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
