import subprocess

call_args = ['python', '-m', 'harc.harc_rest_server', '-d=1', '-p=5000']
subprocess.call(call_args)