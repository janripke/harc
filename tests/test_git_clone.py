from harc.system.System import System
from harc.system.Git import Git

username = 'JanOxyma-at-862682791897'
password = '******'

repository = "https://'{0}':'{1}'@git-codecommit.eu-west-1.amazonaws.com/v1/repos/poc-elsevier-api"
repository = repository.format(username, password)

project_name = 'poc-elsevier-api'

# create an empty folder in tmp
tmp_folder = System.recreate_tmp(project_name)


print(repository)
print(tmp_folder)
# clone the repository to the tmp_folder
result = Git.clone(repository, tmp_folder)

print(result)