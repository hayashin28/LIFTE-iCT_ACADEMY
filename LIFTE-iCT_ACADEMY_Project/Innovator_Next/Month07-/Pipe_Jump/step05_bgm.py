# step05_bgm.py
"""
Step05: BGM を追加するステップ

★ねらい
- 画面の内容(背景・雲・土管・レンガ)は Step04 とほぼ同じ
- そこに「音(BGM)」を足して、ゲームらしさを出す
"""

from pathlib import Path

from kivymd.app import MDApp as App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.core.audio import SoundLoader  # 音声ファイルを読み込んで再生するためのクラス


BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"
IMG_DIR = ASSETS_DIR / "img"
BGM_DIR = ASSETS_DIR / "bgm"


def first_existing(*candidates: Path) -> str:
    """画像や音声ファイル候補の中から、最初に見つかったものを返します。"""
    for p in candidates:
        if p.is_file():
            return str(p)
    raise FileNotFoundError(
        "必要なファイルが見つかりません。assets/img と bgm を確認してください。"
    )


def find_bgm() -> str:
    """
    BGMファイルを探します。

    優先順位:
      bgm.ogg / bgm.mp3 / bgm.wav
      main.ogg / main.mp3 / main.wav
    の順に「見つかったもの」を1つ選びます。
    """
    candidates = []
    for stem in ("bgm", "main"):
        for ext in (".ogg", ".mp3", ".wav"):
            candidates.append(BGM_DIR / f"{stem}{ext}")
    return first_existing(*candidates)


class StaticStage(Widget):
    """
    Step04 と同じ「静的ステージ」。
    背景・雲・土管・レンガを表示する役目だけを持ちます。
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        bg_path = first_existing(IMG_DIR / "bg.png", IMG_DIR / "bg.jpg")
        cloud_path = first_existing(IMG_DIR / "cloud.png")
        dokan_path = first_existing(IMG_DIR / "dokan.png")
        brick_path = first_existing(IMG_DIR / "brick_block.png")

        # 背景
        bg = Image(
            source=bg_path,
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1),
            pos=(0, 0),
        )
        self.add_widget(bg)

        # 雲
        for pos in [(80, 360), (420, 420), (720, 360)]:
            cloud = Image(
                source=cloud_path,
                size=(256, 96),
                pos=pos,
                size_hint=(None, None),
            )
            self.add_widget(cloud)

        # 土管
        pipe = Image(
            source=dokan_path,
            size=(64, 96),
            pos=(550, 0),
            size_hint=(None, None),
        )
        self.add_widget(pipe)

        # レンガ
        brick_y = 200
        brick_w, brick_h = 128, 32
        for i in range(4):
            x = 300 + i * brick_w
            brick = Image(
                source=brick_path,
                size=(brick_w, brick_h),
                pos=(x, brick_y),
                size_hint=(None, None),
            )
            self.add_widget(brick)


class Step05BgmApp(App):
    """
    Step05 用アプリ本体。

    - 起動時(on_start)に BGM をループ再生
    - 終了時(on_stop)に BGM を停止
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bgm = None  # あとで Sound オブジェクトを入れるための変数

    def build(self):
        Window.size = (960, 540)
        self.title = "Pipe & Jump 10 Lessons - Step05 BGM"
        return StaticStage()

    def on_start(self):
        """アプリ起動時に自動的に呼ばれます。ここで BGM を鳴らします。"""
        try:
            bgm_path = find_bgm()
        except FileNotFoundError as e:
            # BGM がなくてもゲームは動いてほしいので、エラーを表示するだけにして止めません。
            print(e)
            return

        self.bgm = SoundLoader.load(bgm_path)
        if self.bgm:
            self.bgm.loop = True  # ループ再生
            self.bgm.play()
        else:
            print("BGM を読み込めませんでした。ファイル形式やパスを確認してください。")

    def on_stop(self):
        """アプリ終了時に BGM を止めます。"""
        if self.bgm:
            self.bgm.stop()


if __name__ == "__main__":
    Step05BgmApp().run()
