from kivy.uix.screenmanager import Screen
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout

TILE_SIZE = 32
KEYS = {'up':('up','w'), 'down':('down','s'), 'left':('left','a'), 'right':('right','d'), 'battle':('b',)}

class FieldScreen(Screen):
    def __init__(self, director, **kwargs):
        super().__init__(**kwargs); self.director=director; self._keyboard=None; self.info_bar=None
    def on_pre_enter(self, *args): self._ensure_keyboard(); self._build_ui(); self._draw_map()
    def on_leave(self, *args): self._release_keyboard()
    def _build_ui(self):
        self.canvas.clear()
        layout = MDBoxLayout(orientation="vertical")
        self.info_bar = MDLabel(text=f"[{self.director.classroom_name}] Map: {self.director.current_map} | Bでバトル", halign="center")
        layout.add_widget(self.info_bar); self.add_widget(layout)
    def _ensure_keyboard(self):
        if self._keyboard is None:
            self._keyboard = Window.request_keyboard(self._on_keyboard_closed, self)
            if self._keyboard: self._keyboard.bind(on_key_down=self._on_key_down)
    def _release_keyboard(self):
        if self._keyboard: self._keyboard.unbind(on_key_down=self._on_key_down); self._keyboard=None
    def _on_keyboard_closed(self): self._release_keyboard()
    def _on_key_down(self, keyboard, keycode, text, modifiers):
        keyname=keycode[1].lower()
        dx=dy=0
        if keyname in KEYS['up']: dy=-1
        elif keyname in KEYS['down']: dy=1
        elif keyname in KEYS['left']: dx=-1
        elif keyname in KEYS['right']: dx=1
        elif keyname in KEYS['battle']: self.manager.current='battle'; return True
        if dx or dy:
            res=self.director.try_move(dx,dy); self._draw_map()
            ev=res.get('event')
            if ev:
                if ev.get('type')=='message': self.info_bar.text=ev.get('text','イベント')
                elif ev.get('type')=='warp': self.info_bar.text=f"{self.director.current_map} に到着"; self._draw_map()
        return True
    def _draw_map(self):
        grid=self.director.grid; px,py=self.director.player_pos
        self.canvas.clear()
        with self.canvas:
            h=len(grid); w=len(grid[0]) if h else 0
            for y in range(h):
                for x in range(w):
                    t=grid[y][x]
                    if t==1: Color(0.25,0.55,0.85,1)
                    elif t==2: Color(0.45,0.9,0.45,1)
                    else: Color(0.12,0.12,0.12,1)
                    Rectangle(pos=(x*TILE_SIZE,(h-1-y)*TILE_SIZE+40), size=(TILE_SIZE,TILE_SIZE))
            Color(0.95,0.85,0.2,1)
            Rectangle(pos=(px*TILE_SIZE,(h-1-py)*TILE_SIZE+40), size=(TILE_SIZE,TILE_SIZE))
        if self.info_bar: self.info_bar.text = f"[{self.director.classroom_name}] Map: {self.director.current_map} | x={px} y={py}"