import os
import pathlib

from flask import Flask, render_template, request


class WebApp:
    def __init__(self, base):
        self.plugins = base.plugins
        self.base = base

        self.app = Flask(__name__)
        self.set_endpoints()

    def set_endpoints(self):
        self.app.add_url_rule('/', 'menu', self.main_menu, methods=['GET'])
        self.app.add_url_rule('/plugin/<int:plug_id>', 'plugin', self.plugin, methods=['GET'])
        self.app.add_url_rule('/plugin/<int:plug_id>/input', 'plug_input', self.imput, methods=['GET'])

    def run(self):
        self.app.run(debug=False)

    def imput(self, plug_id):
        input_str = request.args
        self.base.input_plugin(plug_id, input_str)
        # TODO: Return anpassen
        return 'hui input'

    def plugin(self, plug_id):
        # TODO: get plugin page
        # plug_site = self.base.get_plugin_site(plug_id)
        # self.base.run_plugin(plug_id)
        start_path = os.path.join(pathlib.Path(__file__).parent.resolve(), 'static', 'html', 'start.html')

        with open(start_path, "r") as f:
            plug_html = f.read()

        return render_template('menu.html', plugins=self.plugins, plug_html=plug_html)

    def main_menu(self):
        return render_template('menu.html', plugins=self.plugins, plug_html="")
