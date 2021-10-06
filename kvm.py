#!/usr/bin/env python3

import sys
#echo
def print_error(message, exit_code=1):
    print(message, file=sys.stderr)
    exit(exit_code)

try:
    import ovh
except ImportError:
    print_error('Missing "ovh" module. Please run the following command:\n'
                '\tpip -r requirements.txt')

def exit_handler(signal, frame):
    proc.terminate()
    print('Goodbye!')
    exit(0)

def get_console_conf(api_client, server):
    return api_client.get('/dedicated/server/{server_name}/features/ipmi/access'
            ''.format(server_name=server), **{'type': ACCESS_TYPE})

import os
import time
import json
import signal
import webbrowser
import urllib.request
import xml.etree.ElementTree as ET
from ovh.exceptions import ResourceNotFoundError

ACCESS_TYPE='kvmipHtml5URL'

server = sys.argv[1].lower() if len(sys.argv) > 1 else None
if not server:
    print_error('Missing server name.')

script_path = os.path.dirname(__file__)

# Init OVH API client.
client = ovh.Client()

# Retrieve account's servers list.
servers = client.get('/dedicated/server')
if not server in servers:
    print_error('Invalid server "{server_name}". Possible values are: '
                '{servers_list}.'.format( \
                server_name=server, servers_list=', '.join(servers)))

# Checking IPMI console availability.
ipmi = client.get('/dedicated/server/{server_name}/features/ipmi'
                  ''.format(server_name=server))

if not ipmi['activated'] == True:
    print_error('IPMI feature is not avalable on this server.')

# Retrieve public IPv4 address using httpbin.org.
allowed_ip = json.loads(urllib.request.urlopen('https://httpbin.org/ip').read().decode('utf-8'))['origin']
print('You public IP address is: {ip_address}'.format(ip_address=allowed_ip))

# Activating IPMI console access.
try:
    console = get_console_conf(client, server)
except ResourceNotFoundError:
    print('Activating server console...')
    task = client.post('/dedicated/server/{server_name}/features/ipmi/access'
            ''.format(server_name=server), \
            **{'ipToAllow': allowed_ip, 'ttl': 15, 'type': ACCESS_TYPE})

    while True:
        result = client.get('/dedicated/server/{server_name}/task/{task_id}'
                ''.format(server_name=server, task_id=task['taskId']))

        if result['status'] == 'error':
            print_error('Error during IPMI console activation: "{error_msg}".'
                    ''.format(error_msg=result['comment']))

        elif result['status'] == 'done':
            print('Console successfully activated!')
            break

        else:
            time.sleep(2)
    
    console = get_console_conf(client, server)

print('Console access expires at: {expire_date}'.format( \
        expire_date=console['expiration']))
        
kvm_url=console['value']
# Retrieve KVM login informations.
print('Retrieving KVM login informations...')
print(kvm_url)

webbrowser.open(kvm_url)

print('')
print('KVM HTML5 started.')
print('')
signal.signal(signal.SIGINT, exit_handler)
signal.pause()
