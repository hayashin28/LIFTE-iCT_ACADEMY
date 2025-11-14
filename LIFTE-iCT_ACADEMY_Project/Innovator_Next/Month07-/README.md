# retro-mario / 授業用 README

## 権利・素材について（重要）

本リポジトリは授業で「実装手順」を学ぶためのテンプレートです。  
**任天堂株式会社等の第三者に帰属する著作物・商標（キャラクター名／画像／音源／ロゴ／固有名称など）の使用は想定していません。**

- `retro_mario/assets` 配下に置く画像・音源は **受講者自身が用意した自作素材** または **適法なライセンス（例: CC0/CC-BY）** のものに差し替えてください。
- 具体名の使用を避けるため、以下の**汎用名**を推奨します：
  - `hero_idle.png`（主人公） / `enemy.png`（敵） / `pipe.png`（パイプ） / `brick_block.png`（レンガ） / `bg.png`（背景） / `bgm.ogg`（BGM）
- 第三者著作物を含む素材は **リポジトリにコミットしない** でください（授業内ローカルのみでの使用に限る）。
- 配布・公開を行う場合は、**第三者素材をすべて除去**し、必要に応じて `ASSETS_LICENSE.md` にライセンスと出典を記載してください。

> 本記載は一般的なガイドであり、法的助言ではありません。必要に応じて権利者表示・利用条件をご確認ください。

> **目的**: 「マリオ風」の**最小構成**で、Kivy/KivyMD による**画面構成→入力→当たり判定→非同期（独立更新）**を、**1ステップ=1手**で積み上げる。  
> **方針**: 設計はしない／「どう書けばこの動きになるか」に特化／毎ステップは**最小差分**で進める。  
> **対象時間**: 3h（授業）＋復習。

---

## 0. フォルダ構成（固定）

> 既存コードが参照する標準パス。**名称と階層は変えないこと**。

```
retro-mario/                     # プロジェクト ルート（任意の場所に置いて良い）
├─ step01_bg.py                  # 背景だけを出す（最小）
├─ step02_cloud.py               # 雲を置く
├─ step03_dokan.py               # 土管を置く
├─ step04_brick.py               # レンガを置く
├─ step05_bgm.py                 # BGM を足す
├─ step06_place_mario.py         # 主人公（静止）を置く
├─ step07_move_lr.py             # ←→移動＋左右反転
├─ step08_collide_x.py           # 横の当たり判定（地形にぶつかる）
├─ step09_jump_basic.py          # 重力＋ジャンプ＋縦の当たり判定
├─ step10_goomba_spawn.py        # クリボー出現→往復パトロール（独立更新）
└─ retro_mario/                  # ※コードが参照する**固定サブフォルダ**
   └─ assets/
      ├─ img/
      │  ├─ bg.png or bg.jpg
      │  ├─ cloud.png            (推奨: 512x128)
      │  ├─ dokan.png            (推奨: 64x96)
      │  ├─ brick_block.png      (推奨: 128x32)
      │  ├─ hero_idle.png or mario.png (推奨: 64x64)
      │  └─ goomba.png           (推奨: 48x48 / 透過PNG)
      └─ bgm/
         ├─ bgm.ogg | bgm.mp3 | bgm.wav
         └─ main.ogg | main.mp3 | main.wav
```

**注意**: 既存コードは `ROOT_DIR / "retro_mario" / "assets" / "img"` を前提にしています。  
プロジェクト名は任意（例: `retro-mario`）ですが、**中の `retro_mario/assets/...` は必須**です。

---

## 1. セットアップ（Windows想定）

```powershell
# 任意の場所にプロジェクトを配置
cd D:\workspace
python -m venv .venv
.\.venv\Scriptsctivate

# Kivy + KivyMD を導入（ネットワーク環境により時間がかかる場合あり）
pip install --upgrade pip wheel setuptools
pip install kivy kivymd
```

