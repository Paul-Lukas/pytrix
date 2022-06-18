from flask import Flask, render_template


class WebApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.set_endpoints()

    def set_endpoints(self):
        self.app.add_url_rule('/', 'menu', self.main_menu, methods=['GET'])

    def run(self):
        self.app.run(debug=True)

    def main_menu(self):
        # TODO: get list dynamically from Base
        plugins = [
            [0, "erstes Plug"],
            [1, "zweites plug"],
            [2, "drittes plug"]
        ]

        return render_template('menu.html', plugins=plugins)


if __name__ == "__main__":
    app = WebApp()
    app.run()
