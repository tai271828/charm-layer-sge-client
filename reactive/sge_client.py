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
@when_not('sge-client.installed')
def install_sge_client():
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
        hookenv.log('master: {}'.format(master['hostname']))

        filename = '/usr/share/charm-sge-cluster/master_address'
        with open(filename, 'a') as fout:
            fout.write(master['hostname'] + "\n")

        sge_client.connect_sge_master(master['hostname'])

    sge_client.aggregate_mpi_hosts()

    clear_flag('endpoint.config-exchanger.new-exchanger')


@when('endpoint.config-exchanger.joined')
def publish_host_info():
    endpoint_client = endpoint_from_flag('endpoint.config-exchanger.joined')
    endpoint_client.publish_info(hookenv.unit_public_ip())

