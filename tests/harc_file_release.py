from harc.system.release.ReleaseFile import ReleaseFile
from harc.system.release.ReleaseNumber import ReleaseNumber
import os

here = os.path.abspath(os.path.dirname("../"))
print here
release = ReleaseFile.get_version(here, 'harc', 'python')
release = release.replace('-SNAPSHOT', '')
print str(release)
release = ReleaseNumber.increment_build(release)
print release