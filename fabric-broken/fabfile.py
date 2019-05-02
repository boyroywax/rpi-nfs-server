# Fabfile to:
#    - update the remote system(s) 
#    - download and install an application

# Import Fabric's API module
from fabric.api import *
from fabric.contrib.files import exists
import paramiko
import os
import re
import logging


logger = paramiko.util.logging.getLogger()
hdlr = logging.FileHandler('app.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.INFO)

@task
def test_func():
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        k = paramiko.RSAKey.from_private_key_file('id_rsa')
        ssh.connect('k3s-worker-01.local', username='pi', pkey = k)
    except Exception:
        logging.debug(Exception)
        logging.info('Error connecting to Host')


def connect():
    hosts = [
        # 'pi@k3s-master.local',
        # 'pi@k3s-worker-01.local',
        'k3s-worker-02.local',
        # pi@k3s-worker-03.local',
        'k3s-worker-04.local'
    ]
    for host in hosts:
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            k = paramiko.RSAKey.from_private_key_file('/Users/jdev/.ssh/id_rsa')
            ssh.connect(host, username='pi', pkey = k)
        except Exception:
            logging.debug(Exception)
            logging.info('Error connecting to Host')
    # env.use_ssh_config = True
    # env.ssh_config_path = '/Users/jdev/.ssh/config'
    # Set password for each host:port pair
    # for host in env.hosts:
    #     env.sudo_passwords[host] = 'abc1'


def update_upgrade():
    """
        Update the default OS installation's
        basic default tools.
                                            """
    run('sudo apt update')
    run('sudo apt -y upgrade')


def remove_install():
    """ remove the previous k3s install. """
    if exists('/usr/local/bin/k3s-agent-uninstall.sh'):
        run('sudo /usr/local/bin/k3s-agent-uninstall.sh')

    if exists('/usr/local/bin/k3s-uninstall.sh'):
        run('sudo /usr/local/bin/k3s-uninstall.sh')

    if exists('/usr/local/lib/k3s'):      
        run('sudo rm -r /usr/local/lib/k3s')

    if exists('/usr/local/lib/k3s'):      
        run('sudo rm -r /usr/local/bin/k3s')



def install_k3s():
    """ Download and install k3s. """
    run('curl -sfL https://get.k3s.io | INSTALL_K3S_VERSION="v0.4.0" K3S_URL="https://192.168.0.94:6443" K3S_TOKEN="K10bb2f23fe92c86b5fd55c37ce877498cec4f964651181808f3b1d34b7a4b5a75d::node:afbc85ffbd1f287a53093d62bbf7e699" sh -')


@task
def update_install():

    connect()
  
    update_upgrade()

    remove_install()
        # Installs
    install_k3s() 