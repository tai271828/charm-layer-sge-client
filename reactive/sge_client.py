from charms.reactive import when, when_not, set_flag, clear_flag
from charms.reactive.relations import endpoint_from_flag
from charmhelpers.core import hookenv
from charmhelpers.core.hookenv import application_version_set, status_set
from charmhelpers.fetch import get_upstream_version
import subprocess as sp

@when_not('sge-client.installed')
@when('apt.installed.gridengine-client')
def install_sge_layer():
    # Set the upstream version of hello for juju status.
    application_version_set(get_upstream_version('gridengine-client'))

    # Run hello and get the message
    #message = sp.check_output('hello', stderr=sp.STDOUT)

    # Set the active status with the message
    status_set('active', 'gridengine-client is installed' )

    # Signal that we know the version of hello
    #set_flag('hello.version.set')
    set_flag('sge-client.installed')

@when('endpoint.sge-cluster.new-master')
def update_mater_config():
    master_config = endpoint_from_flag('endpoint.sge-cluster.new-master')
    print("hookenv: {}".format(hookenv))
    for master in master_config.masters():
        hookenv.log('master: {}'.format(master['hostname']))
    clear_flag('endpoint.sge-cluster.new-master')

