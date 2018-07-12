import psutil

for proc in psutil.process_iter():
    if proc.name() == 'elsevierd':
        print proc
        proc.kill()

    # # check whether the process name matches
    # if proc.name() == PROCNAME:
    #     proc.kill()