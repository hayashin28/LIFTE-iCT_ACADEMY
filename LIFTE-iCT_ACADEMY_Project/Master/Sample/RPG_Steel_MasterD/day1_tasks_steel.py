# -*- coding: utf-8 -*-
"""
Day1 タスク割当（RPG Steel / Master-D）— 7名×3h

使い方:
  $ python day1_tasks_steel.py            # 概要を表示
  $ python day1_tasks_steel.py --json     # 構造化JSONを出力（課題配布やスプレッドシート連携に）

前提:
  - 教室: Master-D
  - テーマ: master_D_rpg_steel（Steel（横メニュー／バー表示））
  - 実行環境: Python 3.10+ / kivy / kivymd
  - 配布リポ: このRPGスターター（起動確認済）
定義:
  - TEAM_SIZE = 7
  - 1人1タスク + PM横断（7枠）
DoD (Definition of Done):
  - 全員がローカルで起動スクショを取得
  - READMEに「起動手順/担当/変更点」を1行追記
  - 各自1コミット (PR模擬可)
"""
import sys, json

TEAM_SIZE = 7
CLASSROOM = "Master-D"
THEME = "master_D_rpg_steel"
FLAVOR = "Steel（横メニュー／バー表示）"

TASKS = [
  {
    "id": "S0",
    "role": "PM(横断)",
    "title": "リポ準備と定型追加",
    "goal": "誰でも迷わず起動→コミットできる土台を用意",
    "changes": "CONTRIBUTING最小雛形・Issue/PRテンプレ追加",
    "touch_files": [
      "CONTRIBUTING.md",
      ".github/ISSUE_TEMPLATE.md",
      ".github/PULL_REQUEST_TEMPLATE.md",
      "README.md"
    ],
    "commands": [
      "git init",
      "git add .",
      "git commit -m \"chore: init day1 skeleton\""
    ],
    "dod": [
      "READMEに起動手順がある",
      "テンプレが反映される"
    ]
  },
  {
    "id": "S1",
    "role": "Lead",
    "title": "教室/テーマの固定",
    "goal": "Master-D & Steelで起動表示を固定",
    "changes": "settings.json の classroom/theme を確定",
    "touch_files": [
      "settings.json"
    ],
    "commands": [
      "set classroom=\"Master-D\"",
      "set theme=\"master_D_rpg_steel\"",
      "python src/main.py"
    ],
    "dod": [
      "タイトルに Master-D が表示",
      "Theme: RPG Steel が表示"
    ]
  },
  {
    "id": "S2",
    "role": "UI",
    "title": "HP/MPバー太さ +2px",
    "goal": "Steelの視認性を上げる",
    "changes": "battle_screenのバー高さ（12→14）に変更",
    "touch_files": [
      "src/screens/battle_screen.py"
    ],
    "commands": [
      "python src/main.py  # バー太さが増えたか確認"
    ],
    "dod": [
      "HP/MPバーが明確に太くなっている",
      "スクショをREADMEに貼付"
    ]
  },
  {
    "id": "S3",
    "role": "Field",
    "title": "洞窟に通路を1本追加",
    "goal": "マップ編集の動線理解",
    "changes": "cave.csv の壁を1列削除して通路化",
    "touch_files": [
      "data/maps/cave.csv"
    ],
    "commands": [
      "python src/main.py  # 通路を通過できることを確認"
    ],
    "dod": [
      "プレイヤが新通路を通れる"
    ]
  },
  {
    "id": "S4",
    "role": "Battle",
    "title": "ターゲット選択の点滅速度を上げる",
    "goal": "選択中ターゲットの視認性を上げる",
    "changes": "blink intervalを0.5→0.33sに変更",
    "touch_files": [
      "src/screens/battle_screen.py"
    ],
    "commands": [
      "python src/main.py  # Tでターゲット→点滅速度確認"
    ],
    "dod": [
      "ターゲット時の枠点滅が速くなる"
    ]
  },
  {
    "id": "S5",
    "role": "QA",
    "title": "起動確認とDoDチェック",
    "goal": "動作の抜け漏れを防止",
    "changes": "なし（チェックリスト運用）",
    "touch_files": [
      "README.md"
    ],
    "commands": [
      "python src/main.py  # フィールド/バトル/メッセージ確認"
    ],
    "dod": [
      "DoD全条件に✓を入れた証跡をREADMEへ1行追記"
    ]
  },
  {
    "id": "S6",
    "role": "Docs",
    "title": "README整備（Steel版）",
    "goal": "配布先でも迷わない文書化",
    "changes": "起動手順・担当一覧・変更点（各1行）を追記",
    "touch_files": [
      "README.md"
    ],
    "commands": [
      "git add README.md",
      "git commit -m \"docs(steel): day1 readme\""
    ],
    "dod": [
      "READMEに手順と担当/変更点が反映"
    ]
  }
]

def print_table():
    print(f"=== Day1 タスク一覧 — {CLASSROOM} / {FLAVOR} ===")
    for t in TASKS:
        print(f"[{t['id']}] {t['role']}: {t['title']}")
        print(f"  目的 : {t['goal']}")
        print(f"  変更 : {t['changes']}")
        if t.get('touch_files'):
            print("  対象 : " + ", ".join(t['touch_files']))
        if t.get('commands'):
            print("  実行 :")
            for c in t['commands']:
                print(f"    $ {c}")
        print("  DoD :")
        for d in t['dod']:
            print(f"    - {d}")
        print()

if __name__ == "__main__":
    if "--json" in sys.argv:
        print(json.dumps(dict(classroom=CLASSROOM, theme=THEME, flavor=FLAVOR, team_size=TEAM_SIZE, tasks=TASKS), ensure_ascii=False, indent=2))
    else:
        print_table()
