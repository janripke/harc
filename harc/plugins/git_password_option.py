import click
from harc.system import profile


class GitPasswordOption(click.Option):
    def get_default(self, ctx):
        properties = ctx.obj
        project_name = properties.get('name')
        password = None
        credentials = profile.credentials(project_name, properties)
        if credentials:
            git = credentials.get('git')
            if git:
                password = git.get('password')

        if not password:
            git = profile.credentials('git', properties)
            if git:
                password = git.get('password')

        self.default = password
        return super(GitPasswordOption, self).get_default(ctx)
