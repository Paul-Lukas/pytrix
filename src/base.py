import inspect
import os
import pathlib
import pkgutil

from src.input.webApp import WebApp
from src.plugins.basePlugin import BasePlugin


class Base:
    def __init__(self, config):
        self.config = config

        width = config.get_config()['main']['width']
        height = config.get_config()['main']['height']

        if self.config.get_config()['main']['use Simulation Gui']:
            # TODO: use sim not shellout (make Tkinter work with threads)
            print("Importing Sim")
            from src.output.shellout import Shellout
            self.output = Shellout(width, height)
        else:
            print("Importing Board")
            import board
            import neopixel

            # TODO: Get pin from config
            strip_lengh = width * height
            pixels = neopixel.NeoPixel(board.D18, strip_lengh, auto_write=False)

            from src.output.matrix import NeoMatrix
            self.output = NeoMatrix(width, height, pixels)

        self.plugins = []
        self.generate_plugin_list()

    def generate_plugin_list(self):
        i = 0
        plug_dir_paths = []
        rootpath = os.path.join(pathlib.Path(__file__).parent.resolve(), 'plugins')

        dir_content = os.listdir(rootpath)
        for content in dir_content:
            # TODO: change to block list
            if content == '__pycache__':
                continue

            if os.path.isdir(os.path.join(rootpath, content)):
                plug_dir_paths.append('src.plugins.' + str(content))

        for plug_dir in plug_dir_paths:
            print(plug_dir)
            imported_package = __import__(plug_dir, fromlist=['blah'])

            for _, plugin_name, ispkg in pkgutil.iter_modules(imported_package.__path__,
                                                              imported_package.__name__ + '.'):
                if not ispkg:
                    try:
                        plugin_module = __import__(plugin_name, fromlist=['blah'])
                        cls_members = inspect.getmembers(plugin_module, inspect.isclass)
                        for (_, c) in cls_members:
                            # Only add classes that are a subclass of Plugin, but NOT Plugin itself
                            if issubclass(c, BasePlugin) & (c is not BasePlugin):
                                print(f'    Found plugin class: {c.__module__}.{c.__name__}')
                                plugin = c(self, self.output)
                                plugin_item = (i, plugin.pluginName, plugin)
                                self.plugins.append(plugin_item)
                                i = + 1
                                print(f'    Finished plugin class: {c.__module__}.{c.__name__}')
                    except Exception as e:
                        print("Error trying to add Plugin: ")
                        print(e)

    def get_plugin_site(self, plug_id):
        self.plugins[int(plug_id)][2].get_website()

    def run_plugin(self, plug_id):
        self.plugins[int(plug_id)][2].run()

    def input_plugin(self, plug_id, input_str):
        # Main Application has id -1
        if plug_id == -1:
            input_str.get("start")

        else:
            self.plugins[int(plug_id)][2].input(input_str)

    def run(self):
        # TODO: create Webinterface and parse List (async)

        print("trying to create Webinterface")
        web_app = WebApp(self)
        web_app.run()
        print("WebInterface Running")
