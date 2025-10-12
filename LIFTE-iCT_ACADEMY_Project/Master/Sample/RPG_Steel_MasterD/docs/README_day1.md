# Day1 起動手順（Steel_MasterD）

## 前提
- Python 3.10+
- Kivy 2.2+（`pip install -r requirements_day1.txt`）

## セットアップ（Windows想定）
```bat
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements_day1.txt
python src\main.py
```

## 操作
- タイトル画面で **Enter** キー → フィールド画面へ
- 矢印キー / WASD で移動
- **H**：HUD 表示トグル
- **Esc**：終了（タイトル画面で）

## 目標（Day1）
- タイトル→フィールドまで起動
- プレイヤー移動（上下左右）
- 壁タイルで停止（衝突）
- HUD に x,y,dir,fps,tile_x,tile_y 表示
- 15秒動画＋スクショ撮影 → PR で提出
