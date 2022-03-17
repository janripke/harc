def increment_build(release):
    d = release.split(".")
    d[2] = str(int(d[2]) + 1)
    return '.'.join(d)


def split(s):
    if s:
        parts = s.split('-', maxsplit=2)
        if len(parts) == 1:
            return parts[0], None
        return parts[0], parts[1]
    return None, None
