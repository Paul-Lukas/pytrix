from ..basePlugin import BasePlugin
import time

class Testris(BasePlugin):
    def __init__(self, app, output):
        super().__init__(app, output)
        self.pluginName = "Testris"
        self.version = "pre 0.1"

    def run(self):
        print("tetris")
        self.out.fill_all((0,0,0))
        print("fin")