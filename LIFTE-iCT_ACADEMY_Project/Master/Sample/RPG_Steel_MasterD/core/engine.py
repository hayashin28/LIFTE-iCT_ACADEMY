# -*- coding: utf-8 -*-
"""
core/engine.py – 画面遷移やアプリの土台
なぜ: 画面（シーン）を切り替える責務を分離し、main.py を細く保つため。
前提: Kivy の ScreenManager を使用。scenes で Screen を定義する。
入出力: なし（App.run() で起動）
副作用: ウィンドウ生成・イベントループ開始
例外: Screen の登録漏れや名前不一致に注意。
"""
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivy.core.window import Window

from src.config import WIDTH, HEIGHT
from src.scenes.title import TitleScreen
from src.scenes.field import FieldScreen

class GameScreenManager(ScreenManager):
    pass

class GameApp(App):
    def build(self):
        # ウィンドウサイズを config に合わせる（端末ごとに固定表示のため）
        Window.size = (WIDTH, HEIGHT)

        sm = GameScreenManager(transition=NoTransition())
        sm.add_widget(TitleScreen(name="title"))
        sm.add_widget(FieldScreen(name="field"))
        sm.current = "title"
        return sm

    def goto(self, screen_name: str):
        """画面遷移のユーティリティ"""
        self.root.current = screen_name
