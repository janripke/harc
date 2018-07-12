import subprocess

call_args = ['python', '-m', 'harc.harc_cli', 'http:services:start', '-e=dev', '-u=harc@oxyma.nl', '-p=*Thd4Dh!#']
subprocess.call(call_args)