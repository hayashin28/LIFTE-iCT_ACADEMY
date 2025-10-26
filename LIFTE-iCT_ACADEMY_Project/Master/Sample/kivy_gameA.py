from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDIconButton
from kivymd.uix.toolbar import MDToolbar
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import StringProperties, BooleanProperties, ObjectProperties
from kivy.clock import Clock
import random


KV = r'''
<GameCard>:
    # 個々のカード定義（MDCardベース）
    orientation: 'vertical'
    size_hint: None, None
    size: dp(80), dp(80)       # 表示サイズ
    focus_behavior: True       # タッチ応答
    ripple_behavior: True      # 波紋効果
    md_bg_color: app.theme_cls.primary_light   # 裏面の背景色
    elevation: 4
    on_release: app.on_card_click(root)        # クリック時の処理

    MDBoxLayout:
        orientation: 'vertical'
        padding: dp(10)
        MDLabel:
            id: card_icon_label
            text: ""                                # 表側に出す文字（is_flippedで切替）
            font_size: "48sp"
            halign: "center"
            valign: "center"
            theme_text_color: "Custom"
            text_color: app.theme_cls.primary_dark if root.is_flipped else [0.6, 0.6, 0.6, 0.5]

MDScreen:
    md_bg_color: app.theme_cls.colors.get('Blue', {}).get('100')

    MDBoxLayout:
        orientation: 'vertical'

        MDToolbar:
            title: "カードマッチ"
            md_bg_color: app.theme_cls.primary_color
            specific_text_color: app.theme_cls.accent_color
            elevation: 10

        MDLabel:
            id: status_label
            text: "スタートボタンを押してください。"
            halign: "center"
            font_style: "H6"
            theme_text_color: "Primary"
            size_hint_y: None
            height: dp(60)

        ScrollView:
            MDGridLayout:
                id: game_grid
                cols: 4
                spacing: dp(10)
                padding: dp(20)
                adaptive_height: True
                pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                size_hint_x: 0.9

        MDBoxLayout:
            adaptive_height: True
            padding: dp(10)
            MDRectangleFlatButton:
                text: "スタート"
                on_release: app.show_start_dialog()
                pos_hint: {'center_x': 0.5}
                size_hint_x: 0.8
                md_bg_color: app.theme_cls.accent_color
                text_color: app.theme_cls.text_color
'''


# ここがオブジェクト指向の極み
class GameCard(MDCard):
    # カードが持っている絵柄のアイコン名
    card_icon_name = StringProperties('')
    # カードがめくられているか
    is_flipped = BooleanProperties(False)
    # カードが揃っているか（見えなくする時に使う）
    is_matched = BooleanProperties(False)
    # 以降、振る舞い（メソッド）
    # オブジェクト（インスタンス）作成時にココを通る
    def __init__(self, icon_name, **kwargs):
        super().__init__(**kwargs)
        # このカードの絵柄を設定する
        self.card_icon_name = icon_name
        # 最初は裏向きにする
        self.unflip()

    def flip(self):
        if not self.is_matched:
            # カードをめくる（表にする）
            self.is_flipped = True
            # ラベルのテキストにアイコンを設定する
            self.ids_card_icon_label.text = f'[font=Icons][color={self.theme_cls.primary_dark}]{self.card_icon_name}[/color][/font]'
            # めくった後の色
            self.md_bg_color = self.theme_cls_primary_light
        
    def unflip(self):
        # 揃ったカードは裏にしない
        if not self.is_matched:
            # カードを元に戻す(裏返す)
            self.is_flipped = False
            # ラベルのテキストを空にする（背景色を裏向きにする）
            self.ids_card_icon_label.text = f'[font=Icons][color={self.theme_cls.text_color}]{'help-box'}[/color][/font]'
            # 裏返しの色
            self.md_bg_color = self.theme_cls.secondary_light
        
    def hide(self):
        # カードが揃ったら見えなくする（透明にして触れなくする）
        self.is_matched = True
        # 透明にする
        self.opacity = 0
        # 触れなくする
        self.disabled = True
        

