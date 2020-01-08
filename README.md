# check_vplex.py

This is a Nagios monitoring script for DELL EMC vplex. It calls the vplex RESTfull API and check if every moduls are OK. This plugin have been tested with a version 6.1 of vplex and python 3.6.8.


## usage:

check_vplex.py [-h] -H HOSTADDRESS -u USER -p PASSWORD -m { configuration, back-end, front-end, cache, consistency-group, wan, hardware, cluster_witness, vpn io-aborts}

##  arguments
 * -h, --help
	show this help message and exit
 * -H HOSTNAME, --hostname HOSTNAME
	hostname or IP address
 * -u USERNAME, --username USERNAME
	username
 * -p PASSWORD, --password PASSWORD
	user password
 * -m, --module
 	module checking  among   configuration or back-end or front-end or cache or consistency-group or wan or  hardware or cluster_witness or vpn io-aborts

## module
This module checking :

### configuration:
   - Checking VPlexCli connectivity to directors
   - Checking Directors Commission
   - Checking Directors Communication Status
   - Checking Directors Operation Status
   - Checking Inter-director management connectivity
   - Checking ports status
   - Checking Call Home Status
   - Checking Connectivity
   - Checking Meta Data Backup
   - Checking Meta Data Slot Usage

### back-end:
   - Checking Unreachable Storage Volumes
   - Checking Degraded Storage Volumes
   - Checking Unhealthy Virtual Volumes
   - Back end array status
   - Validating paths to back end arrays
   - Validating LUN limit per IT-Nexus
   - Checking Unhealthy IT Nexuses

### front-end:
   - Checking Front End HA
   - Checking Front End Path

### consistency-group:
   - Consistency Group Health
   - Consistency Group Setting

### wan:
   - WAN Configuration

### hardware:
   - Checking Director Hardware
   - Checking SSD Hardware

### cluster_witness:
   - Checking Cluster Witness

### vpn:
   - VPN Status

### io-aborts:
   - Check if io aborts

## web site

<http://daminoux.fr/check-vplex>

## requirements:

    json
    requests
    argparse


## Creating a user
For reason of security, we recommend to not use administrator account and create a dedied user for monitoring.

For create a user daminoux on the vplex we must :

    - connect on the vplex in ssh with user admin
    - launch vplexcli with the command vplexcli
    - type the command: add user daminoux
    - type the password
    - type again the password
    - logout end reconnect with the new user
    - and retype a new password

And now you you can use the script check_vplex.py with the new user.


© 2020 Damien ARNAUD published under GPLv3 license