import configparser
import os


class Config:
    def __init__(self):
        self.config_version = "0.3"

        self.config = configparser.ConfigParser()
        dirName = os.path.dirname(os.path.abspath(__file__))
        self.fileName = os.path.join(dirName, "..", "config.txt")
        if not os.path.exists(self.fileName):
            print("Config generated")
            self.generate_defaults()
        else:
            print("Config exists")
            if not self.check_config():
                os.remove(self.fileName)
                self.generate_defaults()
            else:
                self.read_config()

    def generate_defaults(self):
        self.config['main'] = {'Version': self.config_version, 'Update Url': 'https://github.com/Paul-Lukas/pytrix_plugins/archive/refs/heads/main.zip', 'use Simulation Gui': True, 'width': 15, 'height': 30, 'orientation': '1'}
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

    def check_config(self) -> bool:
        if not self.config.has_option('main', 'Version'):
            return False

        if self.config['main']['version'] != self.config_version:
            return False
        return True

    # TODO: register plugins with individual config
    def register_plugin(self, name, version):
        self.config[name] = {'version': version}
        self.write_config(self.config)
