# run_neonrunnerc.py  （エディタでこのファイルを開いて右上▶）
import runpy, pathlib, sys

root = pathlib.Path(__file__).resolve().parent  # .../LIFTE-iCT_ACADEMY_Project
# ルートをPYTHONPATHへ（右上▶やCode Runnerでも相対importが通る）
sys.path.insert(0, str(root))

# 実体は "python -m Master.Sample.Neon_RunnerC.main" と同じ
runpy.run_module("Master.Sample.Neon_RunnerC.main", run_name="__main__", alter_sys=True)
