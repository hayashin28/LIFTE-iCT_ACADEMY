# Homework_version.py
# --------------------
# このファイルは「ボタン反応ゲーム」の宿題完成形です。
# 目的：ランダムに光るボタンを出現させ、正しく押すとスコアが加算される。
# 機能：ターゲット出現、スコア加算、時間制限、Startボタンでゲーム開始。
# --------------------

from kivy.clock import Clock  # 時間制御（タイマー）に使う
from kivy.lang import Builder  # 画面レイアウトを文字列で定義するために使う
from kivymd.app import MDApp  # KivyMD の基本アプリクラス
from kivymd.uix.button import MDFlatButton  # mdflatbutton を使うための部品
import random  # ランダムな数字を作るために使う

# KV文字列：画面の見た目を定義します
KV = '''
BoxLayout:
    orientation: 'vertical'
    padding: 12
    spacing: 10

    MDLabel:
        id: score_label
        text: "Score: 0"
        halign: 'center'

    MDLabel:
        id: timer_label
        text: "Time: 0"
        halign: 'center'

    GridLayout:
        id: grid
        cols: 3
        spacing: 8
        size_hint_y: 0.7

    MDRaisedButton:
        text: 'Start'
        pos_hint: {'center_x': .5}
        on_release: app.start_game()
'''

class HomeworkGame(MDApp):
    def build(self):
        # 初期値の設定
        self.score = 0  # スコア
        self.time_left = 45  # 残り時間（秒）
        self.active = -1  # 現在光っているボタンの番号（なければ -1）

        # 画面を作る
        self.root = Builder.load_string(KV)
        grid = self.root.ids.grid  # グリッド領域を取得

        # ボタンを9個作って並べる
        self.buttons = []
        for i in range(9):
            b = MDFlatButton(text=str(i+1), on_release=self.on_press)  # ボタンに番号と押したときの動作を設定
            b.index = i  # 自分の番号を記録（後で判定に使う）
            grid.add_widget(b)  # グリッドに追加
            self.buttons.append(b)  # リストに保存（後で操作するため）

        return self.root

    def start_game(self):
        # ゲーム開始時の初期化
        self.score = 0
        self.time_left = 45
        self.root.ids.score_label.text = f"Score: {self.score}"
        self.root.ids.timer_label.text = f"Time: {self.time_left}"

        # すでにタイマーが動いていたら止める（2重起動防止）
        if hasattr(self, 'tick'): self.tick.cancel()
        if hasattr(self, 'spawn'): self.spawn.cancel()

        # 1秒ごとに時間を減らす処理を開始
        self.tick = Clock.schedule_interval(self._tick, 1)

        # 1.5秒ごとにターゲット（光るボタン）を出す処理を開始
        self.spawn = Clock.schedule_interval(self._spawn, 1.5)

        self.active = -1  # 最初は光っているボタンなし

    def _tick(self, dt):
        # 毎秒呼ばれる：残り時間を減らす
        self.time_left -= 1
        self.root.ids.timer_label.text = f"Time: {self.time_left}"

        # 時間切れになったらゲーム終了
        if self.time_left <= 0:
            self.tick.cancel()
            self.spawn.cancel()
            if 0 <= self.active < len(self.buttons):
                self._set_normal(self.active)  # 光っていたボタンを元に戻す
            self.active = -1

    def _spawn(self, dt):
        # 毎回呼ばれる：ターゲットを1つ選んで光らせる

        # 前のターゲットがあれば元に戻す
        if 0 <= self.active < len(self.buttons):
            self._set_normal(self.active)

        # 新しいターゲットをランダムに選ぶ
        idx = random.randrange(len(self.buttons))
        self.active = idx
        self._set_active(idx)

    def _set_active(self, idx):
        # 指定したボタンを「光らせる」処理
        b = self.buttons[idx]
        b.text = "●"  # 見た目を変える
        b.theme_text_color = "Custom"
        b.text_color = (1,1,1,1)
        b.md_bg_color = [1, 0, 0, 1]  # 赤色にする

    def _set_normal(self, idx):
        # 指定したボタンを「元に戻す」処理
        b = self.buttons[idx]
        b.text = str(idx+1)
        b.theme_text_color = "Primary"
        b.md_bg_color = [1,1,1,1]  # 白色に戻す

    def on_press(self, instance):
        # ボタンが押されたときの処理

        # 押したボタンが現在のターゲットならスコア加算
        if getattr(instance, 'index', -1) == self.active and self.time_left > 0:
            self.score += 1
            self.root.ids.score_label.text = f"Score: {self.score}"
            self._set_normal(self.active)  # 光っていたボタンを元に戻す
            self.active = -1  # 次のターゲット待ち

if __name__ == '__main__':
    HomeworkGame().run()
