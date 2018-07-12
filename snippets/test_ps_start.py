from harc.system.Ps import Ps
import os
# this snippet assumes that the code is in folder /tmp/d5c2f07484f148198406aae1d83baf8a/
tmp_folder = "/tmp/d5c2f07484f148198406aae1d83baf8a/"
daemon_name = "elsevierd"

# virtualenv = os.path.join(tmp_folder, 'env')
# response = Ps.start(virtualenv, daemon_name)

# #!/bin/bash
# source env/bin/activate
# paprika-hook
# deactivate

# read the content of the template shell script
f = open('daemon.sh')
data = f.read()
f.close()

# replace the daemon_name with the actual daemon name.
data = data.replace('${daemon_name}', daemon_name)
print data

# create the shell script
script = os.path.join(tmp_folder, daemon_name + '_service.sh')
f = open(script, 'w')
f.write(data)
f.close()


# read the content of the template service script



# script = os.path.join(tmp_folder, daemon_name + '.sh')
# f = open(script, 'w')
# f.write("#!/bin/bash")
# f.write