# ゲームマスター
class MatchGameApp(MDApp):
    # ゲームの状態を管理する変数たち
    # 最初にめくったカード
    first_card = ObjectProperties(None)
    # ２番目にめくったカード
    second_card = ObjectProperties(None)
    # クリックできるかどうか
    can_click = BooleanProperties(True)
    # 揃ったペアの数
    matched_pairs = 0
    # 全ペアの数
    total_pairs = 0
    # どちらのターンか ’player’ or 'cpu'
    current_turn = StringProperties('player')

    def build(self):
        # メインカラーを水色に設定
        self.theme_cls.primary_palette = 'LightBlue'
        # アクセントカラーをピンクに
        self.theme_cls.accent_palette = 'Pink'
        # 明るいテーマにする
        self.theme_cls.theme_style = 'Light'
        return Builder.load_string(KV)

    def on_start(self):
        # アプリが始まったらゲーム説明のダイアログを表示
        self.show_start_dialog()
    
    def show_start_dialog(self):
        # ゲーム開始前のダイアログ
        dialog = MDDialog(
            title = '神経衰弱',
            text = '同じ絵柄のカードを見つけよう。\n\n1.カードを2枚めくって同じ絵柄だったら消えるよ！\n2.全部消せたらクリア！',
            buttons = [
                MDFlatButton(
                    text = 'スタート！',
                    on_release = lambda x:[dialog.dismis(), self.setup_game_board()] # ダイアログを閉じてゲーム開始
                )
            ]
        )
        dialog.open
    
    def setup_game_board(self):
        # ゲームで使うアイコンのリスト
        icons = ['flower','cat','dog','fish','star','heart','apple','car'] # 8種類
        # 各アイコンを2つずつ用意してペアにする
        game_icon = icons * 2 # 16枚のカードが出来上がる
        # シャッフルする
        random.shuffle()

        game_grid = self.root.ids.game_gird
        game_grid.clear_widgets()
        # ペアの数
        self.total_pairs = len(icons)

        # カードを生成してグリッドに追加する
        for icon_name in game_icon:
            # カードクラスをインスタンス化
            card = GameCard(icon_name=icon_name)
            # カードを盤面に配置する
            game_grid.add_widget(card)

        self.root.ids.status_label.text = 'あなたの番です！カードをめくってね。'
        self.first_card = None
        self.second_card = None
        self.can_click = True
        self.matched_pairs = 0
        self.current_turn = 'player' # 初手をプレイヤーのターンにする

    def on_card_click(self, card):
        # プレイヤーのターンじゃない、カードがめくられている、または既にそろっている
        # いずれかの条件を満たしたら何もしない
        if self.current_turn != 'player' or not self.can_click or card.is_flipped or card.is_matched:
            # 何もせずに終了する
            return
        
        # クリックされたカードを表にする
        card.flip()

        if self.first_card is None:
            # 1枚目をめくった時
            self.first_card = card
        else:
            # 2枚目のカードをめくった時
            self.second_card = card
            # 2枚カードをめくった時はクリックを不可とする
            self.can_click = False
            # カードの判定を行うメッセージを表示
            self.root.ids.status_label.text = '同じ絵柄かな？'
            # 0.8秒後にカードを比較する
            Clock.schedule_once(self.check_match, 0.8)
    
    # カード比較関数
    def check_match(self):
        # 2枚のカードの絵柄が同じかチェックする
        if self.first_card.card_icon_name == self.second_card.icon_name:
            # 同じ絵柄だったら、揃ったペアの数を増やす
            self.matched_pairs += 1
            # 1枚目のカードを隠す
            self.first_card.hide()
            # 2枚目のカードを隠す
            self.second_card.hide()
            # メッセージを表示する
            self.root.ids.status_label.text = '同じ絵柄が揃ったね！'
            if self.matched_pairs == self.total_pairs:
                # すべてのペアが揃ったらゲームクリア
                # 誰が勝ったかを引数で渡す
                self.show_win_dialog(winner=self.current_turn)
            else:
                # 揃ったら同じターンのまま継続
                if self.current_turn == 'player':
                    self.root.ids.status_label.text = 'もう一度あなたのターンです。カードをめくってね！'
                else:
                    self.root.ids.status_label.text = 'CPUが揃えたので、もう一度CPUのターン！'
                    # CPUが揃えたのでもう一度CPUのターン
                    Clock.schedule_once(self.cpu_turn, 1)

        else:
            # 違う絵柄だったら
            # 1枚目のカードを裏に戻す
            self.first_card.unflip()
            # 2枚目のカードも裏に戻す
            self.second_card.unflip()
            # メッセージを表示する
            self.root.ids.status_label.text = '残念！絵柄が揃わなかったね。'
            # ターンを切り替える
            self.switch_trun()
        
        # カードの状態をリセットする
        self.first_card = None
        self.second_card = None
        # クリックを許可する
        self.can_click = True
        
    # ターンを切り替える関数
    def switch_turn(self):
        if self.current_turn == 'player':
            self.current_turn == 'cpu'
            # メッセージを表示
            self.root.ids.status_label.text = '次はCPUの番です！'
            # 少し待ってからCPUのターンを開始する
            Clock.schedule_once(self.cpu_turn, 1.5) # 1.5秒待つ
        else:
            self.current_turn == 'player'
            self.root.ids.status_label.text = 'あなたの番です。カードをめくってね！'
        
    # CPUがカードをめくるロジック
    def cpu_turn(self):
        # CPUが操作中はプレイヤーがクリック出来ないようにする
        self.can_click = False
        # メッセージを表示
        self.root.ids.status_label.text = 'CPUがカードを選んでいます'
        # めくることができる裏向きのカードを探す
        available_cards = [
            card for card in self.root.ids.game_grid.children
            if not card.is_flipped and not card.is_matched
        ]               

        if len(available_cards) < 2:
            # ゲーム終了間際などでカードが足りない場合は何もしないでターン終了
            self.can_click =  True
            return

        # ランダムに2枚のカードを選択する
        # 同じカードを選ばないように、random.sampleを使う
        chosen_cards = random.sample(available_cards, 2)
        
        cpu_first_card = chosen_cards[0]
        cpu_second_card = chosen_cards[1]
        
        # 1枚目をめくる
        cpu_first_card.flip()
        self.first_card = cpu_first_card

        # 少し待ってから2枚目をめくる
        Clock.schedule_once(lambda x: self.cpu_flip_second(cpu_second_card), 1)
        
    def cpu_flip_second(self, card):
        # CPUが2枚目のカードをめくる
        card.flip()
        self.second_card = card
        self.root.ids.status_label.text = 'CPUがカードをめくりました！'
        # 0.8秒後にカードを比較する
        Clock.schedule_once(self.check_match, 0.8)

    def show_win_dialog(self, winner):
        # ゲームクリアのダイアログ
        if winner == 'player':
            title_text = 'あなたの勝ちです！おめでとう👺'
            message_text = 'もう一度、遊ぶ？'
        else:
            title_text = '残念！CPUの勝ちです🐽'
            message_text = 'もう一度、負けてみる？'
        
        dialog = MDDialog(
            title = title_text,
            text = message_text,
            button = [
                MDFlatButton(
                    text = 'もう一度',
                    on_release = lambda x: [dialog.dismiss(), self.setup_game_board]
                )
            ]
        )    
        
        dialog.open() 

if __name__ == '__main__':
    # アプリを起動する
    MatchGameApp().run()