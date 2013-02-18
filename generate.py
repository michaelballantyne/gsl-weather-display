#!/usr/bin/env python

import json, os, argparse, time, logging, logging.handlers, shutil
from jinja2 import Environment, FileSystemLoader
import lakelevel_data, hatisland_data

def ensure_directory_exists(path):
    try: 
        os.makedirs(path)
    except OSError:
        if not os.path.isdir(path):
            raise

def html(data, templatepath):
    jinja_env = Environment(loader=FileSystemLoader(os.path.dirname(templatepath)))
    template = jinja_env.get_template(os.path.basename(templatepath))
    return template.render(data)

def loadjson(filename):
    with open(filename) as jsonfile:
        return json.load(jsonfile)

def setup_logging(log_file):
    logging.getLogger().addHandler(logging.handlers.TimedRotatingFileHandler(log_file, when="D", backupCount=5))
    logging.getLogger().setLevel(logging.INFO)

    logging.getLogger().addHandler(logging.StreamHandler())

if __name__ == '__main__':
    parser = argparse.ArgumentParser("Download data and generate GSL info page.")
    parser.add_argument('--loadjson', action='store_true', help='Load parsed data from json rather than redownloading and reparsing. Useful for development and testing.')
    parser.add_argument('--errormsg', help='Specify error message to show on page when generate fails.', default='An error occurred and the information shown is out of date.')
    args = parser.parse_args()

    script_directory = os.path.dirname(os.path.realpath(__file__)) 

    data_dir = os.path.join(script_directory, "data")
    log_filename = os.path.join(data_dir, 'log.txt')
    jsonfilename = os.path.join(data_dir, 'processed.json')
    output_dir = os.path.join(script_directory, 'output')
    output_filename = os.path.join(output_dir, 'index.html')
    template_filename = os.path.join(script_directory, 'template.html')

    ensure_directory_exists(data_dir)

    setup_logging(log_filename)

    provider_classes = [lakelevel_data.LevelDataProvider, hatisland_data.WeatherDataProvider]
    providers = [x() for x in provider_classes]

    data = {}

    try:
        if args.loadjson:
            data = loadjson(jsonfilename)
        else:
            # Dictionary mapping provider key to list of stream objects of the files that provider 
            # needs to download and process. Download and processing steps are separate to make it 
            # easy to do something else in the middle, like save out a copy of the downloaded files.
            datafilesets = {}
            try:
                # Ask providers for connections to needed files
                for provider in providers:
                    key = provider.get_key()
                    datafilesets[provider.get_key()] = provider.download_latest_data() 

                    # Write files out to data folder, then reopen for reading. Useful to have them there for debugging.
                    for index, item in enumerate(datafilesets[key]):
                        savefilename = os.path.join(data_dir, key + str(index))
                        with open(savefilename, "w") as savefile:
                            shutil.copyfileobj(item, savefile)
                        datafilesets[key][index] = open(savefilename)

                # Ask providers to process data
                for provider in providers:
                    data[provider.get_key()] = provider.process_data(datafilesets[provider.get_key()])

                # Store UTC epoch seconds so client can detect if page is out of date.
                data['generated'] = int(time.time())

                # Save result of run to json so that we can use if a future run fails.
                with open(jsonfilename, 'w') as jsonfile:
                    json.dump(data, jsonfile, indent=4)

            finally:
                # Ensure we close our connections.
                for fileset in datafilesets.values():
                    for file in fileset:
                        file.close()

    except Exception as e:
        try:
            logging.exception('Generate failed.')
        except:
            pass

        try:
            # Show data from most recent successful run, if possible.
            data = loadjson(jsonfilename)
        except:
            data = {}

        data['showerror'] = True


    # Regardless of the state of the data, make sure the client has the appropriate error message to display if needed.
    data['errormsg'] = args.errormsg

    with open(output_filename, 'w') as out:
        out.write(html(data, template_filename))
