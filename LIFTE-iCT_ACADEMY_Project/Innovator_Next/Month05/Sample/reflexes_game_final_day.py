# Final_complete.py
# --------------------
# このファイルは「ボタン反応ゲーム」の最終完成形です。
# 目的：難易度切替・効果音・ハイスコア保存を追加し、完成度を高める。
# 機能：ターゲット出現、スコア加算、時間制限、効果音、ハイスコア記録、難易度選択。
# --------------------

import json  # ハイスコア保存用
import os    # ファイル存在確認用
import random
from kivy.clock import Clock
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivy.core.audio import SoundLoader  # 効果音再生用

# 画面レイアウト（KV言語）
KV = '''
BoxLayout:
    orientation: 'vertical'
    padding: 10
    spacing: 8

    BoxLayout:
        size_hint_y: None
        height: '40dp'
        spacing: 8
        MDRaisedButton:
            text: 'Start'
            on_release: app.start_game()
        MDRaisedButton:
            text: 'Easy'
            on_release: app.set_difficulty('easy')
        MDRaisedButton:
            text: 'Hard'
            on_release: app.set_difficulty('hard')
        MDLabel:
            id: high_label
            text: "High: 0"
            size_hint_x: .5
            halign: 'center'

    MDLabel:
        id: score_label
        text: "Score: 0"
        halign: 'center'
        font_style: 'H5'

    MDLabel:
        id: timer_label
        text: "Time: 0"
        halign: 'center'

    GridLayout:
        id: grid
        cols: 3
        spacing: 6
        size_hint_y: 0.7
'''

HIGHSCORE_FILE = 'highscore.json'  # ハイスコア保存ファイル名

class FinalGame(MDApp):
    def build(self):
        # 初期化
        self.score = 0
        self.time_left = 30
        self.active = -1
        self.difficulty = 'easy'  # 難易度（easy / hard）
        self.spawn_interval = 1.5

        # 画面構築
        self.root = Builder.load_string(KV)
        grid = self.root.ids.grid
        self.buttons = []

        # ボタン生成
        for i in range(9):
            b = MDFlatButton(text=str(i+1), on_release=self.on_press)
            b.index = i
            grid.add_widget(b)
            self.buttons.append(b)

        # 効果音読み込み（hit.wav を同じフォルダに置く）
        self.hit_sound = SoundLoader.load('hit.wav')

        # ハイスコア読み込み
        self.load_highscore()
        self.update_high_label()

        return self.root

    def set_difficulty(self, level):
        # 難易度切替（Easy / Hard）
        self.difficulty = level
        if level == 'easy':
            self.spawn_interval = 1.5
            self.time_left = 30
        else:
            self.spawn_interval = 1.0
            self.time_left = 25
        self.root.ids.timer_label.text = f"Time: {self.time_left}"

    def start_game(self):
        # ゲーム開始処理
        self.score = 0
        self.root.ids.score_label.text = f"Score: {self.score}"

        # タイマーの重複防止
        if hasattr(self, 'tick'): self.tick.cancel()
        if hasattr(self, 'spawn'): self.spawn.cancel()

        # タイマー開始
        self.tick = Clock.schedule_interval(self._tick, 1)
        self.spawn = Clock.schedule_interval(self._spawn, self.spawn_interval)

        self.active = -1
        self.root.ids.timer_label.text = f"Time: {self.time_left}"

    def _tick(self, dt):
        # 毎秒呼ばれる：時間減少
        self.time_left -= 1
        self.root.ids.timer_label.text = f"Time: {self.time_left}"

        # 時間切れ処理
        if self.time_left <= 0:
            self.tick.cancel()
            self.spawn.cancel()
            if 0 <= self.active < len(self.buttons):
                self._set_normal(self.active)
            self.active = -1
            self.on_game_over()

    def _spawn(self, dt):
        # ターゲット出現処理
        if 0 <= self.active < len(self.buttons):
            self._set_normal(self.active)
        idx = random.randrange(len(self.buttons))
        self.active = idx
        self._set_active(idx)

    def _set_active(self, idx):
        # ボタンを光らせる
        b = self.buttons[idx]
        b.text = "●"
        b.theme_text_color = "Custom"
        b.text_color = (1,1,1,1)
        b.md_bg_color = [1, 0, 0, 1]

    def _set_normal(self, idx):
        # ボタンを元に戻す
        b = self.buttons[idx]
        b.text = str(idx+1)
        b.theme_text_color = "Primary"
        b.md_bg_color = [1,1,1,1]

    def on_press(self, instance):
        # ボタン押下時の処理
        if getattr(instance, 'index', -1) == self.active and self.time_left > 0:
            self.score += 1
            self.root.ids.score_label.text = f"Score: {self.score}"
            if self.hit_sound: self.hit_sound.play()  # 効果音再生
            self._set_normal(self.active)
            self.active = -1

    def load_highscore(self):
        # ハイスコア読み込み
        try:
            if os.path.exists(HIGHSCORE_FILE):
                with open(HIGHSCORE_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.high = data.get('high', 0)
            else:
                self.high = 0
        except:
            self.high = 0

    def save_highscore(self):
        # ハイスコア保存
        try:
            with open(HIGHSCORE_FILE, 'w', encoding='utf-8') as f:
                json.dump({'high': self.high}, f)
        except:
            pass

    def update_high_label(self):
        # ハイスコア表示更新
        self.root.ids.high_label.text = f"High: {self.high}"

    def on_game_over(self):
        # ゲーム終了時の処理
        if self.score > getattr(self, 'high', 0):
            self.high = self.score
            self.save_highscore()
            self.update_high_label()

        # 結果をダイアログ表示
        from kivymd.uix.dialog import MDDialog
        dlg = MDDialog(title="Game Over", text=f"Your score: {self.score}\nHigh: {self.high}")
        dlg.open()

if __name__ == '__main__':
    FinalGame().run()
