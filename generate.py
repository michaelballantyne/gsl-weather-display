# -*- coding: utf-8 -*-

from jinja2 import Environment, FileSystemLoader

def html(informatics):
    jinja_env = Environment(loader=FileSystemLoader("."))
    gsl_template = jinja_env.get_template("template.html")
    return gsl_template.render(informatics)
