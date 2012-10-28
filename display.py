# -*- coding: utf-8 -*-

from jinja2 import Environment, FileSystemLoader

def html(informatics):
    jinja_env = Environment(loader=FileSystemLoader("display-templates"))
    gsl_template = jinja_env.get_template("gsl.html")
    return gsl_template.render(informatics)
