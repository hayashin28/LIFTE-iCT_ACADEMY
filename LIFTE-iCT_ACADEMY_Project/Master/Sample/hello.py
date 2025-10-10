from kivy.app import App
from kivy.uix.label import Label
from kivy.core.text import LabelBase

# フォント登録（ここでは「源ノ角ゴシック」）
LabelBase.register(name="GenShinGothic", fn_regular="GenShinGothic-Regular.ttf")

class MyApp(App):
    def build(self):
        return Label(text="こんにちは、Kivy！", font_name="GenShinGothic")

if __name__ == "__main__":
    MyApp().run()
