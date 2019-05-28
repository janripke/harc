import click


@click.group()
@click.option('--debug/--no-debug', default=False)
def cli(debug):
    if debug:
        click.echo('debug is on')
# @click.option('-h', '--host', required=False, prompt=True, default='localhost')
# @click.option('-p', '--port', required=False, prompt=True, type=int, default=1433)
# @click.option('-d', '--database', required=True, prompt='Database name')
# @click.option('-s', '--schema', required=True, prompt='Schema name')
# @click.option('-U', '--username', required=True, prompt='Database username')
# @click.option('-P', '--password', required=True, prompt='Database password',
#               hide_input=True, confirmation_prompt=True)
# @click.option('-v', '--version', required=False,

@click.command()
@click.argument('command', nargs=1, type=click.UNPROCESSED)
@click.option('-r', '--revision',  default=False, is_flag=True)
def main(command, revision):
    print('command', command)
    if revision:
        print('revision', '1.0.0')


if __name__ == "__main__":
    main(args=None)
