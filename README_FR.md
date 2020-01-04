#check_vplex.py

Ce script python est un plugin nagios pour monitorer un vplex de DELL EMC. Il effectue les vérification en interrogeant l'API RESTfull du vplex. Ce plugin a été testé avec une version 6.1 de vplex et python 3.6.8.


#### usage:

check_vplex.py [-h] -H HOSTADDRESS -u USER -p PASSWORD -m { configuration, back-end, front-end, cache, consistency-group, wan, hardware, cluster_witness, vpn io-aborts}

####arguments
 * -h, --help
	Affiche ce message d'aide
 * -H HOSTNAME, --hostname HOSTNAME
	addresse ip ou fqdn du vplex à monitorer.
 * -u USERNAME, --username USERNAME
	utilisateur pour se connecter à l'API du vplex
 * -p PASSWORD, --password PASSWORD
	Mot de passe de l'utilisateur
 * -m, --module
 	module à vérifier parmi configuration ou back-end ou front-end ou cache ou consistency-group ou wan ou  hardware or cluster_witness or vpn io-aborts

#### module
Les modules verifient les status ci-desssous:

#####configuration:
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

##### back-end:
   - Checking Unreachable Storage Volumes
   - Checking Degraded Storage Volumes
   - Checking Unhealthy Virtual Volumes
   - Back end array status
   - Validating paths to back end arrays
   - Validating LUN limit per IT-Nexus
   - Checking Unhealthy IT Nexuses

#####front-end:
   - Checking Front End HA
   - Checking Front End Path

#####consistency-group:
   - Consistency Group Health
   - Consistency Group Setting

#####wan:
   - WAN Configuration

#####hardware:
   - Checking Director Hardware
   - Checking SSD Hardware

#####cluster_witness:
   - Checking Cluster Witness
#####vpn:
   - VPN Status

#####io-aborts:
   - Check if io aborts

### site web

<http://daminoux.fr/check-vplex>

###Dépendence de librairie:

    json
    requests
    argparse


### Création d'un utlisateur
Pour des raisons de sécurité, il est connseillé de ne pas utiliser le compte administrateur et de créer un compte sans aucun droit particulier.

© 2019 Damien ARNAUD published sous GPLv3 license