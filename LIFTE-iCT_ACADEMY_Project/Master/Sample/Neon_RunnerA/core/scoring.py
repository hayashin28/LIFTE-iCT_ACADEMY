from dataclasses import dataclass
DEFAULT_AVOID_POINT = 10

@dataclass
class Score:
    value: int = 0

class ScoringService:
    def __init__(self, avoid_point: int = DEFAULT_AVOID_POINT):
        self._score = Score(); self._avoid_point = int(avoid_point)
    def reset(self) -> None:
        self._score.value = 0
    def add_for_avoid(self, points: int | None = None) -> None:
        p = self._avoid_point if points is None else int(points)
        if p < 0: p = 0
        self._score.value += p
    @property
    def current(self) -> int:
        return self._score.value
