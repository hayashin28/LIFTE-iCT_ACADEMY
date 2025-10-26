# Neon Runner A - Day1 学習指導案（詳細）
日付: 2025-10-17

## ねらい（3h）
- ループの順序を説明しながら、自力で改造できる足場を作る。

## 到達基準（AC）
1) 地面上のみジャンプ（多段なし）
2) 右→左スクロール＆画面外で再配置
3) コイン=回復+加点、障害=減点
4) 10秒ごと速度段階UP
5) 体力0でGameOver→Enter/Space/Touchで再開

## タイムライン
- 00:00–00:10 完成デモとAC共有
- 00:10–00:35 仕組み概観（Engine / Title）
- 00:35–01:20 Play読解（速度→物理→スクロール→衝突→HUDの順）
- 01:20–02:00 パラメータ実験（GRAVITY/JUMP_V/SPEED_STEP）
- 02:00–02:30 小課題（障害2種・コインの落下など）
- 02:30–03:00 PR作成（ACチェック）

## 板書
- vy -= g*dt → y += vy*dt → clamp
- AABB: (ax < bx+bw) and (ax+aw > bx) and (ay < by+bh) and (ay+ah > by)
- Pool: 使い回す/生成しない
- config集中: チューニング容易

## 想定Q&A
- Q: 跳びすぎ/落ちすぎ
  - A: JUMP_V/GRAVITY を対比して説明。dtを頭でイメージ。
- Q: 当たりのズレ
  - A: pos/size と Rectangle 同期のbindを再確認。
- Q: 遅い/速い
  - A: BASE/SPEED_STEP/SPEED_INTERVALで体感を整える。

## 提出（PR）テンプレ
- タイトル: feat(day1): jump/scroll/aabb/hud with speed tiers
- 内容: 起動方法/AC/変更点/スクショ
- チェック: AC5項目 + config集中
