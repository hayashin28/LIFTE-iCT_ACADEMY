# -*- coding: utf-8 -*-
"""
play.py（最小のプレイ画面）
--------------------------------------------------------------------
■ なぜ / 目的
  - 配線（import・起動経路）が正しく動いているかを、最小実装で可視化する。

■ 前提 / 依存
  - Kivy: Screen / Label を利用。
  - config: 画面表示の文言に利用。

■ 入出力
  - 入力: なし
  - 出力: 画面中央に状態ラベルを表示。

■ 副作用
  - 画面遷移（on_enter）が走る度にラベルを張り替え。

■ 例外
  - Kivy 未導入: ImportError
"""
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label

# ルートパッケージ直下の config を相対 import（src 依存なし）
from .. import config

class PlayScreen(Screen):
    """
    最小動作のプレイ画面。
    - 実装が増えても「ここが入口」という目印を残しましょう。
    """
    def on_enter(self) -> None:
        """
        画面に入ったタイミングで呼ばれるフック。
        - 将来的にはここでステージ初期化、BGM 再生などに繋げるイメージ。
        """
        # 既存ウィジェットをクリアしてから、状態ラベルを追加
        self.clear_widgets()
        self.add_widget(Label(
            text=f"{config.APP_NAME} Ready  v{config.VERSION}",
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            font_size="24sp"
        ))
