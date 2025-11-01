# turtleで三色の市松模様（for + if/elif/else）
import turtle as t

t.speed(0)
t.hideturtle()
t.bgcolor("white")

size = 40       # 1マスの大きさ
rows, cols = 6, 6

def square(a):
    for _ in range(4):
        t.forward(a)
        t.right(90)

startx = - (cols * size) / 2
starty =   (rows * size) / 2

for r in range(rows):            # ← for（外側）
    for c in range(cols):        # ← for（内側）
        k = (r + c) % 3
        if k == 0:               # ← if
            t.fillcolor("red")
        elif k == 1:             # ← elif
            t.fillcolor("green")
        else:                    # ← else
            t.fillcolor("blue")

        t.penup()
        t.goto(startx + c*size, starty - r*size)
        t.pendown()
        t.begin_fill()
        square(size)
        t.end_fill()

t.done()
