from __future__ import annotations
from pathlib import Path
import json
from typing import Optional, Dict, Any, List

from .map_loader import load_csv_map
from .collision import can_move
from .theme import load_theme

class RPGDirector:
    def __init__(self, base_dir: Optional[Path] = None, classroom_name: str = "Master", settings: Optional[dict]=None):
        here = Path(__file__).resolve()
        self.base_dir = base_dir or here.parents[2]
        self.data_dir = self.base_dir / 'data'
        self.map_dir = self.data_dir / 'maps'
        self.events_path = self.data_dir / 'events.json'

        self.classroom_name = classroom_name
        self.settings = settings or {}
        theme_name = self.settings.get("theme", "master_B_rpg_rustic")
        self.theme = load_theme(self.base_dir, theme_name)

        # world
        self.current_map: str = 'plains.csv'
        self.player_pos: List[int] = [2, 2]
        self.grid: List[List[int]] = []
        self._events: Dict[str, Any] = {}

        # battle
        self.party: List[Dict[str, Any]] = [
            {"name":"ディア","hp":271,"hp_max":271,"mp":111,"mp_max":111},
            {"name":"エメル","hp":254,"hp_max":254,"mp":122,"mp_max":122},
            {"name":"カイゼン","hp":254,"hp_max":254,"mp":86,"mp_max":86},
            {"name":"セツアー","hp":277,"hp_max":277,"mp":104,"mp_max":104},
        ]
        self.enemies: List[Dict[str, Any]] = [
            {"name":"グラスワーム","hp":120,"hp_max":120},
            {"name":"グラスワーム","hp":120,"hp_max":120},
            {"name":"グラスワーム","hp":120,"hp_max":120},
        ]
        self.phase: str = 'select'      # 'select' | 'target' | 'resolve'
        self.active_index: int = 0
        self.menu_index: int = 0
        self.target_index: int = 0
        self.selected_actions: List[Dict[str, Any]] = []

    # world
    def load_world(self) -> None:
        self._events = self._load_events()
        self.load_map(self.current_map, spawn=tuple(self.player_pos))

    def _load_events(self) -> Dict[str, Any]:
        if not self.events_path.exists():
            return {"maps": {}}
        try:
            return json.loads(self.events_path.read_text(encoding='utf-8'))
        except Exception:
            return {"maps": {}}

    def load_map(self, name: str, spawn=(2,2)) -> None:
        path = self.map_dir / name
        self.grid = load_csv_map(str(path))
        self.current_map = name
        self.player_pos = [int(spawn[0]), int(spawn[1])]

    def _triggers_here(self, mapname: str, x: int, y: int):
        m = self._events.get('maps', {}).get(mapname, {})
        for ev in m.get('triggers', []):
            if ev.get('x') == x and ev.get('y') == y:
                yield ev

    def try_move(self, dx: int, dy: int) -> Dict[str, Any]:
        nx = self.player_pos[0] + dx
        ny = self.player_pos[1] + dy
        moved = False; event = None
        if can_move(self.grid, nx, ny):
            self.player_pos = [nx, ny]; moved = True
            for ev in self._triggers_here(self.current_map, nx, ny):
                et = ev.get('type')
                if et == 'warp':
                    to_map = ev.get('to_map'); spawn = ev.get('spawn', [2,2])
                    self.load_map(to_map, spawn=spawn); event = {"type":"warp","to_map":to_map,"spawn":spawn}; break
                elif et == 'message': event = {"type":"message","text":ev.get('text','')}
        return {"moved": moved, "event": event}

    # battle
    def start_battle(self, enemies: Optional[List[Dict[str, Any]]] = None) -> None:
        if enemies: self.enemies = [dict(e) for e in enemies]
        self.phase = 'select'; self.active_index = 0; self.menu_index = 0; self.target_index = 0; self.selected_actions = []

    def select_menu(self, dir: int): self.menu_index = (self.menu_index + dir) % 4
    def focus_next_target(self, dir: int):
        if self.enemies: self.target_index = (self.target_index + dir) % len(self.enemies)

    def confirm_selection(self, cmd: str) -> str:
        if self.phase == 'select':
            if cmd in ('たたかう','スキル') and self.enemies:
                self.phase = 'target'; return self.phase
            self._store_action(cmd, target=None); return self._advance_or_resolve()
        elif self.phase == 'target':
            target = self.enemies[self.target_index]['name'] if self.enemies else None
            self._store_action(cmd, target=target); self.phase = 'select'; return self._advance_or_resolve()
        return self.phase

    def _store_action(self, cmd: str, target: Optional[str]):
        self.selected_actions.append({"name": self.party[self.active_index]["name"], "cmd": cmd, "target": target})

    def _advance_or_resolve(self) -> str:
        self.active_index += 1; self.menu_index = 0; self.target_index = 0
        if self.active_index >= len(self.party): self.phase = 'resolve'
        return self.phase

    def reset_turn(self) -> None: self.start_battle(enemies=self.enemies)