import shutil
import subprocess as sp

__all__ = ['connect_sge_master']


AUTH_KEYS_PATH = '/home/ubuntu/.ssh/authorized_keys'
KNOWN_HOSTS_PATH = '/home/ubuntu/.ssh/known_hosts'
CLIENT_ADDRESS_PATH = '/home/ubuntu/mpi_host_list'


def connect_sge_master(private_ip, public_ip=None):
    if not public_ip:
        public_ip = private_ip
    _connect_sge_master(public_ip)
    _connect_nfs_server(private_ip)
    #_setup_ssh_server_for_master(master_address)


def build_singularity():
    dir_bin = '/usr/local/sbin/'
    shutil.copy2('bin/build-singularity.sh', dir_bin)
    cmd = '/usr/local/sbin/build-singularity.sh'
    sp.run(cmd)


def _connect_sge_master(address):
    cmd = 'echo ' + address + ' | ' + \
          'tee /var/lib/gridengine/default/common/act_qmaster'
    sp.run(cmd, shell=True)

    sp.run('service gridengine-exec restart', shell=True)


def _connect_nfs_server(address, dir_abs='/home/ubuntu'):
    cmd = 'mkdir ' + dir_abs
    sp.run(cmd, shell=True)

    cmd = 'mount -t nfs ' + address + ':' + dir_abs + ' ' + dir_abs
    sp.run(cmd, shell=True)


# TODO: this seems not to use anymore
def _setup_ssh_server_for_master(address):
    cmd = 'mkdir /home/ubuntu/.ssh/'
    sp.run(cmd, shell=True)

    # TODO: silliy and security concern method. change me later by publish_info
    cmd = 'cp /home/ubuntu/mpi_nfs_mnt/keys/* /home/ubuntu/.ssh/'
    sp.run(cmd, shell=True)

    cmd = 'cat /home/ubuntu/.ssh/id_rsa.pub >> ' + AUTH_KEYS_PATH
    sp.run(cmd, shell=True)

    #cmd = 'chmod 600 ' + AUTH_KEYS_PATH
    #sp.run(cmd, shell=True)

    cmd = 'sh-keyscan -t rsa localhost >> ' + KNOWN_HOSTS_PATH
    sp.run(cmd, shell=True)

    cmd = 'ssh-keyscan -t rsa 127.0.0.1 >> ' + KNOWN_HOSTS_PATH
    sp.run(cmd, shell=True)

    cmd = 'ssh-keyscan -t rsa ' + address + ' >> ' + KNOWN_HOSTS_PATH
    sp.run(cmd, shell=True)

    #cmd = 'chmod 600 ' + KNOWN_HOSTS_PATH
    #sp.run(cmd, shell=True)

    cmd = 'chown ubuntu -R /home/ubuntu/.ssh/'
    sp.run(cmd, shell=True)


def aggregate_mpi_hosts():
    # aggregate hosts to compose of a MPI cluster
    _scan_all_mpi_host_keys()
    # we just ask for the client nodes to be the MPI computing hosts
    address = CLIENT_ADDRESS_PATH
    # TODO: could be done for only once. no need to create this file each time
    with open('/etc/profile.d/mpi-host-file.sh', 'wt') as fout:
        fout.write('export MPI_HOSTS=' + address + "\n")


def _scan_all_mpi_host_keys():
    # TODO: just a prototype, should think about how to remove the duplicates
    with open(CLIENT_ADDRESS_PATH, 'rt') as fin:
        lines = fin.readlines()
        for line in lines:
            # should be an IP address so there are 4 digits at least (IPv4)
            ls = line.strip()
            if len(ls) > 4:
                cmd = 'ssh-keyscan -t rsa ' + ls + ' >> ' + KNOWN_HOSTS_PATH
                sp.run(cmd, shell=True)

