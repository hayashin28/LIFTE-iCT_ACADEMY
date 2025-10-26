# -*- coding: utf-8 -*-
from kivy.properties import StringProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel

ARROWS = {"N":"↑","E":"→","S":"↓","W":"←"}

class Compass(MDBoxLayout):
    direction = StringProperty("N")

    def __init__(self, **kwargs):
        super().__init__(orientation="horizontal", spacing="4dp", **kwargs)
        self.label = MDLabel(text=self._text(), halign="left")
        self.add_widget(self.label)
        self.bind(direction=lambda *_: self._update())

    def _text(self):
        return f"Dir: {self.direction} {ARROWS.get(self.direction, '?')}"

    def _update(self):
        self.label.text = self._text()
