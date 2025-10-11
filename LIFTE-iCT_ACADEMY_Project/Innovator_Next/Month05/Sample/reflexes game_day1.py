# Day1_with_hints_annotated.py
# ============================================================
# 授業用：初日完成＋「宿題の入口」つき・詳細コメント版
# ねらい：
#   1) 3x3 のボタンを並べて、Start でタイマーが減るところまで完成（初日ゴール）
#   2) 宿題の導入として、ランダム点灯処理の「フック（_spawn/_set_active/_set_normal）」を
#      先に“空の関数”として書き、コメントを読めば方針が分かる状態で帰宅してもらう
# 使い方：
#   - このファイルだけで実行可
#   - 宿題では TODO の中身を埋める
# ============================================================

from kivy.clock import Clock            # Kivy のスケジューラ：一定間隔で関数を呼ぶ
from kivy.lang import Builder           # KV 文字列を読み込んで画面を組み立てる
from kivymd.app import MDApp            # KivyMD のアプリ基底クラス
from kivymd.uix.button import (         # ボタン部品（授業中の比較のため両方 import）
    MDFlatButton,                       # フラット：背景色が効きにくい端末あり
    MDRaisedButton,                     # レイズド：背景色 md_bg_color が効きやすい
)

# ----------------------
# チューニング用の定数
# ----------------------
GAME_SECONDS = 45        # ゲームの残り時間（秒）。宿題で変更してもよい
SPAWN_INTERVAL = 1.5     # ターゲット出現の間隔（秒）。初日は未使用（宿題で使う）

# --------------------------------------
# 画面レイアウト（KV Language で宣言）
#   - 「ツリー（どの部品をどこに置くか）」を宣言的に記述
#   - Python 側ではロジック（タイマー/判定）を担当
# ポイント：
#   - ids: で Python から部品を参照（score_label / timer_label / grid）
#   - Start ボタンは KV から app.start_game() を呼ぶ
# --------------------------------------
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


