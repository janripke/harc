import json
import os
import inspect

from harc.consumers.Consumable import Consumable
from harc.system.HarcCliArguments import HarcCliArguments
from harc.plugins.PluginFactory import PluginFactory


class ExecuteJob(Consumable):
    def __init__(self):
        Consumable.__init__(self)

    def action(self, message):
        payload = json.loads(message['payload'])

        parser = HarcCliArguments("Harc, hit and release code")
        args = parser.parse_content(payload)

        data = open("harc.json")
        settings = json.load(data)

        properties = {}
        properties['harc_dir'] = os.path.abspath('.')
        properties['job_name'] = payload['job_name']

        plugin = PluginFactory.create_plugin(args.command)

        path, filename = os.path.split(inspect.getfile(plugin))
        properties['plugin_dir'] = path

        plugin.execute(args, settings, properties)




