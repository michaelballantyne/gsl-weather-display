# -*- coding: utf-8 -*-

from jinja2 import Environment, FileSystemLoader
import lakelevel_data
import hatisland_data

def html(data):
    jinja_env = Environment(loader=FileSystemLoader("."))
    gsl_template = jinja_env.get_template("template.html")
    return gsl_template.render(data)

if __name__ == "__main__":
    data = {}
    data["leveldata"] = lakelevel_data.get_data()
    data["hatisland"] = hatisland_data.get_data()

    print html(data)
