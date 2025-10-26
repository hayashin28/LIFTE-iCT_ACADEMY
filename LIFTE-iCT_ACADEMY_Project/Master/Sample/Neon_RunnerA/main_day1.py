# -*- coding: utf-8 -*-
# エントリポイント。EngineにTitleScene→PlaySceneを接続。

from kivymd.app import MDApp
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window

from .config import P
from .core.engine import Engine
from .scenes.title import TitleScene
from .scenes.play import PlayScene

class Root(FloatLayout):
    pass

class App(MDApp):
    def build(self):
        Window.size = (P.WINDOW_W, P.WINDOW_H)
        root = Root()
        self.engine = Engine(root)
        self.engine.set_scene(TitleScene(lambda: PlayScene()))
        return root

if __name__ == "__main__":
    App().run()
