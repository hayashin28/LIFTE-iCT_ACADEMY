# -*- coding: utf-8 -*-
"""
main.py – エントリポイント
なぜ: 起動の窓口を 1 箇所に集約し、他のモジュールから独立させるため。
"""
from src.core.engine import GameApp

if __name__ == "__main__":
    GameApp().run()
