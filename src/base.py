import inspect
import os
import pathlib
import pkgutil

import requests
import zipfile
import shutil
import asyncio


from src.input.webApp import WebApp
from src.plugins.basePlugin import BasePlugin


class Base:
    def __init__(self, config):
        self.config = config

        width = config.get_config()['main']['width']
        height = config.get_config()['main']['height']

        self.blocklist = ["__pycache__", "system", "basePlugin.py", "__init__.py"]

        if self.config.get_config()['main']['use Simulation Gui'] == "True":
            # TODO: use sim not shellout (make Tkinter work with threads)
            print("Importing Sim")
            from src.output.shellout import Shellout
            self.output = Shellout(width, height)
        else:
            print("Importing Board")
            # noinspection PyUnresolvedReferences
            import board
            # noinspection PyUnresolvedReferences
            import neopixel

            # TODO: Get raspy gpio pin from config
            strip_lengh = int(width) * int(height)
            pixels = neopixel.NeoPixel(board.D18, strip_lengh, auto_write=False)

            from src.output.matrix import NeoMatrix
            self.output = NeoMatrix(int(width), int(height), pixels)

        self.plugins = []

    def generate_plugin_list(self):
        i = 0
        plug_dir_paths = []
        rootpath = os.path.join(pathlib.Path(__file__).parent.resolve(), 'plugins')

        dir_content = os.listdir(rootpath)
        for content in dir_content:
            if content in self.blocklist:
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
                                i = i + 1
                                print(f'    Finished plugin class: {c.__module__}.{c.__name__}')
                    except Exception as e:
                        print("Error trying to add Plugin: ")
                        print(e)

    def get_plugin_site(self, plug_id):
        return self.plugins[int(plug_id)][2].get_html()

    async def run_plugin(self, plug_id):
        try:
            self.plugins[int(plug_id)][2].run()
        except asyncio.CancelledError as e:
            print("Stopping Plugin")
        finally:
            print("Plugin stopped")
            
        # TODO: Reverte Hotfix
        
    def input_plugin(self, plug_id, input_str):
        return self.plugins[int(plug_id)][2].input(input_str)

    def download_plugins(self):
        # TODO: Add Try except
        url = self.config.get_config()['main']['Update Url']
        plug_path = os.path.join(pathlib.Path(__file__).parent.resolve(), 'plugins')
        plug_system_path = os.path.join(plug_path, 'system')
        plug_zip_path = os.path.join(plug_system_path, 'plugins.zip')

        r = requests.get(url, stream=True)
        with open(plug_zip_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=128):
                f.write(chunk)

        with zipfile.ZipFile(plug_zip_path, 'r') as zip_ref:
            zip_ref.extractall(plug_system_path)
        os.remove(plug_zip_path)

        print('     Downloaded and extracted zip-file')

        file_names = os.listdir(plug_path)
        for file_name in file_names:
            if file_name in self.blocklist:
                continue
            shutil.rmtree(os.path.join(plug_path, file_name))

        dir_names = os.listdir(os.path.join(plug_system_path, "pytrix_plugins-main", "plugins"))
        for dir_name in dir_names:
            if os.path.isdir(os.path.join(plug_system_path, "pytrix_plugins-main", "plugins", dir_name)):
                os.mkdir(os.path.join(plug_path, dir_name))
                file_names = os.listdir(os.path.join(plug_system_path, "pytrix_plugins-main", "plugins", dir_name))
                for file_name in file_names:
                    shutil.move(
                        os.path.join(plug_system_path, "pytrix_plugins-main", "plugins", dir_name, file_name),
                        os.path.join(plug_path, dir_name, file_name)
                    )
        print('     moved plugins')

    def run(self):
        self.download_plugins()
        print("Plugin Download finished")
        self.generate_plugin_list()
        print("trying to create Webinterface")
        web_app = WebApp(self)
        web_app.run()
