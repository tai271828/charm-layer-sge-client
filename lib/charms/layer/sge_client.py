import os
import shutil
import subprocess as sp

__all__ = ['connect_sge_master', 'get_installed_message']

def connect_sge_master(master_address=None):
    with open('/etc/profile.d/sge-master', 'w') as fout:
        fout.write("export MASTER_HOSTNAME={}\n".format(master_address))

    cmd = 'echo ' + master_address + ' | ' + \
          'tee /var/lib/gridengine/default/common/act_qmaster'
    sp.run(cmd, shell=True)

    sp.run('service gridengine-exec restart', shell=True)

