from harc.system.Profile import Profile
from harc.system.PipUrlParse import PipUrlParse


class Requirements:
    @staticmethod
    def tokenize(lines, credentials):
        """
        Tokenize a set of pip requirements and insert username/password for
        urls that match any found in the provided credentials.

        :param lines: List of pip requirements
        :param credentials: A dict containing hostname / username+password keys and values
        :return: A list of tokenized pip requirements
        """
        results = []
        for line in lines:
            # ignore comments and empty lines
            if not line.startswith("#") and line.strip():
                pip_url = PipUrlParse(line)
                hostname = pip_url.get_hostname()
                if hostname in credentials:
                    line = pip_url.tokenize(
                        credentials[hostname]['user'], credentials[hostname]['password'])

            results.append(line)
        return results
