# -*- coding: utf-8 -*-
"""
Day1 タスク割当（RPG Rustic / Master-B）— 7名×3h

使い方:
  $ python day1_tasks_rustic.py            # 概要を表示
  $ python day1_tasks_rustic.py --json     # 構造化JSONを出力（課題配布やスプレッドシート連携に）

前提:
  - 教室: Master-B
  - テーマ: master_B_rpg_rustic（Rustic（縦メニュー／数値表示））
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
CLASSROOM = "Master-B"
THEME = "master_B_rpg_rustic"
FLAVOR = "Rustic（縦メニュー／数値表示）"

TASKS = [
  {
    "id": "R0",
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
    "id": "R1",
    "role": "Lead",
    "title": "教室/テーマの固定",
    "goal": "Master-B & Rusticで起動表示を固定",
    "changes": "settings.json の classroom/theme を確定",
    "touch_files": [
      "settings.json"
    ],
    "commands": [
      "set classroom=\"Master-B\"",
      "set theme=\"master_B_rpg_rustic\"",
      "python src/main.py"
    ],
    "dod": [
      "タイトルに Master-B が表示",
      "Theme: RPG Rustic が表示"
    ]
  },
  {
    "id": "R2",
    "role": "UI",
    "title": "縦メニュー色とカーソル調整",
    "goal": "Rusticらしい暖色を適用",
    "changes": "theme.jsonのpalette.accentを #f6cf79 → #eabc5e へ",
    "touch_files": [
      "themes/master_B_rpg_rustic/theme.json"
    ],
    "commands": [
      "python src/main.py"
    ],
    "dod": [
      "メニューの強調色が変更されている",
      "スクショをREADMEに貼付"
    ]
  },
  {
    "id": "R3",
    "role": "Field",
    "title": "街入口でメッセージ表示",
    "goal": "イベント起動の雛形を作る",
    "changes": "events.json に messageトリガーを1件追加 (town.csvの入口)",
    "touch_files": [
      "data/events.json"
    ],
    "commands": [
      "python src/main.py  # 街入口に移動しメッセージ確認"
    ],
    "dod": [
      "街入口で1度メッセージが出る"
    ]
  },
  {
    "id": "R4",
    "role": "Battle",
    "title": "行動ログの整形（数値HP表示）",
    "goal": "縦メニューの選択→整形ログを出す",
    "changes": "battle_screenのログ出力フォーマットを '名前: コマンド' に統一",
    "touch_files": [
      "src/screens/battle_screen.py"
    ],
    "commands": [
      "python src/main.py  # バトル→選択→ログ表示確認"
    ],
    "dod": [
      "下部ログに '◯◯: たたかう' 形式で出る"
    ]
  },
  {
    "id": "R5",
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
    "id": "R6",
    "role": "Docs",
    "title": "README整備（Rustic版）",
    "goal": "配布先でも迷わない文書化",
    "changes": "起動手順・担当一覧・変更点（各1行）を追記",
    "touch_files": [
      "README.md"
    ],
    "commands": [
      "git add README.md",
      "git commit -m \"docs(rustic): day1 readme\""
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
