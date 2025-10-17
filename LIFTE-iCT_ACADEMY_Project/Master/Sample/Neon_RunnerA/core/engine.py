# -*- coding: utf-8 -*-
# シーン切替と60FPS更新を行う極小エンジン。

from kivy.clock import Clock
from kivy.core.window import Window

class Engine:
    # root（レイアウト）に現在のシーン（Title/Play）を載せ替える。
    # set_scene(scene): on_exit→入替→on_enter。キー入力もバインドし直す。
    def __init__(self, root_widget):
        self.root = root_widget
        self.scene = None
        self._clock_ev = None

    def set_scene(self, scene):
        # 古いシーンの後始末
        if self.scene is not None:
            try:
                self.scene.on_exit()
            except Exception:
                pass
            self.root.clear_widgets()

        # 新しいシーンを載せる
        self.scene = scene
        self.scene.on_enter(self.root, self)

        # キー入力の委譲設定（最新シーンへ）
        Window.unbind(on_key_down=self._on_key_down)
        Window.bind(on_key_down=self._on_key_down)

        # 更新ループ開始（多重起動を避ける）
        if self._clock_ev is None:
            self._clock_ev = Clock.schedule_interval(self._update, 1/60)

    def _on_key_down(self, _w, key, *_a):
        if self.scene:
            return self.scene.on_key_down(key)
        return False

    def on_touch_down(self, touch):
        if self.scene:
            return self.scene.on_touch_down(touch)
        return False

    def _update(self, dt):
        if self.scene:
            self.scene.update(dt)
