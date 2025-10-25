# -*- coding: utf-8 -*-
"""
Neon_RunnerC — Day2 模範（教師用／厚手コメント）
- 追加済：衝突→終了、スコア、難易度加速、ベストスコア保存、簡易パーティクル
"""
import os, random, json
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame
from config import WIDTH, HEIGHT, FPS, BG, FG, NEON1, NEON2, GROUND_Y, \
                   PLAYER_W, PLAYER_H, PLAYER_COLOR, GRAVITY, JUMP_VELOCITY, \
                   OBSTACLE_MIN_GAP, OBSTACLE_MAX_GAP, \
                   OBSTACLE_MIN_W, OBSTACLE_MAX_W, \
                   OBSTACLE_MIN_H, OBSTACLE_MAX_H, \
                   SCORE_PER_FRAME

BEST_FILE = "best.txt"

def load_best():
    try:
        with open(BEST_FILE, "r", encoding="utf-8") as f:
            return int(f.read().strip())
    except Exception:
        return 0

def save_best(v):
    try:
        with open(BEST_FILE, "w", encoding="utf-8") as f:
            f.write(str(int(v)))
    except Exception:
        pass

def spawn_obstacle(x_base):
    # 生成：幅・高さのランダム、下端を地面に揃える
    w = random.randint(OBSTACLE_MIN_W, OBSTACLE_MAX_W)
    h = random.randint(OBSTACLE_MIN_H, OBSTACLE_MAX_H)
    y = GROUND_Y - h
    return pygame.Rect(x_base, y, w, h)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Neon_RunnerC - Day2 (Answer)")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 28)

    # 地面
    ground = pygame.Surface((WIDTH, HEIGHT - GROUND_Y), pygame.SRCALPHA)
    ground.fill((20, 24, 34))
    pygame.draw.line(ground, NEON1, (0, 0), (WIDTH, 0), 3)
    g_x1, g_x2 = 0, WIDTH

    # プレイヤ
    px = WIDTH * 0.25
    py = GROUND_Y - PLAYER_H
    vy = 0.0
    on_ground = True

    # 障害物
    obstacles = []
    cursor = WIDTH + 100
    for _ in range(5):
        obstacles.append(spawn_obstacle(cursor))
        cursor += random.randint(OBSTACLE_MIN_GAP, OBSTACLE_MAX_GAP)

    # スコア・難易度
    score = 0
    best = load_best()
    speed = 6
    SPEED_MAX = 12

    # 簡易パーティクル（着地時）
    particles = []  # dict: {x,y,vx,vy,life}

    game_over = False

    def add_land_particles(x, y):
        for i in range(8):
            particles.append({
                "x": x,
                "y": y,
                "vx": (random.random()*2-1)*2.5,
                "vy": -random.random()*3.0,
                "life": random.randint(12, 18)
            })

    def update_particles():
        nonlocal particles
        newp = []
        for p in particles:
            p["vy"] += 0.3
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            p["life"] -= 1
            if p["life"] > 0:
                newp.append(p)
        particles = newp

    def draw_particles(surf):
        for p in particles:
            r = pygame.Rect(int(p["x"]), int(p["y"]), 4, 4)
            pygame.draw.rect(surf, NEON1, r, border_radius=2)

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); return
            if game_over:
                if e.type == pygame.KEYDOWN:
                    # リスタート：状態リセット
                    px = WIDTH * 0.25
                    py = GROUND_Y - PLAYER_H
                    vy = 0.0
                    on_ground = True
                    obstacles.clear()
                    cursor = WIDTH + 100
                    for _ in range(5):
                        obstacles.append(spawn_obstacle(cursor))
                        cursor += random.randint(OBSTACLE_MIN_GAP, OBSTACLE_MAX_GAP)
                    score = 0
                    speed = 6
                    particles.clear()
                    game_over = False

        if not game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]:
                if on_ground:
                    vy = JUMP_VELOCITY
                    on_ground = False

            vy += GRAVITY
            py += vy
            was_air = not on_ground
            if py >= GROUND_Y - PLAYER_H:
                py = GROUND_Y - PLAYER_H
                vy = 0.0
                on_ground = True
                if was_air:
                    add_land_particles(px + PLAYER_W*0.5, py + PLAYER_H)

            # 地面スクロール
            g_x1 -= speed; g_x2 -= speed
            if g_x1 + WIDTH <= 0: g_x1 = g_x2 + WIDTH
            if g_x2 + WIDTH <= 0: g_x2 = g_x1 + WIDTH

            # 障害物スクロール＋再配置
            for r in obstacles:
                r.x -= speed
            if obstacles and obstacles[0].x + obstacles[0].width < 0:
                obstacles.pop(0)
                cursor = obstacles[-1].x + random.randint(OBSTACLE_MIN_GAP, OBSTACLE_MAX_GAP)
                obstacles.append(spawn_obstacle(cursor))

            # スコア＆加速
            score += SCORE_PER_FRAME
            if score % 300 == 0 and speed < SPEED_MAX:
                speed += 0.2

            # 衝突判定（矩形 vs 矩形）
            rect_player = pygame.Rect(int(px), int(py), PLAYER_W, PLAYER_H)
            for r in obstacles:
                if rect_player.colliderect(r):
                    game_over = True
                    if score > best:
                        best = score
                        save_best(best)
                    break

            update_particles()

        # 描画
        screen.fill(BG)
        screen.blit(ground, (g_x1, GROUND_Y))
        screen.blit(ground, (g_x2, GROUND_Y))

        for r in obstacles:
            pygame.draw.rect(screen, NEON2, r, border_radius=4)

        rect_player = pygame.Rect(int(px), int(py), PLAYER_W, PLAYER_H)
        pygame.draw.rect(screen, PLAYER_COLOR, rect_player, border_radius=6)
        draw_particles(screen)

        # UI
        ui = f"Score: {score:05d}   Best: {best:05d}   Speed: {speed:.1f}"
        screen.blit(pygame.font.SysFont(None, 24).render(ui, True, FG), (16, 14))

        if game_over:
            msg1 = "GAME OVER — Enter/Spaceで再開"
            screen.blit(pygame.font.SysFont(None, 32).render(msg1, True, FG), (WIDTH//2-220, HEIGHT//2-16))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
