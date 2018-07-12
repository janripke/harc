import subprocess

call_args = ['python', '-m', 'harc.harc_cli', 'git:branches', '-u=jan.ripke', '-p=*Drapje01*']
subprocess.call(call_args)