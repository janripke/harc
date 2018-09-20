from harc.system.io.Files import Files
import harc
import os

harc_dir = os.path.dirname(harc.__file__)
plugin_dir = os.path.join(harc_dir, 'plugins')

template_dir = os.path.join(plugin_dir, 'aws', 'generate', 'templates')
lambda_dir = os.path.join(template_dir, 'lambda')
files = Files.list(template_dir)
for file in files:
    print(file.replace(template_dir,'').lstrip(os.sep))