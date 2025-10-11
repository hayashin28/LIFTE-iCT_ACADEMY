from kivy.config import Config
Config.set('graphics', 'width', '960')
Config.set('graphics', 'height', '640')

from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivymd.app import MDApp
import json, pathlib

from screens.title_screen import TitleScreen
from screens.field_screen import FieldScreen
from screens.battle_screen import BattleScreen
from src.core.rpg_director import RPGDirector

class GameApp(MDApp):
    def build(self):
        base = pathlib.Path(__file__).resolve().parents[1]
        settings_path = base / 'settings.json'
        settings = json.loads(settings_path.read_text(encoding='utf-8')) if settings_path.exists() else {}
        classroom = settings.get("classroom", "Master-D")
        self.title = f"RPG — {classroom} | Steel"
        self.director = RPGDirector(classroom_name=classroom, settings=settings)
        self.director.load_world()
        sm = ScreenManager(transition=NoTransition())
        sm.add_widget(TitleScreen(name="title", director=self.director))
        sm.add_widget(FieldScreen(name="field", director=self.director))
        sm.add_widget(BattleScreen(name="battle", director=self.director))
        return sm

if __name__ == "__main__":
    GameApp().run()