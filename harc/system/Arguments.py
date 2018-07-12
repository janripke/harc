import argparse


class Arguments:
    def __init__(self, description):
        self.__arguments = []
        self.__parser = argparse.ArgumentParser(description=description)

    def get_arguments(self):
        return self.__arguments

    def add_argument(self, argument):
        parser = self.get_parser()
        parser.add_argument(argument['argument'], type=type(argument['type']), help=argument['help'])
        arguments = self.get_arguments()
        arguments.append(argument)

    def get_parser(self):
        return self.__parser

    def parse_args(self, args=None):
        parser = self.get_parser()
        return parser.parse_args(args)

    def parse_content(self, content):
        results = []
        arguments = self.get_arguments()
        for argument in arguments:
            for key in content:
                if argument["argument"] == key:
                    if argument["argument"] != "command":
                        results.append(argument['argument'])
                    results.append(content[key])
        return self.parse_args(results)
