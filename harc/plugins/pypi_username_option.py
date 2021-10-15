import click

from harc.system import profile


class PyPiUsernameOption(click.Option):
    def get_default(self, ctx):
        properties = ctx.obj
        project_name = properties.get('name')
        username = None
        credentials = profile.credentials(project_name, properties)
        if credentials:
            pypi = credentials.get('pypi')
            if pypi:
                username = pypi.get('username')

        if not username:
            pypi = profile.credentials('git', properties)
            if pypi:
                username = pypi.get('username')

        self.default = username
        return super(PyPiUsernameOption, self).get_default(ctx)
