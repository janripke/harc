import os
import json


class Config:

    @staticmethod
    def load(properties):
        """
        Retrieve the config from the config file in your home folder if present.
        """
        config = None

        # load the users from the credentials file, if present
        home_dir = properties.get('home.dir')
        config_file = os.path.join(home_dir, '.harc', 'config.json')
        if os.path.isfile(config_file):
            f = open(config_file, 'r')
            config = json.load(f)
            f.close()

        return config
