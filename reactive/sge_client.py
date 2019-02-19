import subprocess as sp
from charms.reactive import when, when_not, set_flag, clear_flag
from charms.reactive.relations import endpoint_from_flag
from charmhelpers.core import hookenv
from charmhelpers.core.hookenv import application_version_set, status_set
from charmhelpers.fetch import get_upstream_version
from charms.layer import sge_client


@when('apt.installed.gridengine-client')
@when('apt.installed.gridengine-exec')
@when('apt.installed.mpich')
@when('apt.installed.nfs-common')
@when('apt.installed.libarchive-dev')
@when_not('sge-client.installed')
def install_sge_client():
    hookenv.log('Begin to boostrap a client node.')
    sge_client.build_singularity()

    application_version_set(get_upstream_version('gridengine-client'))

    # Set the active status with the message
    status_set('active', 'SGE client is installed')

    set_flag('sge-client.installed')


@when('endpoint.config-exchanger.new-exchanger')
def update_master_config():
    cmd = ['mkdir', '-p', '/usr/share/charm-sge-cluster/']
    sp.check_call(cmd)
    flag = 'endpoint.config-exchanger.new-exchanger'
    master_config = endpoint_from_flag(flag)
    for master in master_config.exchangers():
        hookenv.log('master: {}'.format(master['unit_private_ip']))

        filename = '/usr/share/charm-sge-cluster/master_address'
        with open(filename, 'a') as fout:
            fout.write(master['unit_private_ip'] + "\n")

        sge_client.connect_sge_master(private_ip=master['unit_private_ip'])

    clear_flag('endpoint.config-exchanger.new-exchanger')


# still very buggy to have duplicate entries in the known_hosts
@when('endpoint.config-exchanger.new-mpi-host')
def update_mpi_cluster_info():
    # aggregate the mpi host info when the host info is published
    sge_client.aggregate_mpi_hosts()
    hookenv.log('Aggregated MPI hosts.')
    clear_flag('endpoint.config-exchanger.new-mpi-host')


@when('endpoint.config-exchanger.joined')
def publish_public_address():
    endpoint_client = endpoint_from_flag('endpoint.config-exchanger.joined')
    endpoint_client.publish_info_public_ip(hookenv.unit_public_ip())


@when('endpoint.config-exchanger.joined')
def publish_private_address():
    endpoint_client = endpoint_from_flag('endpoint.config-exchanger.joined')
    endpoint_client.publish_info_private_ip(hookenv.unit_private_ip())

