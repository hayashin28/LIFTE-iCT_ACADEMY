# -*- coding: utf-8 -*-
"""Day2 模範：壁衝突（軸分離）＋会話ダミー＋NPC矩形"""
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, PushMatrix, PopMatrix, Translate
from kivy.uix.label import Label
from kivy.properties import ListProperty
from config import WIDTH, HEIGHT, TILE_SIZE, MAP_CSV, PLAYER_SPEED, RUN_MULTIPLIER, ACCEL, FRICTION, BG
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
    cam = ListProperty([0,0])
    def __init__(self, **kw):
        super().__init__(**kw)
        self.size=(WIDTH,HEIGHT)
        self.grid,self.rows,self.cols = load_csv_as_tilemap(MAP_CSV)
        self.tiles = load_tileset_regions()
        ts=TILE_SIZE
        self.px=ts*3; self.py=ts*3; self.w=ts-6; self.h=ts-6
        self.vx=0; self.vy=0; self.keys=set()
        self.npcs=[(ts*10,ts*6,ts-6,ts-6),(ts*14,ts*8,ts-6,ts-6)]
        Window.bind(on_key_down=self._kd, on_key_up=self._ku)
        self.hud = Label(text="E近接会話／衝突OK", pos=(12, HEIGHT-28)); self.add_widget(self.hud)
        Clock.schedule_interval(self.update, 1/60)
    def _kd(self,win,key,*a): self.keys.add(key); return True
    def _ku(self,win,key,*a): self.keys.discard(key); return True
    def update(self,dt):
        left=276; right=275; up=273; down=274; ekey=101
        ax=(1 if right in self.keys else 0)-(1 if left in self.keys else 0)
        ay=(1 if down  in self.keys else 0)-(1 if up   in self.keys else 0)
        speed = PLAYER_SPEED
        self.vx=ax*speed; self.vy=ay*speed
        nx=self.px+self.vx
        if not rect_collides(nx, self.py, self.w, self.h, self.grid): self.px=nx
        ny=self.py+self.vy
        if not rect_collides(self.px, ny, self.w, self.h, self.grid): self.py=ny
        if ekey in self.keys:
            for (nxp,nyp,nw,nh) in self.npcs:
                if not (self.px+self.w<=nxp or nxp+nw<=self.px or self.py+self.h<=nyp or nyp+nh<=self.py):
                    self.hud.text="NPC：こんにちは！（会話ダミー）"; break
        self.cam[0]=max(0,self.px-self.width/2); self.cam[1]=max(0,self.py-self.height/2)
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
            Color(0.31,0.78,0.47,1)
            for (nxp,nyp,nw,nh) in self.npcs:
                Rectangle(pos=(nxp,nyp), size=(nw,nh))
            Color(0.35,0.67,1,1); Rectangle(pos=(self.px,self.py), size=(self.w,self.h))
            PopMatrix()
class AppDay2(App):
    def build(self): return Game()
if __name__=="__main__": AppDay2().run()
