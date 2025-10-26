# -*- coding: utf-8 -*-
# 画像なしの帯状パララックス。矩形を左右にラップさせるだけの軽量実装。
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp

class ParallaxLayer(Widget):
    """
    なぜ: 動く背景で奥行き感を出し、速度段階UPの体感を増幅する。
    前提: 幅=画面幅, 高さ=band_h。矩形を2枚用意し、左へ流しつつラップ。
    入力: speed_px_s（実速度）, color=(r,g,b,a)
    副作用: 自身のcanvas内Rectangleのposを更新
    """
    def __init__(self, band_h_px, color, **kw):
        super().__init__(**kw)
        self.band_h = dp(band_h_px)
        self.color_rgba = color
        with self.canvas:
            self._c = Color(*color)
            self._r1 = Rectangle(size=(self.width, self.band_h), pos=self.pos)
            self._r2 = Rectangle(size=(self.width, self.band_h), pos=(self.x + self.width, self.y))
        self.bind(pos=self._sync, size=self._sync)

    def _sync(self, *a):
        self._r1.size = (self.width, self.band_h)
        self._r2.size = (self.width, self.band_h)
        self._r1.pos = (self.x, self.y)
        self._r2.pos = (self.x + self.width, self.y)

    def tick(self, dt, speed_px_s):
        # 左へ流す。左に出た矩形を右へ巻き戻す。
        for r in (self._r1, self._r2):
            x, y = r.pos
            x -= speed_px_s * dt
            # 1枚分左に抜けたら右へワープ
            if x <= -self.width:
                x += self.width * 2
            r.pos = (x, y)
