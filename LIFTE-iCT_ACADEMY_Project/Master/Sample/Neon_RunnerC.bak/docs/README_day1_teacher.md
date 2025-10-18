# NeonRunner – Day1 教師パック（コメント厚め完品）
作成日: 2025-10-12

## 目的（Day1）
- タイトル→プレイ画面までの起動動線。
- 左右レーン移動 / ジャンプ（Space）。
- 一定周期（＋ランダム）で障害物を生成しスクロール。
- AABB 衝突で HP 減少（無敵時間あり）。
- HUD：score/hp/speed/paused 表示。`P` でポーズ切替。
- 提出：15秒動画 + スクショ + PR（テンプレあり）。

## 実行
```bat
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements_day1.txt
python -m src.main
```

## 操作
- ←/→: レーン移動（3レーン）
- Space: ジャンプ（地上時）
- P: ポーズ/再開
- H: HUD 表示切替

## 収録
- `src/` … Kivy の最小構成（厚いコメント付き）
- `TEACHER_GUIDE_Day1_NeonRunner.md` … 学習指導案（厚め詳細）
- `PR_TEMPLATE_Day1_NeonRunner.md` … 提出本文テンプレ
