s = "1.0.1"
release, seperator, snapshot = s.rpartition("-")
print(f"{release=}, {seperator=}, {snapshot=}")

s = "1.0.1-dev0"
release, seperator, snapshot = s.rpartition("-")
print(f"{release=}, {seperator=}, {snapshot=}")


def release_split(s):
    if s:
        parts = s.split('-', maxsplit=2)
        if len(parts) == 1:
            return parts[0], None
        return parts[0], parts[1]
    return None, None

s = "1.0.1-dev0"
release, snapshot = release_split(s)
print(f"{release=}, {snapshot=}")

s = "1.0.1"
release, snapshot = release_split(s)
print(f"{release=}, {snapshot=}")

s = ""
release, snapshot = release_split(s)
print(f"{release=}, {snapshot=}")

s = None
release, snapshot = release_split(s)
print(f"{release=}, {snapshot=}")