from flask import Flask, Blueprint, render_template, request
try:
    from .setstress import setup_stress
except SystemError:
    from setstress import setup_stress
except ValueError:
    from setstress import setup_stress

import json


def setup_rs(cl=None):
    if cl == Flask:
        simple_page = Flask(__name__)
        homeroute = "/"
    else:
        simple_page = Blueprint("rust",__name__,template_folder='templates')
        homeroute = "/rustress"

    @simple_page.route(homeroute)
    def rustress():
        return render_template("index.html")

    try:
        set_stress, pm = setup_stress("./rustress/dict_data")
    except (IOError):
        try:
            set_stress, pm = setup_stress("./dict_data")
        except (IOError):
            set_stress, pm = setup_stress("./mysite/rustress/dict_data")

    @simple_page.route("/stress/", methods = ["POST"])
    def stress():
        data = request.data.decode("utf8")
        jsn = json.loads(data)["words"]
        print("Request", jsn)
        out = json.dumps({k: list(set_stress(pm, k)) for k in jsn})
        print(out)
        return out

    return simple_page

if __name__ == "__main__":
    app = setup_rs(Flask)
    #app.debug = True
    app.run(host='0.0.0.0', port=5001)
