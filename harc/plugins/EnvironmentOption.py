import click


class EnvironmentOption(click.Option):
    def get_default(self, ctx):
        properties = ctx.obj
        self.default = properties.get('default_environment')
        return super(EnvironmentOption, self).get_default(ctx)