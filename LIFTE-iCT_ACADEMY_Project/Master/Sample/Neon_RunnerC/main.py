# -*- coding: utf-8 -*-
"""
main.py（自己ブート対応・厚めコメント）
--------------------------------------------------------------------
■ なぜ / 目的
    - VSCode の右上 ▶ などで「ファイル直実行」しても、
    パッケージ文脈に自動切替（自己ブート）して安定起動させるため。

■ 前提 / 依存
    - 本プロジェクトのルート（LIFTE-iCT_ACADEMY_Project）直下に Master/ が存在する構成。
    - Kivy が導入済みであること。

■ 入出力
    - 入力: なし
    - 出力: 画面（Window）として PlayScreen を表示。

■ 副作用
    - sys.path にプロジェクトルートを一時的に追加。

■ 例外
    プロジェクトルートを探索できない場合、StopIteration 例外。
    → その場合は `python -m Master.Sample.Neon_RunnerC` での起動を試してください。
"""
# ▼ 自己ブート：直実行でも「モジュール起動」へ切替
if __name__ == "__main__" and (__package__ in (None, "")):
    import runpy, pathlib, sys
    p = pathlib.Path(__file__).resolve()
    # 「Master/」を含むディレクトリを上位に向かって探索
    project_root = next(up for up in p.parents if (up / "Master").is_dir())
    # Python のモジュール検索パスの先頭にプロジェクトルートを追加
    sys.path.insert(0, str(project_root))
    # 以降は「正規のモジュール実行」として再実行
    runpy.run_module("Master.Sample.Neon_RunnerC.main", run_name="__main__", alter_sys=True)
    raise SystemExit

# ▼ ここから通常の（パッケージ文脈での）実装
from .core.engine import GameApp

def main() -> None:
    """
    アプリケーションのエントリポイント。
    - ScreenManager を内包する GameApp を起動します。
    """
    GameApp().run()

# F5/▶ 対応（保険）
if __name__ == "__main__":
    main()
