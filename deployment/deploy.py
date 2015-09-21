#!/usr/bin/python
'''
Deployment script

./deploy.py                Deploys to a local virtual machine using the files/Vagrantfile as settings for the VM. Needs port 8080 and 8443 to be free
./deploy.py production     Deploys to a production server listed in inventories production.ini
'''

import os
import argparse
import subprocess
import getpass

LOCALVM = 'local-vm'
PRODUCTION = 'production'
DEPLOYMENT_LOCATIONS = [LOCALVM]
PRODUCTION_INVENTORY = 'dev.inventory.ini'
ANSIBLE_DIR = os.path.join(os.getcwd(), 'playbooks')
PLAYBOOK = os.path.join(ANSIBLE_DIR, 'sites.yml')

# os.environ['VAGRANT_VAGRANTFILE'] = os.path.join(ANSIBLE_DIR, 'VagrantFile')
os.environ['ANSIBLE_CONFIG'] = os.path.join(ANSIBLE_DIR, 'ansible.cfg')

def main(args):
    location = args.location
    print 'location:', location
    if location == LOCALVM:
        # start VM (provisioning)
        output = subprocess.check_call(['vagrant', 'up'])
        # run the ansible playbook (configuration and deployment)
        inventory_filepath = os.path.join(ANSIBLE_DIR, 'inventories', 'hosts.ini')
        output = subprocess.call(['ansible-playbook', PLAYBOOK, '-i', inventory_filepath])
        print output
    elif location == PRODUCTION:
        user = args.user
        key = args.key
        inventory_filepath = os.path.join(ANSIBLE_DIR, 'inventories', PRODUCTION_INVENTORY)
        output = subprocess.check_call(['ansible-playbook', PLAYBOOK, '-i', inventory_filepath, '--user', user, '--ask-su-pass', '--private-key', key])
    else:
        raise Exception('Unrecognised location:', location)
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Depoloyment script')
    
    parser.add_argument('location', nargs='?', default=LOCALVM,
                        help='Where do you want to deploy to? Options are, {}'.format(DEPLOYMENT_LOCATIONS))
    parser.add_argument('--user', default=getpass.getuser())
    parser.add_argument('--key', default='{}/.ssh/id_rsa'.format(os.environ['HOME']))
    
    args = parser.parse_args()

    main(args)

