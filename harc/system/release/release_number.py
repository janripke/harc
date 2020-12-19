def increment_build(release):
    d = release.split(".")
    d[2] = str(int(d[2]) + 1)
    return '.'.join(d)
