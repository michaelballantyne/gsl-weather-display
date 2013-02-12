#!/usr/bin/env python

import json, os, argparse, shutil
from jinja2 import Environment, FileSystemLoader
import lakelevel_data, hatisland_data

def ensure_directory_exists(path):
    try: 
        os.makedirs(path)
    except OSError:
        if not os.path.isdir(path):
            raise

def html(data):
    jinja_env = Environment(loader=FileSystemLoader("."))
    gsl_template = jinja_env.get_template("template.html")
    return gsl_template.render(data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser("Download data and generated gsl info page")
    parser.add_argument("--save", action="store_true", help="write out downloaded datafiles for later use")
    parser.add_argument("--load", action="store_true", help="load data from previously downloaded datafiles instead of downloading now")
    parser.add_argument("--savejson", action="store_true", help="write parsed data out to json for later use")
    parser.add_argument("--loadjson", action="store_true", help="load parsed data from json rather than redownloading and reparsing")
    parser.add_argument("--nogenerate", action="store_true", help="don't generate html")

    args = parser.parse_args()

    cwd = os.path.dirname(os.path.realpath(__file__)) 
    data_dir = os.path.join(cwd, "data")
    ensure_directory_exists(data_dir)

    provider_classes = [lakelevel_data.LevelDataProvider, hatisland_data.WeatherDataProvider]
    providers = [x() for x in provider_classes]

    data = {}

    if args.loadjson:
        jsonfilename = os.path.join(data_dir, "processed.json")
        jsonfile = open(jsonfilename)
        data = json.load(jsonfile)
    else:
        datafilesets = {}
        if args.load:
            for provider in providers:
                key = provider.get_key()
                datafilesets[key] = [open(os.path.join(data_dir, x)) for x in sorted(os.listdir(data_dir)) if x.startswith(key)]

        else:
            for provider in providers:
                key = provider.get_key()
                datafilesets[provider.get_key()] = provider.download_latest_data() 
                if args.save:
                    for index, item in enumerate(datafilesets[key]):
                        savefilename = os.path.join(data_dir, key + str(index))
                        savefile = open(savefilename, "w")
                        shutil.copyfileobj(item, savefile)

        for provider in providers:
            data[provider.get_key()] = provider.process_data(datafilesets[provider.get_key()])

        if args.savejson:
            jsonfilename = os.path.join(data_dir, "processed.json")
            jsonfile = open(jsonfilename, "w")
            json.dump(data, jsonfile, indent=4)


    if not args.nogenerate:
        out = open(os.path.join(cwd, "output", "out.html"), "w")
        out.write(html(data))
