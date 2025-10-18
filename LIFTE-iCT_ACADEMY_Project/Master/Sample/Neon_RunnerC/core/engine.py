# -*- coding: utf-8 -*-
"""
engine.py（Kivy アプリの骨組み）
--------------------------------------------------------------------
■ なぜ / 目的
  - Kivy の App と ScreenManager をまとめ、最初の画面（PlayScreen）を登録する。

■ 前提 / 依存
  - Kivy がインストール済みであること（pip install kivy）。
  - scenes.play 内に PlayScreen が定義されていること。

■ 入出力
  - 入力: なし
  - 出力: App.build() が ScreenManager（最初のシーンを含む）を返す。

■ 副作用
  - Kivy のウィンドウ生成、内部のイベントループ開始。

■ 例外
  - Kivy 未導入時: ImportError
"""
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

# 相対 import（src には依存しない）
from ..scenes.play import PlayScreen

class GameApp(App):
    """
    ゲームアプリケーションクラス。
    - ScreenManager を用いて画面（Screen）を切り替えます。
    """
    title = "Neon Runner C (clean-jp)"

    def build(self) -> ScreenManager:
        """
        ScreenManager を生成して返します。
        - 必要に応じて今後、他の画面（TitleScreen, ResultScreen など）を追加してください。
        """
        sm = ScreenManager()
        sm.add_widget(PlayScreen(name="play"))
        return sm
