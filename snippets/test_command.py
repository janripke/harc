# Test command stdout and stderr redirection and polling

from harc.shell.Command import Command
from harc.exceptions.CommandException import CommandException

print("> RUN SCRIPT test_command.sh\n")

try:
    output = Command.execute("./test_command.sh")
except CommandException as e:
    print("\n> EXCEPTION CAUGHT: {}".format(e))
    print("> RETURNCODE: {}".format(e.get_retcode()))
    print("> OUTPUT:\n")
    print(Command.stringify(e.get_output()))
else:
    print("> DONE, OUTPUT:")
    print(Command.stringify(output))