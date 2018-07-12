import subprocess

call_args = ['python', '-m', 'harc.harc_cli', 'http:git:deploy:all', '-v=1.0.0', '-u=harc@oxyma.nl', '-p=*Thd4Dh!#']
subprocess.call(call_args)