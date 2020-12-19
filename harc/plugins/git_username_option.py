import click

from harc.system import profile


class GitUsernameOption(click.Option):
    def get_default(self, ctx):
        properties = ctx.obj
        project_name = properties.get('name')
        username = None
        credentials = profile.credentials(project_name, properties)
        if credentials:
            git = credentials.get('git')
            if git:
                username = git.get('username')

        if not username:
            git = profile.credentials('git', properties)
            if git:
                username = git.get('username')

        self.default = username
        return super(GitUsernameOption, self).get_default(ctx)
