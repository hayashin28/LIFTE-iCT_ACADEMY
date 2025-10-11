# RPG_Steel_MasterD_v1 — Day1 Starter

**教室**: Master-D　**テーマ**: Steel  
**目標 (Day1)**: 3マップ移動 + 戦闘画面（Rustic=縦/数値, Steel=横/バー）で**ログ/バーが見える状態**に。

## 起動
```
pip install "kivy[base]" kivymd
python src/main.py
```

## 主要フォルダ
- `src/core/`：RPGDirector・theme loader・map/collision
- `src/screens/`：Title/Field/Battle（UI表示）
- `themes/`：Rustic/Steel の `theme.json`
- `data/`：マップCSV・イベントJSON