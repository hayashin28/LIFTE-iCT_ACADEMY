# -*- coding: utf-8 -*-
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivymd.app import MDApp

from ui.theme import apply_theme
from screens.title import TitleScreen
from screens.town import TownScreen
from screens.dungeon import DungeonScreen

class RootManager(ScreenManager):
    pass

class App(MDApp):
    def build(self):
        apply_theme(self)
        sm = RootManager(transition=NoTransition())
        sm.add_widget(TitleScreen(name="title"))
        sm.add_widget(TownScreen(name="town"))
        sm.add_widget(DungeonScreen(name="dungeon"))
        return sm

if __name__ == "__main__":
    App().run()
