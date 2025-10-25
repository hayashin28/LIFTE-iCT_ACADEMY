# README — Day2 模範解答キー（RPG_Rustic_MasterB）
（2日目の到達版：授業内DoD）

## できること
- CSVタイル描画／プレイヤ移動（慣性・加速・摩擦）／走る（Shift）／壁衝突（軸分離）
- HUD（HP/スタミナ）／カメラ追従
- 主要パラメタは `config.py` に集約

## 実行
```bash
pip install pygame
python game.py
```

## DoD（合格基準）
- 壁停止・走行・スタミナ減回復・HUD表示の4点が動作
- 変更内容を簡単に記録（担当/スクショ）
- PRを1本マージし `day2_milestone` を付与
