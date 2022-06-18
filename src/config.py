import configparser
import os


class Config:
    def __init__(self):
        self.config = configparser.ConfigParser()
        dirName = os.path.dirname(os.path.abspath(__file__))
        self.fileName = os.path.join(dirName, "..", "config.txt")
        if not os.path.exists(self.fileName):
            print("Config generated")
            self.generate_defaults()
        else:
            print("Config exists")
            # TODO: Check if config is complete
            self.read_config()

    def generate_defaults(self):
        self.config['main'] = {'use Simulation Gui': True, 'width': 15, 'height': 30, 'orientation': '1'}
        self.write_config(self.config)

    def read_config(self):
        print("Config read:")
        print(self.config.read(self.fileName))

    def get_config(self):
        return self.config

    def change_config(self, category, name, value):
        self.config[category][name] = value
        self.write_config(self.config)

    def write_config(self, config):
        with open(self.fileName, "w") as configfile:
            config.write(configfile)
            print("Config saved")

    # TODO: register plugins with individual config
    def register_plugin(self, name, version):
        self.config[name] = {'version': version}
        self.write_config(self.config)
