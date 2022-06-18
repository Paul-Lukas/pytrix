class BasePlugin:
    # TODO: get output File

    version = None
    pluginName = None

    def __init__(self, app, output):
        self.app = app
        self.out = output

        self.version = "blah"
        self.pluginName = "blah"

    def run(self):
        raise NotImplementedError

    @classmethod
    def get_name(cls):
        return cls.pluginName

    @classmethod
    def get_version(cls):
        return cls.version
