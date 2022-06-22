class BasePlugin:
    version = None
    pluginName = None

    def __init__(self, app, output):
        self.app = app
        self.out = output

        self.version = "blah"
        self.pluginName = "blah"

    def run(self):
        raise NotImplementedError

    def input(self, inp):
        pass

    def get_html(self):
        return "No Site Set"

    @classmethod
    def get_name(cls):
        return cls.pluginName

    @classmethod
    def get_version(cls):
        return cls.version
