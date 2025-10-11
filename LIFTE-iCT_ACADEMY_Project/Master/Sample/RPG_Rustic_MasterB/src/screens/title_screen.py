from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel

class TitleScreen(Screen):
    def __init__(self, director, **kwargs):
        super().__init__(**kwargs); self.director = director
    def on_pre_enter(self, *args): self.build_ui()
    def build_ui(self):
        self.clear_widgets()
        layout = MDBoxLayout(orientation="vertical", padding=24, spacing=24)
        title = MDLabel(text=f"RPG — {self.director.classroom_name} / Theme: {self.director.theme.get('name','')}", halign="center", font_style="H5")
        btn_field = MDRaisedButton(text="フィールドへ", pos_hint={"center_x": .5}); btn_field.bind(on_release=lambda *_: setattr(self.manager,'current','field'))
        btn_battle = MDRaisedButton(text="バトルへ（直行）", pos_hint={"center_x": .5}); btn_battle.bind(on_release=lambda *_: setattr(self.manager,'current','battle'))
        layout.add_widget(title); layout.add_widget(btn_field); layout.add_widget(btn_battle); self.add_widget(layout)