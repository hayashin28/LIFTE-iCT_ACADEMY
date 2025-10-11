from kivy.clock import Clock
from kivy.lang import Builder
from kivymd.app import MDApp # kivyMD のアプリの基底クラス
from kivymd.uix.button import (
    MDFlatButton,
    MDRaisedButton,
)

# ---------------------
# チューニング用の定数
#----------------------
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
            btn = MDFlatButton(text=str(i + 1), on_release=self.on_press)
