from kivy.clock import Clock
from kivy.lang import Builder
from kivymd.app import MDApp # kivyMD のアプリの基底クラス
from kivymd.uix.button import (
    MDFlatButton,
    MDRaisedButton,
)

KV = '''
# ルートは縦並びの BoxLayout
BoxLayout:
    orientation: 'vertical'
    padding: 12
    spacing: 10

    # スコア表示ラベル（Python 側から text を差し替える）
    MDLabel:
        id: score_label
        text: "Score: 0"
        halign: 'center'

    # タイマー表示ラベル（同上）
    MDLabel:
        id: timer_label
        text: "Time: 0"
        halign: 'center'

    # 3x3 のボタンを並べるグリッド（中身の 9 ボタンは Python 側で生成して add）
    GridLayout:
        id: grid
        cols: 3
        spacing: 8
        size_hint_y: 0.7

    # Start ボタン（ここは背景色が効きやすい MDRaisedButton を採用）
    MDRaisedButton:
        text: 'Start'
        pos_hint: {'center_x': .5}
        on_release: app.start_game()  # ← アプリの start_game() を直接呼ぶ
'''


#--------------------
# チューニング用の定数
#--------------------
# ゲームの残り時間
GAME_SECONDS = 45
# ターゲットの出現感覚（秒）
SPAWN_INTERVAL = 1.5


class SimpleButtonGame(MDApp):
    
    def build(self):
        # ゲーム状態の初期化
        self.score = 0
        self.time_left = GAME_SECONDS
        self.active = -1 # 光っているボタンの番号 -1 (無効)
        
        # 画面を組み立てて参照を取る
        self.root = Builder.load_string(KV)
        grid = self.root.ids.grid
        
        # 3x3のボタンをPython側で作り出す → Grid に add する
        self.buttons = [] # 空のリストを用意
        for i in range(9):
            # MDFlatButtonのインスタンス化
            btn = MDFlatButton(text=str(i + 1), on_release=self.on_press)
            btn.index = i # どのボタンが自分自身あるかを覚えさせる
            grid.add_widget(btn) # 画面に配置する
            self.buttons.append(btn) # リストに追加する
        
        # 自分自身を戻す
        return self.root
    
    def start_game(self):
        # 見た目の初期化
        self.score = 0
        self.time_left = GAME_SECONDS
        self.root.ids.score_label.text = f'Score: {self.score}'
        self.root.ids.timer_label.text = f'Time: {self.time_left}'
        
        # 1秒ごとのタイマーを開始（既に動いていたら止めてから開始）
        if hasattr(self, 'tick'):
            self.tick.cancel()
        self.tick = Clock.schedule_interval(self._tick, 1)
        
        # 今はターゲットなし（-1）
        self.active = -1
        
    # 毎秒呼ばれる：残り時間を 1 減らして表示を更新
    # 0 になったら終了
    def _tick(self, dt):
        self.time_left -= 1
        self.root.ids.timer_label.text = f'Time: {self.time_left}'
        
        # 時間切れ：タイマー停止
        if self.time_left <= 0:
            if hasattr(self, 'tick'):
                self.tick.canel()