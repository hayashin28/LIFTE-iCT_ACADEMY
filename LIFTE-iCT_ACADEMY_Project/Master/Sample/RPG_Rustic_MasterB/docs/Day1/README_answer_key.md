# README — Day1 模範解答キー

このフォルダは **Day1(初日)のDoD達成** を目的にした「完成コード（授業内の完成）」です。  
> *注*: ここでの「完成」は **初日の合格基準** であり、商用品質の「完品」ではありません。

## できること
- Title → Town → Dungeon の画面遷移
- 画面左上の **方位コンパス** と **現在地テキスト**
- WASD/矢印キーで向き・座標を更新
- `maps/dungeon_01.json` を読み込んでテキストマップを表示（`#`=壁, `.`=床, `P`=プレイヤ）
- オプション: 壁に衝突しない設定（`BLOCK_WALLS=True`）

## 実行
```bash
python main.py
# 必要なら事前に: pip install -r requirements.txt
```

## 構成
- `main.py` — ScreenManagerとテーマを初期化
- `screens/` — Title/Town/Dungeonの各画面
- `ui/widgets/compass.py` — 方位インジケータ
- `maps/dungeon_01.json` — 10×10の壁つきマップ
- `docs/解説.md` — ステップ別の考え方とつまずき対策
- `docs/採点ルーブリック.md` — 評価の観点（配点の目安）
