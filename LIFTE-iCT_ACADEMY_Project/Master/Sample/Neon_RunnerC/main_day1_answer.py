# -*- coding: utf-8 -*-
"""Day1 模範：ジャンプ＋二段ジャンプ＋簡易パララックス"""
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.uix.label import Label
from config import WIDTH, HEIGHT, GROUND_Y, SPEED, JUMP_VEL, GRAVITY, BG

class Game(Widget):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.size=(WIDTH,HEIGHT)
        self.scroll=0.0
        self.x=120; self.w=32
        self.ground=GROUND_Y; self.y=self.ground; self.h=32
        self.vy=0.0; self.can_double=False
        self.keys=set()
        Window.bind(on_key_down=self._kd, on_key_up=self._ku)
        self.hud = Label(text="二段ジャンプ可／速度関数はDay2で拡張", pos=(12, HEIGHT-28)); self.add_widget(self.hud)
        Clock.schedule_interval(self.update, 1/60)
    def _kd(self,win,key,*a):
        self.keys.add(key)
        if key==32:
            if self.y<=self.ground+0.01:      # 地面
                self.vy=JUMP_VEL; self.can_double=True
            elif self.can_double:             # 二段
                self.vy=JUMP_VEL*0.9; self.can_double=False
        return True
    def _ku(self,win,key,*a):
        self.keys.discard(key); return True
    def update(self,dt):
        self.scroll += SPEED
        if self.y>self.ground:
            self.vy -= GRAVITY; self.y += self.vy
        if self.y <= self.ground:
            self.y = self.ground; self.vy = 0.0; self.can_double=False
        self.draw()
    def draw(self):
        self.canvas.clear()
        with self.canvas:
            Color(*BG); Rectangle(pos=self.pos, size=self.size)
            Color(0.10,0.13,0.2,1)
            for i in range(12):
                x = - (self.scroll*0.5 % 160) + i*160
                Rectangle(pos=(x, 360), size=(140, 2))
            Color(0.14,0.18,0.28,1)
            for i in range(12):
                x = - (self.scroll*0.8 % 220) + i*220
                Rectangle(pos=(x, 260), size=(180, 3))
            Color(0.25,0.8,0.9,1); Rectangle(pos=(0, self.ground-6), size=(self.width, 6))
            Color(0.95,0.2,0.6,1); Rectangle(pos=(self.x,self.y), size=(self.w,self.h))
class AppDay1(App): 
    def build(self): return Game()
if __name__=="__main__": AppDay1().run()