- **Python**: 3.10–3.12 を推奨。
- **フォーカス**: 実行後はウィンドウを**一度クリック**してからキー操作（←→、Space/↑）。
- **音が出ない**: OSの出力デバイス・音量を確認。MP3 が再生できない場合は OGG/WAV を試す。

---

## 2. 進め方（1手ずつ / 検収基準つき）

各ステップは**最小差分**で、**できたか/できていないか**が判定しやすい粒度にしています。  
ファイルは同名で用意済みの想定（なければ作成）。

### Step 01 — 背景だけを出す（`step01_bg.py`）
- **学習目標**: `MDApp + Builder.load_string(KV)` の最小パターンを知る。
- **やること**: `Image` を全画面（`size_hint: 1,1`）で貼る。`bg.png|jpg` を使う。
- **検収**: 背景がウィンドウ全面に表示される。
- **つまずき**: 画像が見えない → 相対パス/拡張子が誤り。

### Step 02 — 雲を置く（`step02_cloud.py`）
- **学習目標**: `size_hint: None,None` と `size/pos` の明示指定。
- **やること**: `cloud.png` を `(512,128)` で `(192,512)` に固定配置。
- **検収**: 雲が画面上部に見える。

### Step 03 — 土管を置く（`step03_dokan.py`）
- **学習目標**: 複数 `Image` を重ねて“シーン”を構成する。
- **やること**: `dokan.png` を `(64,96)` / `pos: (640,92)` に。
- **検収**: 土管が地面上に“刺さらず”置けている。

### Step 04 — レンガを置く（`step04_brick.py`）
- **学習目標**: 画面レイアウトの微調整（±16px刻み）。
- **やること**: `brick_block.png` を `(128,32)` / `pos: (448,208)` に。
- **検収**: レンガが土管の左上空間に浮く。

### Step 05 — BGM を足す（`step05_bgm.py`）
- **学習目標**: `SoundLoader` によるループ再生・終了時停止。
- **やること**: `bgm.(ogg|mp3|wav)` を if 存在で `loop=True` 再生。
- **検収**: アプリ起動でBGM。終了時に停止。

### Step 06 — 主人公（静止）を置く（`step06_place_mario.py`）
- **学習目標**: 主人公を“最後に”描く（前面）・サイズ合わせ（64x64）。
- **やること**: `hero_idle.png|mario.png` を `pos: (128,GROUND_Y)`。
- **検収**: 主人公が床の上端（`GROUND_Y=100`）に立っている。

### Step 07 — ←→移動＋左右反転（`step07_move_lr.py`）
- **学習目標**: `Window.bind(on_key_down=...)` と `FlipImage（左右反転）`。
- **要点（KV）**: `Translate` は **x/y 行に分ける**（例外回避）
  ```kv
  <FlipImage@Image>:
      canvas.before:
          PushMatrix
          Translate:
              x: self.center_x
              y: self.center_y
          Scale:
              x: -1 if app.face_left else 1
              y: 1
              z: 1
          Translate:
              x: -self.center_x
              y: -self.center_y
      canvas.after:
          PopMatrix
  ```
- **検収**: ←→で16pxずつ移動／向きが反転。

### Step 08 — 横の当たり判定（`step08_collide_x.py`）
- **学習目標**: AABB衝突（矩形重なり）と“めり込み防止”。
- **やること**: `dokan/brick` を障害物にして、ぶつかったら手前で止める。
- **検収**: 土管・レンガに水平移動で入れなくなる。

### Step 09 — ジャンプ（重力＋縦の当たり判定）（`step09_jump_basic.py`）
- **学習目標**: `vy`（縦速度）＋`GRAVITY`＋`_resolve_vertical`。
- **やること**: Space/↑ で `vy=JUMP_SPEED`、毎フレーム `vy+=GRAVITY*dt`。
- **接地条件**: 床の上端 `GROUND_Y`、または障害物の**上面**に到達したら `vy=0`。
- **検収**: ジャンプ→着地で安定。上昇中に下面へ当たると頭打ち。

