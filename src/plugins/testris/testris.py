import time

from ..basePlugin import BasePlugin


class Testris(BasePlugin):
    def __init__(self, app, output):
        super().__init__(app, output)
        self.pluginName = "Testris"
        self.version = "pre 0.1"

    def run(self):
        print("tetris")
        while True:
            self.out.fill_all((0, 0, 0))
            time.sleep(5)
        print("fin")

    def input(self, inp):
        pass
