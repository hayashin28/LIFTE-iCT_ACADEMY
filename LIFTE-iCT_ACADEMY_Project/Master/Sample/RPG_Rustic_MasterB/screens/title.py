# -*- coding: utf-8 -*-
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel

class TitleScreen(MDScreen):
    def on_pre_enter(self, *args):
        self.clear_widgets()
        layout = MDBoxLayout(orientation="vertical", spacing="16dp", padding="24dp")
        layout.add_widget(MDLabel(text="RPG Rustic - MasterB", halign="center", font_style="H4"))
        layout.add_widget(MDLabel(text="Title Screen", halign="center"))
        layout.add_widget(MDRectangleFlatButton(text="Start (Go Town)", pos_hint={"center_x": 0.5}, on_release=self.go_town))
        self.add_widget(layout)

    def go_town(self, *args):
        self.manager.current = "town"
