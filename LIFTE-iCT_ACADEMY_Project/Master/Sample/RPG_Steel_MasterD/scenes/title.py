# -*- coding: utf-8 -*-
"""
scenes/title.py – タイトル画面
なぜ: 起動確認とシーン遷移の動線を最小実装するため。
前提: Enter でフィールドへ。Esc で終了。
入出力: なし
副作用: アプリ終了（Esc）
例外: キー入力が取れない場合は request_keyboard の取得を再確認。
"""
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.clock import Clock

class TitleScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", padding=20, spacing=10)
        layout.add_widget(Label(text="[b]Steel MasterD[/b]", markup=True, font_size="28sp"))
        layout.add_widget(Label(text="Press [b]Enter[/b] → Field", markup=True))
        layout.add_widget(Label(text="Press [b]Esc[/b] → Quit", markup=True))
        self.add_widget(layout)

        # キーボード取得
        self._keyboard = None
        Clock.schedule_once(self._bind_keyboard, 0)

    def _bind_keyboard(self, *_):
        self._keyboard = Window.request_keyboard(self._on_keyboard_closed, self)
        if self._keyboard is not None:
            self._keyboard.bind(on_key_down=self._on_key_down)

    def _on_keyboard_closed(self):
        if self._keyboard is not None:
            self._keyboard.unbind(on_key_down=self._on_key_down)
            self._keyboard = None

    def _on_key_down(self, keyboard, keycode, text, modifiers):
        key, key_str = keycode  # (key_id, 'enter' 等)
        if key_str in ("enter", "numpadenter"):
            # フィールドへ
            self.manager.current = "field"
            return True
        if key_str == "escape":
            # 終了
            from kivy.app import App
            App.get_running_app().stop()
            return True
        return False
