import subprocess

call_args = ['python', '-m', 'harc.harc_cli', 'git:deploy', '-v=1.0.0', '-n=paprika', '-e=dev']
subprocess.call(call_args)

