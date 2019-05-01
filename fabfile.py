# Fabfile to:
#    - update the remote system(s) 
#    - download and install an application

# Import Fabric's API module
from fabric.api import *
from fabric.contrib.files import exists


env.hosts = [
    # 'k3s-master.local',
    'k3s-worker-01.local'
    # 'k3s-worker-02.local',
    # 'k3s-worker-03.local',
    # 'k3s-worker-04.local'
]
# Set the username
env.user = "pi"
env.password = 'abc1'
env.sudo_password = 'abc1'

# Set the password [NOT RECOMMENDED]
# env.password = "passwd"



def update_upgrade():
    """
        Update the default OS installation's
        basic default tools.
                                            """
    run("sudo apt update")
    run("sudo apt -y upgrade")



def remove_install():
    """ remove the previous k3s install. """
    if exists('/usr/local/bin/k3s-agent-uninstall.sh'):
        run("sudo /usr/local/bin/k3s-agent-uninstall.sh")

    if exists('/usr/local/bin/k3s-uninstall.sh'):
        run("sudo /usr/local/bin/k3s-uninstall.sh")

    if exists('/usr/local/lib/k3s'):      
        run("sudo rm -r /usr/local/lib/k3s")

    if exists('/usr/local/lib/k3s'):      
        run("sudo rm -r /usr/local/bin/k3s")



def install_memcached():
    """ Download and install k3s. """
    run("curl -sfL https://get.k3s.io | INSTALL_K3S_VERSION='v0.4.0' K3S_URL=https://192.168.0.94:6443 K3S_TOKEN='K10bb2f23fe92c86b5fd55c37ce877498cec4f964651181808f3b1d34b7a4b5a75d::node:afbc85ffbd1f287a53093d62bbf7e699' sh -")



def update_install():

    # Update
    update_upgrade()

    remove_install()
    # Install
    install_memcached()