from harc.system.Profile import Profile
from harc.system.PipUrlParse import PipUrlParse


class Requirements:
    @staticmethod
    def tokenize(lines, properties):

        # resolve the egg_name, so the egg_name is required for this work around.
        results = list()
        for line in lines:
            # ignore comments
            if not line.startswith("#"):

                pip_url = PipUrlParse(line)
                egg_name = pip_url.egg_name()
                if egg_name:

                    credentials = Profile.credentials(egg_name, properties)
                    username = credentials['username']
                    password = credentials['password']

                    line = pip_url.tokenize(username, password)

            results.append(line)
        return results
