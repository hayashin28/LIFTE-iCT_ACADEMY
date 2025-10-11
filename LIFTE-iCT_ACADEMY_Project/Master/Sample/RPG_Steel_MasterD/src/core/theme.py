from __future__ import annotations
from pathlib import Path
import json

def load_theme(base_dir: Path, theme_name: str) -> dict:
    p = base_dir / 'themes' / theme_name / 'theme.json'
    if not p.exists():
        return {
            "name": "Default",
            "palette": {"bg":"#101010","ui":"#1b1b1b","panel":"#222","accent":"#ffd166","hp":"#ef476f","mp":"#118ab2","text":"#eee"},
            "battle": {"menu_layout":"vertical-right","status_style":"text","message_top_panel": False}
        }
    try:
        return json.loads(p.read_text(encoding='utf-8'))
    except Exception:
        return {"name":"BrokenTheme","palette":{},"battle":{}}