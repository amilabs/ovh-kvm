# Ovh-kvm

Ovh-KVM is a modified OVH WebKVM little python script that enables your server's emergency
console using OVH API by HTML5. Since OVH API use token autentification we are not able to connect through noVNC.

## Requirements

 - Python 3.2+
 - Html web browser

This script must works on OS X and any recent Linux distribution shipping
Python 3.2+.

## Setup

Install dependencies:
```
pip install -r requirements.txt
```

Register your application on the OVH API using
[this form](https://eu.api.ovh.com/createToken/) (EU) or
[this form](https://ca.api.ovh.com/createToken/) (CA), with the following
permissions:
```
GET  /dedicated/server
GET  /dedicated/server/*/features/ipmi*
POST /dedicated/server/*/features/ipmi*
GET  /dedicated/server/*/task/*
```

Then rename the `ovh.conf.default` file to `ovh.conf`, and edit it with the
application key, application secret, and consumer key provided by OVH.

## Usage

You can now launch the script:
```
./kvm.py [your server name]
```

Example:
```
./kvm.py nsXXXXXX.ip-XXX-XXX-XXX.eu
```

Link will be printed in terminal and web browser will be opened if available.