### Step 10 — クリボー出現→往復パトロール（`step10_goomba_spawn.py`）
- **学習目標**: **非同期=独立更新**（asyncio は使わず、**Clock を2本**）。
- **ループの分離**:
  - `Clock.schedule_interval(update_hero, 1/60)` … 主人公の物理・入力
  - `Clock.schedule_interval(update_goomba, 1/60)` … クリボーの物理・AI
- **状態の分離**（混線防止）: `goomba_vx/vy/on_ground/phase` は**敵専用**。
- **フェーズ**: `EMERGE`（土管から上へ）→`WALK`（落下着地→左右パトロール）。
- **往復**: 画面端 or 前進不能で `goomba_vx *= -1`。
- **検収**: 起動直後に土管から“にゅっ”→着地→左右に往復。

---

## 3. 非同期（独立更新）メモ（授業での説明用）

- **UIは1本のイベントループ**で動いている。時間のかかる処理（`while/sleep`）は**固まる原因**。
- **やること**: やりたい処理を**小さく刻んで** `Clock.schedule_interval(func, 1/60)` に登録。  
  これで毎フレーム**少しずつ**動かせる。主人公と敵を**別登録**すれば、互いに**待たない**。
- **asyncioを使わない理由**: 本授業では概念負荷を上げないため。Kivyのスケジューラで十分。

---

## 4. 型アノテーション（最小限の使い方）

- `def f(x: float) -> int:` のように**目印**を書く。挙動や速度は**変わらない**。
- エディタ補完や静的解析（mypy など）で**誤りが早期に見つかる**。
- 本教材では、戻り値が複数ある関数で `-> tuple[float, float, bool]` を使用。

---

## 5. トラブルシュート（頻出）

- **KV パーサ例外**: `Invalid data after declaration`  
  → `Translate: self.center_x, self.center_y` のような**カンマ区切りは不可**。  
  **正**:  
  ```kv
  Translate:
      x: self.center_x
      y: self.center_y
  ```

- **資材が見つからない**: 実行ログ `print("[BG] using: ...")` を確認。  
  `retro_mario/assets/img/...` の**階層とファイル名**を見直す。

- **キー入力が効かない**: 実行ウィンドウを**一度クリック**（フォーカス獲得）。

- **BGMが鳴らない**: コーデック/拡張子差異。`ogg` or `wav` を試す。

- **当たり判定が不安定**: 画像サイズと `size` の不一致。推奨サイズへ合わせるか、`size` を明示。

---

## 6. 授業運営メモ（講師向け）

- **一手主義**: 各ステップは**差分 1 つ**。生徒に「何が追加/変更されたか」を言語化させる。
- **検収フレーズ**: 「いまは *できた/できていない* の二値だけを見る」。  
  できたら次の一手へ、できていなければ**資材パス**と**KVの構文**を優先確認。
- **調整ノブ**: `STEP`（歩幅）, `GRAVITY`/`JUMP_SPEED`（体感）, 座標は**±16px**で合わせる。

---

## 7. つぎの課題（発展）

- **踏みつけで敵を倒す**（上からの衝突時のみ有効）
- **ジャンプ中だけ画像差し替え**（`mario_junp.png`）
- **長押しで歩き続ける**（連続移動）
- **ステージカメラのスクロール**（主人公追従）
- **タイルマップ化**（`stage_grid.png` を行列読込して自動配置）
- **複数敵とスポーン管理**（一定間隔で出現）

---

## 8. 素材と権利

- 本教材は**学習目的**です。実在のキャラクター/ロゴ等に類似する素材は**学外配布しない**こと。
- 音源・画像のライセンスは**各素材の規約**に従ってください。

---

## 9. 実行のしかた（共通）

```powershell
# 例: Step 10 を実行
.\.venv\Scriptsctivate
python step10_goomba_spawn.py
```

**検収基準**は各ステップの節を参照。最小の一手で前進し、手元の動きを**必ず言語化**するのが上達の近道です。

※権利・素材の注意書きを入れて、配布物は自作/フリー素材（CC0/CC-BY等）に限定