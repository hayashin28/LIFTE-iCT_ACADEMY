class HUD:
    def __init__(self, scoring_service, difficulty_service):
        self.svc_s = scoring_service; self.svc_d = difficulty_service
    def get_labels(self) -> dict:
        s = self.svc_s.current; d = self.svc_d.current
        return {"score": f"Score: {s}", "speed": f"Speed: x{d.speed:.2f} (Lv.{d.stage})"}
