import subprocess as sp
from charms.reactive import when, when_not, set_flag, clear_flag
from charms.reactive.relations import endpoint_from_flag
from charmhelpers.core import hookenv
from charmhelpers.core.hookenv import application_version_set, status_set
from charmhelpers.fetch import get_upstream_version

@when_not('sge-client.installed')
@when('apt.installed.gridengine-client')
def install_sge_layer():
    application_version_set(get_upstream_version('gridengine-client'))

    # Set the active status with the message
    status_set('active', 'SGE client is installed' )

    set_flag('sge-client.installed')

@when('endpoint.master-config-receiver.new-master')
def update_mater_config():
    master_config = endpoint_from_flag('endpoint.master-config-receiver.new-master')
    print("hookenv: {}".format(hookenv))
    for master in master_config.masters():
        hookenv.log('master: {}'.format(master['hostname']))

    cmd = ['mkdir', '-p', '/usr/share/charm-sge-cluster/']
    sp.check_call(cmd)
    filename = '/usr/share/charm-sge-cluster/master_address'
    with open(filename, 'w') as fout:
        fout.write(master['hostname'])

    clear_flag('endpoint.master-config-receiver.new-master')

