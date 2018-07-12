from harc.plugin.Plugable import Plugable
import os.path


class Generate(Plugable):
    def __init__(self):
        Plugable.__init__(self)
        pass

    @staticmethod
    def execute(arguments, settings, properties):
        projects = settings['projects']

        print properties['harc_dir']
        properties['template_dir'] = properties['plugin_dir'] + os.sep + 'template'

        path, filename = os.path.split(arguments.f)
        filename, ext = os.path.splitext(filename)
        print path, filename, ext

        # retrieve the project_alias and table_name from the given filename
        project_alias, table_name = filename.split('_')

        print project_alias, table_name

        file = open(arguments.f)
        data = file.read()
        # todo: windows and mac files
        lines = data.split(chr(10))
        file.close()

        columns = []
        for line in lines:
            # todo : guess the column seperator
            # todo : tests the number of columns in the file
            column = {}
            column['name'], column['type'], column['nullable'], column['default'], column['in'] = line.split('|')
            columns.append(column)

        print columns
        print properties['template_dir']
        for root, dirnames, filenames in os.walk(properties['template_dir']):
            if filenames:
                print root, filenames



