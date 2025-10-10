# tanjiro_ichimatsu_micropython.py
# MicroPython/CPython どちらでも動く想定の最小API（turtle）版
# 市松模様（炭治郎柄）：黒背景に緑の正方形を交互配置

# --- 互換初期化 ---
try:
    import turtle
    scr = getattr(turtle, "Screen", lambda: None)()
    t = getattr(turtle, "Turtle", turtle.Turtle)()
except Exception:
    from turtle import *
    t = Turtle()
    try:
        scr = Screen()
    except:
        scr = None

# --- 見た目調整 ---
try: t.hideturtle()
except: pass
try: t.speed(0)          # 一番速く
except: pass
try:
    if scr: scr.bgcolor("#000000")  # 背景を黒（未対応なら下で黒マスも描けます）
except: pass
t.pensize(1)

# --- 色定義（緑は羽織っぽい青緑に近い値）---
GREEN = "#0fa37f"  # お好みで "#00a58a" "#0f9d58" などへ
BLACK = "#000000"

# --- 正方形を塗る関数（fill未対応なら輪郭のみで描画）---
def fill_square(x, y, a, color):
    # (x,y) は左上、a は1辺の長さ
    try:
        t.penup(); t.goto(x, y); t.pendown()
    except Exception:
        # gotoが無い実装は少ないですが、念のため
        pass
    try:
        t.color(color)
    except:
        pass
    can_fill = hasattr(t, "begin_fill")
    if can_fill:
        t.begin_fill()
    for _ in range(4):
        t.forward(a); t.right(90)
    if can_fill:
        t.end_fill()

# --- グリッド設定（行・列・サイズをお好みで）---
ROWS = 8      # 行数
COLS = 10     # 列数
SIZE = 36     # 1マスのピクセル（環境に合わせて）

# 画面中央に収まるよう原点オフセット（左上を起点に）
W = COLS * SIZE
H = ROWS * SIZE
origin_x = -W // 2
origin_y =  H // 2

# --- 描画（黒背景が使えない環境のために全マス描画も可能）---
# 1) 背景が黒にできる環境なら、緑マスだけ描く：
draw_all = False  # Trueにすると全マス（黒＋緑）を塗る

for r in range(ROWS):
    for c in range(COLS):
        x = origin_x + c * SIZE
        y = origin_y - r * SIZE
        if draw_all:
            # 交互に黒／緑
            color = GREEN if ((r + c) % 2 == 0) else BLACK
            fill_square(x, y, SIZE, color)
        else:
            # 黒は背景に任せ、緑だけを描く（軽量）
            if (r + c) % 2 == 0:
                fill_square(x, y, SIZE, GREEN)

# おしまい処理
try:
    turtle.done()
except Exception:
    try: done()
    except: pass
