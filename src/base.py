import inspect
import os
import pathlib
import pkgutil

from src.plugins.basePlugin import BasePlugin


class Base:
    def __init__(self, config):
        self.config = config

        width = config.get_config()['main']['width']
        height = config.get_config()['main']['height']

        # if gconfig.get_config()['main']['use Simulation Gui']:
        # TODO: import oanly nesassary libs
        from src.output.simulator import Simulator
        # TODO: Create output from import

        self.output = Simulator(width, height)

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
                                print('    Found plugin class: {c.__module__}.{c.__name__}')
                                plugin = c(self, self.output)
                                plugin_item = (i, plugin.pluginName, plugin)
                                self.plugins.append(plugin_item)
                                i = + 1
                                print('    Finished plugin class: {c.__module__}.{c.__name__}')
                    except Exception as e:
                        print("Error trying to add Plugin: ")
                        print(e)

    def run(self):
        # TODO: create Webinterface and parse List (async)

        print("Start running")
        for plugin in self.plugins:
            plugin[2].run()
