import subprocess

call_args = ['python', '-m', 'harc.harc_cli', 'http:status', '-e=dev', '-u=harc@oxyma.nl', '-p=*Thd4Dh!#', '-j=JOB$_']
subprocess.call(call_args)
