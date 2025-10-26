# -*- coding: utf-8 -*-
import json, os
from kivy.core.window import Window
from kivy.properties import NumericProperty, StringProperty, ListProperty
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel

from ui.widgets.compass import Compass

# 設定
BLOCK_WALLS = True  # 壁にぶつかれない（Falseにすると初日仕様の「範囲チェックのみ」）

class DungeonScreen(MDScreen):
    x = NumericProperty(1)
    y = NumericProperty(1)
    facing = StringProperty("N")
    grid = ListProperty([])  # 0=floor, 1=wall
    w = NumericProperty(10)
    h = NumericProperty(10)

    def on_pre_enter(self, *args):
        self.clear_widgets()

        # マップ読込（失敗時はフォールバックで外周壁）
        self._load_map()

        root = MDBoxLayout(orientation="vertical", padding="12dp", spacing="8dp")
        hud = MDBoxLayout(orientation="horizontal", spacing="8dp", size_hint_y=None, height="48dp")
        self.compass = Compass(direction=self.facing)
        self.status = MDLabel(text=self._status_text(), halign="left")
        hud.add_widget(self.compass)
        hud.add_widget(self.status)

        self.map_label = MDLabel(text=self._map_ascii(), halign="left")
        root.add_widget(hud)
        root.add_widget(self.map_label)
        self.add_widget(root)

        # キーボード取得
        self._keyboard = Window.request_keyboard(self._kb_closed, self, 'text')
        if self._keyboard:
            self._keyboard.bind(on_key_down=self._on_key_down)

    def on_leave(self, *args):
        if getattr(self, "_keyboard", None):
            self._keyboard.unbind(on_key_down=self._on_key_down)
            self._keyboard = None

    def _kb_closed(self, *a):
        self._keyboard = None

    # ---- map ----
    def _load_map(self):
        path = os.path.join(os.path.dirname(__file__), "..", "maps", "dungeon_01.json")
        path = os.path.normpath(path)
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.w = int(data.get("width", 10))
            self.h = int(data.get("height", 10))
            self.grid = data.get("tiles") or [[1 if (i in (0,self.w-1) or j in (0,self.h-1)) else 0 for i in range(self.w)] for j in range(self.h)]
        except Exception:
            self.w, self.h = 10, 10
            self.grid = [[1 if (i in (0,9) or j in (0,9)) else 0 for i in range(10)] for j in range(10)]

    def is_wall(self, i, j):
        if not (0 <= i < self.w and 0 <= j < self.h):  # out of range is wall-like
            return True
        try:
            return int(self.grid[j][i]) == 1
        except Exception:
            return False

    # ---- input ----
    def _on_key_down(self, *args):
        _, keycode, text, modifiers = args
        key = keycode[1]
        dx = dy = 0
        if key in ("up", "w"):
            dy = -1; self.facing = "N"
        elif key in ("down", "s"):
            dy = 1; self.facing = "S"
        elif key in ("left", "a"):
            dx = -1; self.facing = "W"
        elif key in ("right", "d"):
            dx = 1; self.facing = "E"
        else:
            return False

        nx, ny = self.x + dx, self.y + dy
        if 0 <= nx < self.w and 0 <= ny < self.h:
            if (not BLOCK_WALLS) or (not self.is_wall(nx, ny)):
                self.x, self.y = nx, ny

        self._refresh_hud()
        return True

    # ---- ui ----
    def _refresh_hud(self):
        self.status.text = self._status_text()
        self.compass.direction = self.facing
        self.map_label.text = self._map_ascii()

    def _status_text(self):
        return f"Pos: ({self.x},{self.y})  Facing: {self.facing}"

    def _map_ascii(self):
        rows = []
        for j in range(self.h):
            row = []
            for i in range(self.w):
                if i == self.x and j == self.y:
                    row.append("P")
                else:
                    row.append("#" if self.is_wall(i, j) else ".")
            rows.append("".join(row))
        return "\\n".join(rows)
