from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.label import Label

class Game(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.clearcolor = (0, 0, 0, 1)
        self.ground_y = 100
        self.player_size = (40, 40)
        self.player_pos = [60, self.ground_y]
        self.vel_y = 0.0
        self.gravity = -900.0
        self.jump = 420.0
        self.obstacles = []
        self.spawn = 0.0
        self.score = 0

        with self.canvas:
            Color(0.1, 1.0, 0.9)
            self.player_rect = Rectangle(pos=self.player_pos, size=self.player_size)

        self.hud = Label(text="Score: 0", pos=(10, Window.height-30),
                         size_hint=(None, None))
        self.add_widget(self.hud)

        Clock.schedule_interval(self.update, 1/60)

    def on_touch_down(self, *args):
        if self.player_pos[1] <= self.ground_y + 1:
            self.vel_y = self.jump

    def rects_collide(self, a_pos, a_size, b_pos, b_size):
        ax, ay = a_pos; aw, ah = a_size
        bx, by = b_pos; bw, bh = b_size
        return (ax < bx + bw and ax + aw > bx and ay < by + bh and ay + ah > by)

    def update(self, dt):
        # 1) たまに障害物を生成
        self.spawn += dt
        if self.spawn > 1.2:
            self.spawn = 0.0
            size = (30, 60)
            pos = [Window.width, self.ground_y]
            with self.canvas:
                Color(1.0, 0.3, 0.6)
                rect = Rectangle(pos=pos, size=size)
            self.obstacles.append((rect, pos, size))

        # 2) プレイヤーの縦運動
        self.vel_y += self.gravity * dt
        self.player_pos[1] = max(self.ground_y, self.player_pos[1] + self.vel_y * dt)
        if self.player_pos[1] == self.ground_y and self.vel_y < 0:
            self.vel_y = 0.0
        self.player_rect.pos = self.player_pos

        # 3) 障害物の横移動と当たり判定
        speed = 220.0
        for rect, pos, size in list(self.obstacles):
            pos[0] -= speed * dt
            rect.pos = pos
            if pos[0] + size[0] < 0:
                self.obstacles.remove((rect, pos, size))
                self.canvas.remove(rect)
                self.score += 1
                self.hud.text = f"Score: {self.score}"
            elif self.rects_collide(self.player_pos, self.player_size, pos, size):
                Clock.unschedule(self.update)
                self.hud.text = f"Game Over  Score: {self.score}"
                return

class NeonRunnerApp(App):
    def build(self):
        return Game()

if __name__ == "__main__":
    NeonRunnerApp().run()