class SimpleButtonGame(MDApp):
    """
    アプリ本体（MDApp 継承）

    なぜ：
        画面（KV）とロジック（Python）を分離しつつ、ゲーム状態を一元管理するため。

    前提：
        - 3x3 = 9 個のボタンを GridLayout に並べる。
        - 各ボタンには 0〜8 の index を持たせ、押下時にどれが押されたか判定できるようにする。
        - Kivy のスケジューラ（Clock）で 1秒ごとの tick を回す。
        - 宿題では別スケジューラで「ランダム点灯（_spawn）」を回す。

    入出力：
        - 入力：ユーザーのボタン押下（on_press）
        - 出力：ラベルのテキスト更新（スコア/タイマー）、コンソール出力（初日は print）

    副作用：
        - start_game() でスケジューラを起動・停止（多重起動を避けるため cancel してから start）
        - _tick() で残り時間を更新し、0 で停止
        - （宿題）_spawn() でターゲット点灯/消灯

    例外・注意：
        - スケジューラの多重起動に注意：再開前に cancel を行う（hasattr で存在チェック）
        - index の範囲チェック：0 <= active < len(self.buttons) を都度確認
    """

    def build(self):
        """
        画面を構築して root を返す。

        なぜ：
            KV で宣言したツリーを読み込み、Python 側で 9 ボタンを生成して Grid に追加するため。

        前提：
            - KV の ids から grid/score_label/timer_label を参照する。
            - ボタンには .index を付与して押下判定に使う。

        入出力：
            戻り値：ルートウィジェット（App が画面として使う）

        副作用：
            self.root / self.buttons / self.score / self.time_left / self.active を初期化

        例外：
            特になし（KV の読み込み失敗時は例外が出るので授業ではコピー漏れに注意）
        """
        # ゲーム状態の初期化
        self.score = 0
        self.time_left = GAME_SECONDS
        self.active = -1       # 光っているボタンの番号。ないときは -1（無効値）

        # 画面を組み立てて参照を取る
        self.root = Builder.load_string(KV)
        grid = self.root.ids.grid

        # 3x3 = 9 個のボタンを Python 側で生成 → Grid に add
        # メモ：MDFlatButton は“背景色が効かない端末”があるため、
        #       宿題で「光らせる（md_bg_color）」を使いたい場合は MDRaisedButton に変えてもよい。
        self.buttons = []
        for i in range(9):
            btn = MDFlatButton(text=str(i + 1), on_release=self.on_press)
            btn.index = i  # どのボタンかを自分自身に覚えさせる（押下判定に使う）
            grid.add_widget(btn)
            self.buttons.append(btn)

        return self.root

    def start_game(self):
        """
        Start ボタン押下時：ゲーム開始の初期化とタイマー起動

        なぜ：
            毎回同じ初期状態からスタートし、授業中の動作確認を安定させる。

        前提：
            - tick（1秒ごと）以外に、宿題用の spawn（1.5秒ごと）を後日追加予定。

        入出力：
            表示ラベルを現在値に更新

        副作用：
            既存のスケジューラがあれば cancel（多重起動防止）→ 新規に schedule_interval

        例外：
            特になし
        """
        # 見た目の初期化
        self.score = 0
        self.time_left = GAME_SECONDS
        self.root.ids.score_label.text = f"Score: {self.score}"
        self.root.ids.timer_label.text = f"Time: {self.time_left}"

        # 1秒ごとのタイマーを開始（既に動いていたら止めてから開始）
        if hasattr(self, 'tick'):
            self.tick.cancel()
        self.tick = Clock.schedule_interval(self._tick, 1)

        # 宿題：ランダム点灯のスケジューラ（今日は OFF / 下の2行はコメントのまま）
        # if hasattr(self, 'spawn'):
        #     self.spawn.cancel()
        # self.spawn = Clock.schedule_interval(self._spawn, SPAWN_INTERVAL)

        # いまはターゲットなし（-1）
        self.active = -1

    def _tick(self, dt):
        """
        毎秒呼ばれる：残り時間を 1 減らして表示更新。0 になったら終了。

        なぜ：
            「Startで時間が減る」を体感させる（初日のゴール）。

        前提：
            - Kivy の Clock が 1秒ごとに dt（経過秒数）を渡して呼び出す。

        入出力：
            timer_label の text を更新

        副作用：
            time_left を書き換え、0 以下で tick を停止
            （宿題）点灯中なら元に戻す

        例外：
            特になし
        """
        self.time_left -= 1
        self.root.ids.timer_label.text = f"Time: {self.time_left}"

        # 時間切れ：タイマー停止。宿題では点灯も消す（_set_normal）
        if self.time_left <= 0:
            if hasattr(self, 'tick'):
                self.tick.cancel()
            # 宿題：点灯を戻す（今日は未実装）
            # if 0 <= self.active < len(self.buttons):
            #     self._set_normal(self.active)
            self.active = -1

    # ===================== 宿題フック（今日ここまで打ち込む） =====================

    def _spawn(self, dt):
        """
        【宿題】一定間隔で呼ばれる「ターゲット出現」処理

        なぜ：
            1.5 秒ごとにランダムで 1 個のボタンを「光らせる」ことで、反応ゲームにするため。

        前提：
            - self.buttons に 9 個のボタンが入っている
            - self.active に「前回の点灯位置」または -1 が入っている

        入出力：
            なし（UI の見た目を更新）

        副作用：
            - 前回の点灯があれば元に戻す（_set_normal）
            - 新しく選んだ位置を self.active に記録し、_set_active で光らせる

        例外：
            - 同じマスが連続しないようにするなら、random.choice で active 以外を選ぶ工夫をする
        """
        # TODO:
        # if 0 <= self.active < len(self.buttons):
        #     self._set_normal(self.active)
        # idx = random.randrange(len(self.buttons))
        # self.active = idx
        # self._set_active(idx)
        pass  # ← 宿題で上のコメントどおりに実装

    def _set_active(self, idx):
        """
        【宿題】指定 idx のボタンを「光らせる」見た目にする

        なぜ：
            当たりの場所が一目で分かるようにするため。

        前提：
            self.buttons[idx] が存在する

        入出力：
            なし（UI の見た目を更新）

        副作用：
            ボタンの text / 色 / 背景色 を変更
            ※ 注意：MDFlatButton は端末によって md_bg_color が効きにくい。
                    確実に背景色を変えたい場合は MDRaisedButton を使うか、
                    KV の canvas で矩形を敷く方法もある。

        例外：
            なし（範囲外アクセスに注意）
        """
        btn = self.buttons[idx]
        # 例（MDRaisedButton を想定）：
        # btn.text = "●"
        # btn.theme_text_color = "Custom"
        # btn.text_color = (1, 1, 1, 1)
        # btn.md_bg_color = [1, 0, 0, 1]  # 赤
        pass  # ← 宿題で実装

    def _set_normal(self, idx):
        """
        【宿題】指定 idx のボタンを「元の見た目」に戻す

        なぜ：
            次のターゲットを出す前に、前の光りを消して盤面を整えるため。

        前提：
            self.buttons[idx] が存在する

        入出力：
            なし（UI の見た目を更新）

        副作用：
            ボタンの text / 色 / 背景色 を元に戻す

        例外：
            なし
        """
        btn = self.buttons[idx]
        # 例（MDRaisedButton を想定）：
        # btn.text = str(idx + 1)
        # btn.theme_text_color = "Primary"
        # btn.md_bg_color = [1, 1, 1, 1]
        pass  # ← 宿題で実装

    # ============================================================================

    def on_press(self, instance):
        """
        ボタン押下時のコールバック（初日：押した番号をコンソール表示）

        なぜ：
            index が正しく入っているか確認し、イベント結線の感覚を掴む。

        前提：
            すべてのグリッドボタンに on_release=self.on_press が設定済み

        入出力：
            標準出力に "pressed <index>" を出す（初日）

        副作用：
            なし（宿題ではスコアを加算し、見た目を戻す）

        例外：
            なし
        """
        idx = getattr(instance, 'index', None)
        if idx is None:
            print("pressed (unknown)")
        else:
            print(f"pressed {idx + 1}")   # ← 表示は1〜9に

        # 宿題（当たり判定とスコア加算）：
        # if getattr(instance, 'index', -1) == self.active and self.time_left > 0:
        #     self.score += 1
        #     self.root.ids.score_label.text = f"Score: {self.score}"
        #     self._set_normal(self.active)
        #     self.active = -1


if __name__ == '__main__':
    # エントリポイント（Kivy アプリの起動）
    SimpleButtonGame().run()
