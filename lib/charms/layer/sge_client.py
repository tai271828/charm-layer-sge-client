import subprocess as sp

__all__ = ['connect_sge_master']


def connect_sge_master(master_address=None):
    _connect_sge_master(master_address)
    _connect_nfs_server(master_address)
    setup_ssh_key_over_nodes(master_address)


def _connect_sge_master(address):
    cmd = 'echo ' + address + ' | ' + \
          'tee /var/lib/gridengine/default/common/act_qmaster'
    sp.run(cmd, shell=True)

    sp.run('service gridengine-exec restart', shell=True)


def _connect_nfs_server(address):
    dir_abs = '/home/ubuntu/mpi_nfs_mnt'
    cmd = 'mkdir ' + dir_abs
    sp.run(cmd, shell=True)

    cmd = 'mount -t nfs ' + address + ':' + dir_abs + ' ' + dir_abs
    sp.run(cmd, shell=True)


def setup_ssh_key_over_nodes(address):
    cmd = 'mkdir /home/ubuntu/.ssh/'
    sp.run(cmd, shell=True)

    cmd = 'chmod 700 /home/ubuntu/.ssh/'
    sp.run(cmd, shell=True)

    # TODO: silliy and security concern method. change me later by publish_info
    cmd = 'cp /home/ubuntu/mpi_nfs_mnt/keys/* /home/ubuntu/.ssh/'
    sp.run(cmd, shell=True)

    cmd = 'cat /home/ubuntu/.ssh/id_rsa.pub >> /home/ubuntu/.ssh/authorized_keys'
    sp.run(cmd, shell=True)

    cmd = 'chmod 600 /home/ubuntu/.ssh/authorized_keys'
    sp.run(cmd, shell=True)

    cmd = 'sh-keyscan -t rsa localhost >> /home/ubuntu/.ssh/known_hosts'
    sp.run(cmd, shell=True)

    cmd = 'ssh-keyscan -t rsa 127.0.0.1 >> /home/ubuntu/.ssh/known_hosts'
    sp.run(cmd, shell=True)

    cmd = 'ssh-keyscan -t rsa ' + address + ' >> /home/ubuntu/.ssh/known_hosts'
    sp.run(cmd, shell=True)

    cmd = 'chmod 600 /home/ubuntu/.ssh/known_hosts'
    sp.run(cmd, shell=True)

