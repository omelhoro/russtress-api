from flask import Flask,Blueprint, render_template, abort,request
from jinja2 import TemplateNotFound
from setstress import setup_stress
import json

def setup_rs(cl=Blueprint):
    if cl==Flask:
        simple_page = cl(__name__,template_folder='web')
        homeroute="/" 
    else:
        simple_page = cl("rust",__name__,static_folder='web',template_folder='web')
        homeroute="/rustress"
    @simple_page.route(homeroute)
    def rustress():
        return render_template("index.html")

    try:
        set_stress,pm=setup_stress("./rustress/dict_data")
    except:
        set_stress,pm=setup_stress("./dict_data")

    @simple_page.route("/stress")
    def stress():
        return json.dumps({k:list(set_stress(pm,k)) for k,v in request.args.items()})
    return simple_page

if __name__ == "__main__": 
    app=setup_rs(Flask)
    app.debug = True
    app.run()
