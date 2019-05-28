import click
from harc.system.Profile import Profile


class UsernameOption(click.Option):

    def get_default(self, ctx):
        properties = ctx.obj
        project_name = properties.get('name')
        username = None
        credentials = Profile.credentials(project_name, properties)
        if credentials:
            username = credentials.get('username')
        self.default = username
        return super(UsernameOption, self).get_default(ctx)
