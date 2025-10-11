# 学習指導案 — Innovator_next「Kivy/KivyMD 反応ゲーム Day1」

## 1. 単元・本時
- **単元名**：Kivy/KivyMDで作る「ボタン反応ゲーム」
- **本時（Day1）のねらい**：  
  3×3のボタンとStartボタンを作り、**Startでタイマーが1秒ごとに減る**こと、**ボタン押下イベントが動く**ことを確認する。  
  帰宅前に「宿題フック（`_spawn`／`_set_active`／`_set_normal`）」の**ひな型とヒントをコードに挿入**しておく。

## 2. 目標（知識・技能／思考・判断・表現／主体的に学習に取り組む態度）
- **知識・技能**
  - Kivy/KivyMDの**KV言語**でUIツリーを宣言できる。
  - `Clock.schedule_interval()` で**毎秒処理**を実装できる。
  - `ids` 参照でラベルを更新できる。
  - ボタンに `index` を付与し、**イベントハンドラ**で値を扱える。
- **思考・判断・表現**
  - 画面構造（KV）とロジック（Python）の**役割分担**を説明できる。
  - 「内部は0始まり／表示は1始まり」を**混乱なく扱い分け**られる。
- **態度**
  - 実行→観察→修正の**反復**をいとわず、ログ出力で状況を**言語化**できる。

## 3. 評価規準（形成的評価）
- **A**：KVとPythonの役割を言語化し、Start→タイマー減少→`pressed #` 表示まで自力で通せる。  
- **B**：教員の支援下で上記を通し、宿題フックを所定位置に挿入できる。  
- **C**：テンプレを用い、最低限の動作と板書キーワードの再現ができる。

## 4. 準備・環境
- 受講者PC：Python 3.10〜3.12、`pip install kivy kivymd` 済み（ポータブル可）
- 配布ファイル：`Day1_with_hints_annotated.py`（初日完成＋厚めコメント版）
- 予備：動作しない生徒向けに**完成版**と**半完成版**（途中から差し替え可）
- 表示装置：プロジェクタ（板書はスライド併用可）

## 5. 授業の流れ（60分想定）

| 時間 | 指導・学習の流れ | 教師の働きかけ／ポイント |
|---:|---|---|
| 0–5 | 目的提示・デモ（StartでTimeが減る／ボタン押すと番号表示） | 「今日は**動く土台**を作る。宿題の入口まで打ち込んで帰る」 |
| 5–10 | 環境確認・テンプレ配布 | 起動テスト。インポートエラーは `pip install kivy kivymd` |
| 10–20 | KVの骨格入力（ラベル×2、Grid、Start） | 「**UI＝KV**、**動き＝Python**」の役割分担を言語化 |
| 20–30 | `build()`：9ボタン生成、`index`付与、`on_release`結線 | `btn.index = i` と `ids.grid.add_widget(btn)` を確認 |
| 30–40 | `start_game()` と `_tick()` 実装、Start動作確認 | `Clock.schedule_interval(self._tick, 1)`／多重起動は `cancel()` |
| 40–45 | `on_press()`でデバッグ表示 | **表示は1始まり**で揃える：`print(f"pressed {idx+1}")` |
| 45–55 | 宿題フック挿入（`_spawn`/`_set_active`/`_set_normal` の雛形とコメント） | コメントを読み合わせ。「今日は**ここまで**でOK」 |
| 55–60 | ふりかえり・自己チェック・保存 | 宿題の目的と提出物（.py＋任意スクショ）を短く再確認 |

## 6. 板書（黒板）計画
### 左（本時のめあて）
- ① 3×3ボタン＋Start  
- ② Startで**Timeが1秒ごとに減る**  
- ③ 押下で **pressed #** を表示（※ #は1〜9）

### 中（キーワード）
- `Clock.schedule_interval(func, 1)` … 毎秒  
- `ids.score_label.text = f"Score: {score}"` … 表示更新  
- `btn.index = i`／`def on_press(self, instance)` … イベント  
- **内部は0始まり／表示は1始まり**（`idx+1`）

### 右（宿題フック方針）
```text
_spawn:
  1) 先に前回の光りを消す（_set_normal）
  2) ランダムに1つ選ぶ（random.randrange(9)）
  3) 光らせる（_set_active）
_set_active/_set_normal:
  text・色・背景を切り替える
```

## 7. 今日配るコード（投影しながら読み上げ）
- `Day1_with_hints_annotated.py`（厚めコメント版）  
  **表示だけ1始まり**にする最小差分：
  ```python
  def on_press(self, instance):
      idx = getattr(instance, 'index', None)
      if idx is not None:
          print(f"pressed {idx+1}")  # 表示は1〜9に
  ```
- 色変更が効きにくい端末：グリッドのボタンを `MDFlatButton` → `MDRaisedButton` に変更。

## 8. つまずき予測と対処
- `NameError: MDFlatButton` → `from kivymd.uix.button import MDFlatButton`
- `AttributeError: 'BoxLayout' object has no attribute 'ids'` → KV読み込み前の参照ミス。`Builder.load_string(KV)`→`self.root.ids...` の順。
- 背景色が変わらない → `MDRaisedButton` を使用。
- Start多重押下で加速 → `if hasattr(self, 'tick'): self.tick.cancel()` を再確認。

## 9. 個別最適化・配慮（差分指導）
- 速い子：`random.choice([i for i in range(9) if i != active])` で**同じマス連続の回避**。  
- つまずいた子：完成テンプレから**該当ブロックのみ**を写経／貼り替え。  
- 集中維持：10分ごとに**実行チェック**→成功体験を入れる。

## 10. 宿題（次回まで）
- **目的**：ランダム点灯→正解でスコア＋1→時間0で終了。  
- **提出**：`Homework_version.py`（.py）＋任意スクショ1枚。  
- **チェック項目**：  
  - Startで `Time` が減る  
  - **1.5秒ごと**に1つだけ光る  
  - **押すとScore+1**  
  - 0で停止・消灯

## 11. 授業後ふりかえり（教員用メモ）
- 到達度（A/B/C）  
- つまずきの最多箇所／次回改善点  
- 時間配分（どこで伸縮が必要か）  
- 次回（Day2）の導入で再確認する事項
