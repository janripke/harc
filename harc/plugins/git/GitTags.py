from harc.system.System import System
from harc.system.Git import Git
import click
import logging
from harc.plugins.UsernameOption import UsernameOption
from harc.plugins.PasswordOption import PasswordOption
from urllib.parse import urlparse, quote


class GitTags:

    @click.command()
    @click.option('-u', '--username', cls=UsernameOption, required=True)
    @click.option('-p', '--password', cls=PasswordOption, required=True)
    @click.pass_context
    def execute(ctx, username, password):
        logger = logging.getLogger()
        logger.debug("username : {}".format(username))

        # retrieve the properties, set by the cli
        properties = ctx.obj

        url = urlparse(properties['repository'])
        repository = properties['repository']

        if url.scheme in ['http', 'https']:

            repository = url.scheme + "://'{0}':'{1}'@" + url.netloc + url.path
            repository = repository.format(quote(username), quote(password))

        # create an empty folder in tmp
        tmp_folder = System.recreate_tmp(properties['name'])

        # clone the repository to the tmp_folder
        print("Clone")
        result = Git.clone(repository, tmp_folder)
        print(str(result))

        # retieve the tags
        print("Tags:")
        tags = Git.tags(tmp_folder)
        for tag in tags:
            print(tag)
