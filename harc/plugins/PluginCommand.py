import click
from harc.plugins.git.GitRelease import GitRelease
from harc.plugins.git.GitBranches import GitBranches
from harc.plugins.az.AzContainerPush import AzContainerPush
from harc.plugins.git.GitTags import GitTags
from harc.plugins.docker.DockerBuild import DockerBuild


class PluginCommand(click.MultiCommand):

    def list_commands(self, ctx):
        print("list_commands")
        commands = list()
        commands.append('git:branches')
        commands.append('git:tags')
        commands.append('git:release')
        commands.append('docker:build')
        # commands.append('az:container:push')
        return commands

    def get_command(self, ctx, cmd_name):

        if cmd_name == "git:branches":
            return GitBranches.execute
        if cmd_name == "git:tags":
            return GitTags.execute
        if cmd_name == "git:release":
            return GitRelease.execute
        if cmd_name == "docker:build":
            return DockerBuild.execute
        # if cmd_name == "az:container:push":
        #     return AzContainerPush.execute
