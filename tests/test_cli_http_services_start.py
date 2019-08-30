import subprocess

call_args = ['python', '-m', 'harc.harc_cli', 'http:services:start', '-e=dev', '-u=harc@harc.nl', '-p=*']
subprocess.call(call_args)