# -*- coding: utf-8 -*-
# Day2 エントリポイント（Day1は main_day1.py を温存）
from kivymd.app import MDApp
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window

from .config import P
from .scenes.play import PlayScene

class Root(FloatLayout):
    pass

class App(MDApp):
    def build(self):
        Window.size = (P.WINDOW_W, P.WINDOW_H)
        root = Root()
        # Day2は PlayScene を直接開始（タイトルはDay3以降で強化予定）
        self.scene = PlayScene()
        self.scene.on_enter(root, engine=None)
        return root

if __name__ == "__main__":
    App().run()
