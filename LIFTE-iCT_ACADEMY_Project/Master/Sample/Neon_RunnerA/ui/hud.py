# -*- coding: utf-8 -*-
# Score/Energy の表示だけを担当。更新は PlayScene 側で行う。

from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.core.window import Window

def build_hud():
    return Label(text="Score: 0   Energy: 100",
                 size_hint=(1, None), height=dp(32),
                 pos=(0, Window.height - dp(40)))
