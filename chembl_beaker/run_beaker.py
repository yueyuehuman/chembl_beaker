#!/usr/bin/env python

__author__ = 'mnowotka'

# ----------------------------------------------------------------------------------------------------------------------

import json
from bottle import run
from optparse import OptionParser
from chembl_beaker.beaker import app, config, loadPlugins, loadApps

# ----------------------------------------------------------------------------------------------------------------------


parser = OptionParser()
parser.add_option("-c", "--config", dest="config_path", help="path to config file", default="beaker.conf")
(options, args) = parser.parse_args()
conf_path = options.config_path

config.load_config(conf_path)

apps = json.loads(config.get('installed_apps', '[]'))
plugins = json.loads(config.get('plugins', '[]'))

loadApps(apps)
loadPlugins(app, plugins)

# ----------------------------------------------------------------------------------------------------------------------


def main():

    server = config.get('server_middleware', 'tornado')
    kwargs = {}
    if server is 'gunicorn':
        try:
            kwargs['workers'] = int(config.get('workers', '4'))
        except Exception as e:
            print e.message
            kwargs['workers'] = 4

    run(app=app, host=config.get('bottle_host', 'localhost'), port=config.get('bottle_port', '8080'),
        debug=config.get('debug', True), server=server, **kwargs)

if __name__ == "__main__":
    main()

else:
    application = app

# ----------------------------------------------------------------------------------------------------------------------
