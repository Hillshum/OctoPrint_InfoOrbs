# coding=utf-8
from __future__ import absolute_import

from dataclasses import dataclass
import octoprint.settings

import flask


import octoprint.plugin

from . import orbs

@dataclass
class Display:
    label: str
    data: str|int|float
    labelColor: str
    color: str
    background: str
    alignment: str

class InfoOrbsResponse:

    def __init__(self, interval=5000, displays=[]):
        self.interval = interval
        self.displays = displays


    def build_json(self):
        return {
            "interval": self.interval,
            "displays": [d.render() for d in self.displays]
        }

class InfoorbsPlugin(octoprint.plugin.SettingsPlugin,
    octoprint.plugin.AssetPlugin,
    octoprint.plugin.SimpleApiPlugin,
):


    ##~~ SettingsPlugin mixin

    def get_settings_defaults(self):
        return {
            # put your plugin's default settings here
        }

    ##~~ AssetPlugin mixin

    def get_assets(self):
        # Define your plugin's asset files to automatically include in the
        # core UI here.
        return {
            "js": ["js/InfoOrbs.js"],
            "css": ["css/InfoOrbs.css"],
            "less": ["less/InfoOrbs.less"]
        }

    def on_api_get(self, request):
        # get selected file from octoprint
        selected_file = self._printer.get_current_job()["file"]["name"]

        temp = self._printer.get_current_temperatures()

        tempOrb = orbs.TempOrb(temp)

        current_status = self._printer.get_current_data()

        progressOrb = orbs.ProgressOrb(current_status)


        resp = InfoOrbsResponse()

        resp.displays = [tempOrb, progressOrb, orbs.Orb(), orbs.Orb(), orbs.Orb()]

        d = resp.build_json()
        return flask.jsonify(d)

    ##~~ Softwareupdate hook

    def get_update_information(self):
        # Define the configuration for your plugin to use with the Software Update
        # Plugin here. See https://docs.octoprint.org/en/master/bundledplugins/softwareupdate.html
        # for details.
        return {
            "InfoOrbs": {
                "displayName": "Infoorbs Plugin",
                "displayVersion": self._plugin_version,

                # version check: github repository
                "type": "github_release",
                "user": "hillshum",
                "repo": "OctoPrint-InfoOrbs",
                "current": self._plugin_version,

                # update method: pip
                "pip": "https://github.com/hillshum/OctoPrint-InfoOrbs/archive/{target_version}.zip",
            }
        }


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "Infoorbs Plugin"


# Set the Python version your plugin is compatible with below. Recommended is Python 3 only for all new plugins.
# OctoPrint 1.4.0 - 1.7.x run under both Python 3 and the end-of-life Python 2.
# OctoPrint 1.8.0 onwards only supports Python 3.
__plugin_pythoncompat__ = ">=3,<4"  # Only Python 3

def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = InfoorbsPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }
