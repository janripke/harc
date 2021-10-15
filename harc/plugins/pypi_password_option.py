import click
from harc.system import profile


class PyPiPasswordOption(click.Option):
    def get_default(self, ctx):
        properties = ctx.obj
        project_name = properties.get('name')
        password = None
        credentials = profile.credentials(project_name, properties)
        if credentials:
            pypi = credentials.get('pypi')
            if pypi:
                password = pypi.get('password')

        if not password:
            pypi = profile.credentials('pypi', properties)
            if pypi:
                password = pypi.get('password')

        self.default = password
        return super(PyPiPasswordOption, self).get_default(ctx)
