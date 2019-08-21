import subprocess

call_args = ['python', '-m', 'harc.harc_cli', 'http:status', '-e=dev', '-u=harc@harc.nl', '-p=*', '-j=JOB$_']
subprocess.call(call_args)
