import subprocess as sp

__all__ = ['connect_sge_master']


def connect_sge_master(master_address=None):
    _connect_sge_master(master_address)
    _connect_nfs_server(master_address)


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

