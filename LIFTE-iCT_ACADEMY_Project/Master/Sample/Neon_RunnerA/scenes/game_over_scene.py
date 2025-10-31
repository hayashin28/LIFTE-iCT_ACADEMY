class GameOverScene:
    def __init__(self, navigator):
        self.nav = navigator
    def on_retry(self):
        self.nav.goto_game(reset=True)
    def on_exit(self):
        self.nav.goto_title()
