import click
from harc.system.Profile import Profile


class PasswordOption(click.Option):

    def get_default(self, ctx):
        properties = ctx.obj
        project_name = properties.get('name')
        password = None
        credentials = Profile.credentials(project_name, properties)
        if credentials:
            password = credentials.get('password')
        self.default = password
        return super(PasswordOption, self).get_default(ctx)
