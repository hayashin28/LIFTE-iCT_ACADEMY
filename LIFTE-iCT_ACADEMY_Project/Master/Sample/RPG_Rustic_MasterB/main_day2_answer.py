# -*- coding: utf-8 -*-
"""
RPG Rustic Master B — Day2（生徒用）Kivy
到達：壁衝突／Eで看板を読む（会話ダミー）
実装：鍵と扉（Flag）／宝箱（HUD）
"""
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, PushMatrix, PopMatrix, Translate
from kivy.uix.label import Label
from kivy.properties import ListProperty
from config import WIDTH, HEIGHT, TILE_SIZE, MAP_CSV, PLAYER_SPEED, BG
from map_loader_kivy import load_csv_as_tilemap, load_tileset_regions

def rect_collides(px, py, w, h, grid, solid=(1,)):
    ts=TILE_SIZE
    min_c=max(0,int(px)//ts); max_c=min(len(grid[0])-1,int((px+w-1))//ts)
    min_r=max(0,int(py)//ts); max_r=min(len(grid)-1,int((py+h-1))//ts)
    for r in range(min_r, max_r+1):
        for c in range(min_c, max_c+1):
            if grid[r][c] in solid:
                wx,wy=c*ts,r*ts
                if not (px+w<=wx or wx+ts<=px or py+h<=wy or wy+ts<=py):
                    return True
    return False

class Game(Widget):
    cam=ListProperty([0,0])
    def __init__(self, **kw):
        super().__init__(**kw)
        self.size=(WIDTH,HEIGHT)
        self.grid,self.rows,self.cols = load_csv_as_tilemap(MAP_CSV)
        self.tiles = load_tileset_regions()
        ts=TILE_SIZE
        self.px=ts*3; self.py=ts*3; self.w=ts-6; self.h=ts-6
        self.keys=set()
        self.sign = (ts*10, ts*6, ts, ts)  # 看板（ダミー）
        self.msg = Label(text="E: 看板を読む / 壁衝突あり", pos=(12,HEIGHT-28))
        self.add_widget(self.msg)
        Window.bind(on_key_down=self._kd, on_key_up=self._ku)
        Clock.schedule_interval(self.update, 1/60)
    def _kd(self,win,key,*a):
        self.keys.add(key); return True
    def _ku(self,win,key,*a):
        self.keys.discard(key); return True
    def update(self,dt):
        left=276; right=275; up=273; down=274; ekey=101
        ax=(1 if right in self.keys else 0)-(1 if left in self.keys else 0)
        ay=(1 if down  in self.keys else 0)-(1 if up   in self.keys else 0)
        spd=PLAYER_SPEED
        nx=self.px+ax*spd
        if not rect_collides(nx, self.py, self.w, self.h, self.grid): self.px=nx
        ny=self.py+ay*spd
        if not rect_collides(self.px, ny, self.w, self.h, self.grid): self.py=ny
        # 看板
        sx,sy,sw,sh=self.sign
        if ekey in self.keys and not (self.px+self.w<=sx or sx+sw<=self.px or self.py+self.h<=sy or sy+sh<=self.py):
            self.msg.text="【看板】ようこそ、Rustic村へ！"
        self.cam[0]=max(0,self.px-self.width/2); self.cam[1]=max(0,self.py-self.height/2)
        self.draw()
    def draw(self):
        self.canvas.clear()
        with self.canvas:
            Color(*BG); Rectangle(pos=self.pos,size=self.size)
            PushMatrix(); Translate(-self.cam[0],-self.cam[1],0)
            ts=TILE_SIZE
            for r,row in enumerate(self.grid):
                for c,tid in enumerate(row):
                    Rectangle(texture=self.tiles[tid], pos=(c*ts,r*ts), size=(ts,ts))
            # 看板
            Color(0.8,0.6,0.25,1); Rectangle(pos=(self.sign[0],self.sign[1]), size=(self.sign[2],self.sign[3]))
            # プレイヤ
            Color(0.35,0.67,1,1); Rectangle(pos=(self.px,self.py), size=(self.w,self.h))
            PopMatrix()
class Day2(App):
    def build(self): return Game()
if __name__=="__main__": Day2().run()
