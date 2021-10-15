import click


class PluginCommand(click.MultiCommand):

    def list_commands(self, ctx):
        commands = list()
        commands.append('git:release')
        commands.append('docker:build')
        commands.append('container:push')
        commands.append('container:deploy')
        commands.append('databricks:deploy')
        commands.append('databricks:upload')
        commands.append('databricks:run')
        return commands

    def get_command(self, ctx, cmd_name):
        if cmd_name == "git:release":
            from harc.plugins.git.git_release import GitRelease
            return GitRelease.execute
        if cmd_name == "pypi:deploy":
            from harc.plugins.pypi.pypi_deploy import PyPiDeploy
            return PyPiDeploy.execute
