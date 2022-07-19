from flask import Flask, render_template, render_template_string, request

class WebApp:
    def __init__(self, base):
        self.plugins = base.plugins
        self.base = base

        self.app = Flask(__name__)
        self.set_endpoints()

        self.plugin_running = 0

    def set_endpoints(self):
        self.app.add_url_rule('/', 'menu', self.main_menu, methods=['get'])
        self.app.add_url_rule('/plugin/<int:plug_id>', 'plugin', self.plugin, methods=['get'])
        self.app.add_url_rule('/plugin/<string:plug_id>/input', 'input', self.input, methods=['get'])

    async def input(self, plug_id):
        plug_id = int(plug_id)
        input_str = request.args

        # main application has id -1
        if plug_id == -1:
            #if self.plugin_running != 0:
                # TODO: Anzeige, dass schon Plugin läuft
            #    print(
            #        f"plugin {self.plugin_running} is already running, unable to start more than one plugin at the same time")
            #    return ""

            start_id = input_str.get("start_id")
            self.plugin_running = start_id
            await self.base.run_plugin(start_id)
            self.plugin_running = 0
            # TODO: return anpassen
            return ""
        else:
            # TODO: disable passing input if plugin does not run
            # TODO: return anpassen
            self.base.input_plugin(plug_id, input_str)
            return ""

    def plugin(self, plug_id):
        plugin_id, plugin_name, plugin = self.plugins[int(plug_id)]
        plug_html = render_template_string(self.base.get_plugin_site(plugin_id), start_name=plugin_name,
                                           start_id=plugin_id)
        return render_template('start.html', plugins=self.plugins, plug_html=plug_html, start_name=plugin_name,
                               start_id=plugin_id)

    def main_menu(self):
        return render_template('menu.html', plugins=self.plugins)

    def run(self):
        self.app.run(debug=False, host="0.0.0.0")
