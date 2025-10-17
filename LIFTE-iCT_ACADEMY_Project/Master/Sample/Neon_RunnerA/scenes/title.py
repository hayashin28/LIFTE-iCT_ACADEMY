# -*- coding: utf-8 -*-
# タイトル画面：Enter/Space/タッチで開始。

from kivy.uix.label import Label
from kivy.metrics import dp

class TitleScene:
    def __init__(self, play_scene_factory):
        self.play_scene_factory = play_scene_factory
        self.root = None
        self.engine = None

    def on_enter(self, root_widget, engine):
        self.root = root_widget
        self.engine = engine
        self.lbl = Label(text='[ Neon Runner A / Day1 ]\nPress Space/Enter/Touch',
                         halign='center', valign='middle',
                         size_hint=(1,1), font_size=dp(24))
        self.root.add_widget(self.lbl)

    def on_exit(self):
        pass

    def on_key_down(self, key):
        # Enter(13) / Space(32) で開始（環境により差あり。実機確認）
        if key in (13, 32):
            self.engine.set_scene(self.play_scene_factory())
            return True
        return False

    def on_touch_down(self, touch):
        self.engine.set_scene(self.play_scene_factory())
        return True

    def update(self, dt):
        pass
