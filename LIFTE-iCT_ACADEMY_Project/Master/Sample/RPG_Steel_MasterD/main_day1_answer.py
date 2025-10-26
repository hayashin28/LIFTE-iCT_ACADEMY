# -*- coding: utf-8 -*-
"""Day1 模範：走る＋慣性＋摩擦＋Clamp 実装済（厚手コメント）"""
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, PushMatrix, PopMatrix, Translate
from kivy.uix.label import Label
from kivy.properties import ListProperty
from config import WIDTH, HEIGHT, TILE_SIZE, MAP_CSV, PLAYER_SPEED, RUN_MULTIPLIER, ACCEL, FRICTION, BG
from map_loader_kivy import load_csv_as_tilemap, load_tileset_regions

class Game(Widget):
    cam = ListProperty([0,0])
    def __init__(self, **kw):
        super().__init__(**kw)
        self.size=(WIDTH,HEIGHT)
        self.grid,self.rows,self.cols = load_csv_as_tilemap(MAP_CSV)
        self.tiles = load_tileset_regions()
        ts=TILE_SIZE
        self.px=ts*2; self.py=ts*2; self.w=ts-6; self.h=ts-6
        self.vx=0; self.vy=0; self.keys=set()
        Window.bind(on_key_down=self._kd, on_key_up=self._ku)
        self.hud = Label(text="Shift走る／慣性＋摩擦／Clamp 実装", pos=(12, HEIGHT-28)); self.add_widget(self.hud)
        Clock.schedule_interval(self.update, 1/60)
    def _kd(self,win,key,*a): self.keys.add(key); return True
    def _ku(self,win,key,*a): self.keys.discard(key); return True
    def update(self,dt):
        left=276; right=275; up=273; down=274; lshift=304; rshift=303
        ax=(1 if right in self.keys else 0)-(1 if left in self.keys else 0)
        ay=(1 if down  in self.keys else 0)-(1 if up   in self.keys else 0)
        speed = PLAYER_SPEED * (RUN_MULTIPLIER if (lshift in self.keys or rshift in self.keys) else 1.0)
        # 慣性＋摩擦（一次フィルタ）
        self.vx = self.vx*(1-ACCEL) + ax*speed*ACCEL
        self.vy = self.vy*(1-ACCEL) + ay*speed*ACCEL
        self.vx *= FRICTION; self.vy *= FRICTION
        # 位置更新
        self.px += self.vx; self.py += self.vy
        # Clamp（マップ端）
        map_w=self.cols*TILE_SIZE; map_h=self.rows*TILE_SIZE
        self.px = max(0, min(self.px, map_w-self.w))
        self.py = max(0, min(self.py, map_h-self.h))
        # カメラ
        self.cam[0]=max(0, self.px-self.width/2); self.cam[1]=max(0, self.py-self.height/2)
        self.draw()
    def draw(self):
        self.canvas.clear()
        with self.canvas:
            Color(*BG); Rectangle(pos=self.pos, size=self.size)
            PushMatrix(); Translate(-self.cam[0], -self.cam[1], 0)
            ts=TILE_SIZE
            for r,row in enumerate(self.grid):
                for c,tid in enumerate(row):
                    Rectangle(texture=self.tiles[tid], pos=(c*ts,r*ts), size=(ts,ts))
            Color(0.35,0.67,1,1); Rectangle(pos=(self.px,self.py), size=(self.w,self.h))
            PopMatrix()
class AppDay1(App):
    def build(self): return Game()
if __name__=="__main__": AppDay1().run()
