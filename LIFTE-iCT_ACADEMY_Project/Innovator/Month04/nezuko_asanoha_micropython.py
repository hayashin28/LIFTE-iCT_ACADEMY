# nezuko_asanoha_micropython.py
# nezuko_asanoha_turtle.py
# Python (CPython) の turtle で「ねずこ柄（麻の葉）」を敷き詰め描画

import math
import turtle

# ===== 見た目設定 =====
PINK = "#f2b4c9"   # 背景色（お好みで調整）
LINE = "#ffffff"   # 線色（麻の葉の白）
LINE_WIDTH = 2

# グリッド（行列とセル半径）
R     = 28          # セルの半径（大きさ）
COLS  = 10          # 横方向の枚数
ROWS  = 8           # 縦方向の枚数

# ===== 初期化 =====
scr = turtle.Screen()
scr.title("Nezuko Asanoha Pattern")
scr.bgcolor(PINK)

t = turtle.Turtle(visible=False)
t.speed(0)
t.pencolor(LINE)
t.pensize(LINE_WIDTH)

# 高速化（環境によってはオフでもOK）
try:
    turtle.tracer(False)
except Exception:
    pass

def move(x, y):
    t.penup(); t.goto(x, y); t.pendown()

def line(x1, y1, x2, y2):
    t.penup(); t.goto(x1, y1); t.pendown(); t.goto(x2, y2)

def asanoha_cell(cx, cy, r, outline=False):
    """
    フラットトップ六角の中心(cx,cy)に麻の葉の「三本の直径」を描く。
    outline=True で六角の外枠も追加できます。
    """
    angs = [0, 60, 120, 180, 240, 300]  # 度数（0°が右、反時計回り）
    verts = [(cx + r*math.cos(math.radians(a)),
              cy + r*math.sin(math.radians(a))) for a in angs]
    # 三本の直径（0-180, 60-240, 120-300）
    for i in range(3):
        x1, y1 = verts[i]
        x2, y2 = verts[i+3]
        line(x1, y1, x2, y2)
    # 外枠の六角（任意）
    if outline:
        t.penup(); t.goto(verts[0]); t.pendown()
        for v in verts[1:]:
            t.goto(v)
        t.goto(verts[0])

# ===== 六角タイル配置（フラットトップ）=====
SQRT3 = math.sqrt(3)
DX = 1.5 * R        # 中心の横間隔
DY = SQRT3 * R      # 中心の縦間隔

# 全体サイズを見積もって中央配置
W = int((COLS - 1) * DX + 2*R)
H = int((ROWS - 1) * DY + 2*R)
OX = -W // 2      # 左端のx
OY =  H // 2      # 上端のy

for c in range(COLS):
    for r in range(ROWS):
        cx = OX + R + c * DX
        # 奇数列を半段下げる（フラットトップ六角のオフセット）
        cy = OY - R - (r * DY + (DY/2 if (c % 2) else 0))
        asanoha_cell(cx, cy, R, outline=False)
    # 行ごとに更新してチラつき低減
    try: turtle.update()
    except Exception: pass

try:
    turtle.update()
except Exception:
    pass

turtle.done()


# ねずこ柄（麻の葉）— MicroPython/CPython両対応を意識した最小API版
'''
import math

# ---- 互換初期化（MicroPython/PC双方） ----
try:
    import turtle
    scr = getattr(turtle, "Screen", lambda: None)()
    t = getattr(turtle, "Turtle", turtle.Turtle)()
except Exception:
    from turtle import *
    t = Turtle()
    try: scr = Screen()
    except: scr = None

# ---- 見た目（速さ・太さ） ----
try: t.hideturtle()
except: pass
try:
    # 可能なら一気描き（環境によっては未実装）
    turtle.tracer(False)
except Exception:
    pass
try: t.speed(0)
except: pass
t.pensize(2)

# ---- 色（ピンク地＋白線）----
PINK = "#f2b4c9"
LINE = "#ffffff"

# ---- 画面サイズ相当（格子の行列とサイズ）----
R = 28            # 麻の葉の“半径”（一辺の長さに近い）
COLS = 9          # 列数（横方向）
ROWS = 7          # 行数（縦方向）

SQRT3 = math.sqrt(3)
# フラットトップ六角の中心間隔（横=1.5R, 縦=√3 R）
DX = 1.5 * R
DY = SQRT3 * R

W = int((COLS - 1) * DX + 2*R)    # おおよその描画幅
H = int((ROWS - 1) * DY + 2*R)    # おおよその描画高
OX = -W // 2                       # 左上原点x
OY =  H // 2                       # 左上原点y

# ---- お役立ち ----
def move(x, y):
    t.penup(); t.goto(x, y); t.pendown()

def line(x1, y1, x2, y2):
    t.penup(); t.goto(x1, y1); t.pendown(); t.goto(x2, y2)

def polygon(points):
    t.penup(); t.goto(points[0]); t.pendown()
    for p in points[1:]: t.goto(p)
    t.goto(points[0])

# ---- 背景（ピンク塗り）----
def fill_bg():
    try:
        if scr: scr.bgcolor(PINK)  # これで済む環境は軽い
        else:
            raise Exception()
    except Exception:
        # 画面塗りが無い実装向けに矩形で塗る
        t.color(PINK)
        t.begin_fill()
        move(-W//2 - 10,  H//2 + 10)
        for _ in range(2):
            t.forward(W + 20); t.right(90)
            t.forward(H + 20); t.right(90)
        t.end_fill()

# ---- 麻の葉（中心に三本の直径＋六角の外枠は任意）----
def asanoha_cell(cx, cy, r, draw_hex=False):
    # 六角の頂点（フラットトップ角度）
    angs = [0, 60, 120, 180, 240, 300]
    verts = [(cx + r*math.cos(math.radians(a)),
              cy + r*math.sin(math.radians(a))) for a in angs]

    # 三本の直径（0-180 / 60-240 / 120-300）
    t.pencolor(LINE)
    for i in range(3):
        a = verts[i]
        b = verts[i+3]
        line(a[0], a[1], b[0], b[1])

    # 外枠を付けたい場合
    if draw_hex:
        polygon(verts)

# ---- 描画本体 ----
fill_bg()
t.pencolor(LINE)

for c in range(COLS):
    for r in range(ROWS):
        # 奇数列を半段下げる（フラットトップ六角のオフセット）
        cx = OX + R + c*DX
        cy = OY - R - (r*DY + (DY/2 if (c % 2 == 1) else 0))
        asanoha_cell(cx, cy, R, draw_hex=False)

# ---- 後処理 ----
try:
    turtle.update()   # tracer(False) が効いた環境向け
except Exception:
    pass
try:
    turtle.done()
except Exception:
    try: done()
    except Exception:
        pass
'''