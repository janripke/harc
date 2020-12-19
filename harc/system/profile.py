import os
import json


def credentials(name, properties):
    """
    Retrieve the credentials from the credentials file in your home folder if present.
    """
    profile = None

    # load the users from the credentials file, if present
    home_dir = properties.get('home.dir')
    credentials_file = os.path.join(home_dir, '.harc', 'credentials.json')
    if os.path.isfile(credentials_file):
        f = open(credentials_file, 'r')
        credentials = json.load(f)
        f.close()

        profile = credentials.get(name)
    return profile
