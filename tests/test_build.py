import sys
import json
import os
import shutil

if __name__ == '__main__':
    arguments = sys.argv
    environment = arguments[2]
    print environment

    settings_file = arguments[1]+'.build'
    if os.path.isfile(settings_file):

        data = open(settings_file)
        settings = json.load(data)

        target_folder = settings['target']
        if not os.path.isdir(target_folder):
            os.mkdir(target_folder)

        build_folder = settings['target'] + os.sep + settings['name']
        if os.path.isdir(build_folder):
            shutil.rmtree(build_folder)
            os.mkdir(build_folder)
        if not os.path.isdir(build_folder):
            os.mkdir(build_folder)

        files = settings['files']
        for file in files:
            shutil.copy(file, build_folder + os.sep + file)

        packages = settings['packages']
        for package in packages:
            shutil.copytree(package, build_folder + os.sep + package)

        excludes = settings['excludes']
        for exclude in excludes:
            shutil.rmtree(build_folder + os.sep + exclude)

        specifics = settings['specifics']
        for specific in specifics:
            print specific
            if os.path.isdir(specific + os.sep + environment):
                shutil.copytree(specific + os.sep + environment, build_folder + os.sep + specific)
            else:
                shutil.copytree(specific, build_folder + os.sep + specific)