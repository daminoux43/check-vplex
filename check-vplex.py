#!/usr/bin/env python3
# encoding: utf-8
""""
########################################
#
#  plugin nagios for check DELL EMC VPLEX
#
########################################

#import modules"""
import argparse
import sys
import os
import re
import json
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

""" entete """
__author__ = 'Damien ARNAUD'
__contact__ = 'github@daminoux.fr'
__license__ = 'GPLv3'
__version__ = 0.2
__date__ = '2019-12-30'
__updated__ = '2020-O1-04'

###########################################
#        VARIABLE
###########################################
DEBUG = False

module_arg = {
                'configuration': '--configuration',
                'back-end': '--back-end',
                'front-end': '--front-end',
                'cache': '--cache',
                'consistency-group': '--consistency-group',
                'wan': '--wan',
                'hardware': '--hardware',
                'cluster_witness': '--cluster_witness',
                'vpn': '--vpn',
                'io-aborts': '--io-aborts',
    }

###########################################
#    FONCTION
###########################################


def escape_ansi(line):
        ansi_escape = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -/]*[@-~]')
        return ansi_escape.sub('', str(line))


def get_argument():
    """ recuperation des arguments de la ligne de command"""

    try:
        # Setup argument parser
        epilog = __author__ + ' <' + __contact__ + '>\n'\
            ' license: ' + __license__ +  \
            '\nwebsite: http://daminoux.fr/check-vplex'

        version = '%(prog)s {version}'.format(version=__version__)
        desc_script = 'plugin\'s Nagios check for DELL EMC VPLEX'
        parser = argparse.ArgumentParser(description=desc_script,
                                         epilog=epilog)
        parser.add_argument('-H', '--hostname',
                            type=str,
                            help='hostname or IP address',
                            required=True)
        parser.add_argument('-u', '--username',
                            type=str,
                            help='username', dest='username',
                            required=True)
        parser.add_argument('-p', '--password',
                            type=str,
                            help='user password',
                            required=True)
        parser.add_argument('-m', '--module',
                            type=str,
                            choices=['configuration',
                                     'back-end',
                                     'front-end',
                                     'cache',
                                     'consistency-group',
                                     'wan',
                                     'hardware',
                                     'cluster_witness',
                                     'vpn',
                                     'io-aborts'],
                            help='Requested MODULE for getting status. \
                                    Possible options are: configuration  | \
                                     back-end | front-end | cache | \
                                     consistency-group | wan hardware |\
                                     cluster_witness | vpn io-aborts',
                                  dest='module', required=True)
        parser.add_argument('-v', '--version', action='version',
                            version=version)
        args = parser.parse_args()

    except KeyboardInterrupt:
        # handle keyboard interrupt #
        return 0
    global hostaddress, user, password, module, arg_cmd
    hostaddress = args.hostname
    user = args.username
    password = args.password
    module = args.module.lower()
    arg_cmd = module_arg[module]

###########################################
#    CLASS
###########################################


class Vplex():
    """ This class permit to connect of the vplex's API"""

    def __init__(self):
        self.user = user
        self.password = password
        self.cmd = arg_cmd

    def send_request(self):
        """ This method send a request and get the result in a array """
        global status_split
        """ prepare requet http"""
        payload = {'args': self.cmd}
        headers = {'Username': self.user, 'Password': self.password}
        url = 'https://' + hostaddress + '/vplex/health-check'

        r = requests.post(url, json=payload, headers=headers, verify=False)

        """ prepare return to analyse """
        j = json.loads(r.text)
        full_status = j['response']['custom-data']
        full_status = escape_ansi(full_status)
        status_split = full_status.split('\n')

        """ display the return in array  form"""
        if DEBUG:
            print(status_split)
        return status_split

    """   #########################  GET MODULE ##########################"""
    def get_configuration(self):

        """ ------------- CONFIGURATION -----------
         This method send and treat the data for module configuration
         status_split ( the return of request http ) is of the form :
         ['Configuration (CONF):',
         'Checking VPlexCli connectivity to directors........ OK',
          'Checking Directors Commission...................... OK',
          'Checking Directors Communication Status............ OK',
          'Checking Directors Operation Status................ OK',
          'Checking Inter-director management connectivity.... OK',
          'Checking ports status.............................. OK',
          'Checking Call Home Status.......................... Error',
          'Checking Connectivity.............................. OK',
          'Checking Meta Data Backup.......................... Warning',
          'Checking Meta Data Slot Usage...................... OK','',
          'Output to /var/log/VPlex/cli/health_check_full_scan.log', '', '']
        """

        self.send_request()

        """  OK   """
        if status_split[1].lower().endswith('ok') and\
           status_split[2].lower().endswith('ok') and\
           status_split[3].lower().endswith('ok') and\
           status_split[4].lower().endswith('ok') and\
           status_split[5].lower().endswith('ok') and\
           status_split[7].lower().endswith('ok') and\
           status_split[8].lower().endswith('ok') and\
           status_split[9].lower().endswith('ok') and\
           status_split[10].lower().endswith('ok'):

            print(status_split[1] + ' ' +
                  status_split[2] + ' ' +
                  status_split[3] + ' ' +
                  status_split[4] + ' ' +
                  status_split[5] + ' ' +
                  status_split[6] + ' ' +
                  status_split[7] + ' ' +
                  status_split[8] + ' ' +
                  status_split[9] + ' ' +
                  status_split[10])
            sys.exit(0)

        """  ERROR   """
        if status_split[1].lower().endswith('error') or \
           status_split[2].lower().endswith('error') or \
           status_split[3].lower().endswith('error') or \
           status_split[4].lower().endswith('error') or \
           status_split[5].lower().endswith('error') or \
           status_split[7].lower().endswith('error') or \
           status_split[8].lower().endswith('error') or \
           status_split[9].lower().endswith('error') or \
           status_split[10].lower().endswith('error')or \
           status_split[1].lower().endswith('degraded') or \
           status_split[2].lower().endswith('degraded') or \
           status_split[3].lower().endswith('degraded') or \
           status_split[4].lower().endswith('degraded') or \
           status_split[5].lower().endswith('degraded') or \
           status_split[7].lower().endswith('degraded') or \
           status_split[8].lower().endswith('degraded') or \
           status_split[9].lower().endswith('degraded') or \
           status_split[10].lower().endswith('degraded'):

            print(status_split[1] + ' ' +
                  status_split[2] + ' ' +
                  status_split[3] + ' ' +
                  status_split[4] + ' ' +
                  status_split[5] + ' ' +
                  status_split[6] + ' ' +
                  status_split[7] + ' ' +
                  status_split[8] + ' ' +
                  status_split[9] + ' ' +
                  status_split[10])
            sys.exit(2)

        """  WARNING   """
        if status_split[1].lower().endswith('warning') or \
           status_split[2].lower().endswith('warning') or \
           status_split[3].lower().endswith('warning') or \
           status_split[4].lower().endswith('warning') or \
           status_split[5].lower().endswith('warning') or \
           status_split[7].lower().endswith('warning') or \
           status_split[8].lower().endswith('warning') or \
           status_split[9].lower().endswith('warning') or \
           status_split[10].lower().endswith('warning'):

            print(status_split[1] + ' ' +
                  status_split[2] + ' ' +
                  status_split[3] + ' ' +
                  status_split[4] + ' ' +
                  status_split[5] + ' ' +
                  status_split[6] + ' ' +
                  status_split[7] + ' ' +
                  status_split[8] + ' ' +
                  status_split[9] + ' ' +
                  status_split[10])
            sys.exit(1)

        """  UNKNOWN   """
        print(status_split[1] + ' ' +
              status_split[2] + ' ' +
              status_split[3] + ' ' +
              status_split[4] + ' ' +
              status_split[5] + ' ' +
              status_split[6] + ' ' +
              status_split[7] + ' ' +
              status_split[8] + ' ' +
              status_split[9] + ' ' +
              status_split[10])
        sys.exit(3)

    def get_backend(self):
        """ ------------- BACK-END -----------
        This method send and treat the data for module back-end
        status_split ( the return of request http ) is of the form :
        ['Back End (BE):',
        'Checking Unreachable Storage Volumes....... OK',
        'Checking Degraded Storage Volumes.......... OK',
        'Checking Unhealthy Virtual Volumes......... OK',
        'Back end array status...................... OK',
        'Validating paths to back end arrays........ OK',
        'Validating LUN limit per IT-Nexus.......... OK',
        'Checking Unhealthy IT Nexuses.............. OK', '',
        'Output to /var/log/VPlex/cli/health_check_full_scan.log', '', '']
        """
        self.send_request()

        """  OK   """
        if status_split[1].lower().endswith('ok') and \
           status_split[2].lower().endswith('ok') and \
           status_split[3].lower().endswith('ok') and \
           status_split[4].lower().endswith('ok') and \
           status_split[5].lower().endswith('ok') and \
           status_split[7].lower().endswith('ok'):

            print(status_split[1] + ' ' +
                  status_split[2] + ' ' +
                  status_split[3] + ' ' +
                  status_split[4] + ' ' +
                  status_split[5] + ' ' +
                  status_split[6] + ' ' +
                  status_split[7])
            sys.exit(0)

        """  ERROR   """
        if status_split[1].lower().endswith('error') or \
           status_split[2].lower().endswith('error') or \
           status_split[3].lower().endswith('error') or \
           status_split[4].lower().endswith('error') or \
           status_split[5].lower().endswith('error') or \
           status_split[7].lower().endswith('error'):

            print(status_split[1] + ' ' +
                  status_split[2] + ' ' +
                  status_split[3] + ' ' +
                  status_split[4] + ' ' +
                  status_split[5] + ' ' +
                  status_split[6] + ' ' +
                  status_split[7])
            sys.exit(2)

        """  WARNING   """
        if status_split[1].lower().endswith('warning') or \
           status_split[2].lower().endswith('warning') or \
           status_split[3].lower().endswith('warning') or \
           status_split[4].lower().endswith('warning') or \
           status_split[5].lower().endswith('warning') or \
           status_split[7].lower().endswith('warning'):

            print(status_split[1] + ' ' +
                  status_split[2] + ' ' +
                  status_split[3] + ' ' +
                  status_split[4] + ' ' +
                  status_split[5] + ' ' +
                  status_split[6] + ' ' +
                  status_split[7])
            sys.exit(1)

        """  UNKNOWN   """
        print(status_split[1] + ' ' +
              status_split[2] + ' ' +
              status_split[3] + ' ' +
              status_split[4] + ' ' +
              status_split[5] + ' ' +
              status_split[6] + ' ' +
              status_split[7])
        sys.exit(3)

    def get_frontend(self):
        """ ------------- FRONT-END -----------
         This method send and treat the data for module front-end
         status_split ( the return of request http ) is of the form :
        ['Front End (FE):', 'Checking Storage Views..... OK',
        'Checking Front End HA...... OK',
        'Checking Front End Path.... OK', '',
        'Output to /var/log/VPlex/cli/health_check_full_scan.log', '', '']
        """
        self.send_request()

        """  OK   """
        if status_split[1].lower().endswith('ok') and \
           status_split[2].lower().endswith('ok'):

            print(status_split[1]+' '+status_split[2])
            sys.exit(0)

        """  ERROR   """
        if status_split[1].lower().endswith('error') or \
           status_split[2].lower().endswith('error'):

            print(status_split[1]+' '+status_split[2])
            sys.exit(2)

        """  WARNING   """
        if status_split[1].lower().endswith('warning') or \
           status_split[2].lower().endswith('warning'):

            print(status_split[1]+' '+status_split[2])
            sys.exit(1)

        """  UNKNOWN   """
        print(status_split[1]+' '+status_split[2])
        sys.exit(3)

    def get_cache(self):
        """ ------------- CACHE -----------
        This method send and treat the data for module cache
        status_split ( the return of request http ) is of the form :

        """

        self.send_request()

        """  OK   """
        if status_split[1].lower().endswith('ok'):
            print(status_split[1])
            sys.exit(0)

        """  WARNING   """
        if status_split[1].lower().endswith('warning'):
            print(status_split[1])
            sys.exit(1)

        """  ERROR   """
        if status_split[1].lower().endswith('error'):
            print(status_split[1])
            sys.exit(2)

        """  UNKNOWN   """
        print(status_split[1])
        sys.exit(3)

    def get_consistencygroup(self):
        """ ------------- CONSISTENCY - GROUP -----------
        This method send and treat the data for module consistency-group
        status_split ( the return of request http ) is of the form :
        ['Consistency Group Health:',
        'Consistency Group Health..... OK',
        'Consistency Group Setting.... OK', '',
        'Output to /var/log/VPlex/cli/health_check_full_scan.log', '', '']
        """
        self.send_request()

        """  OK   """
        if status_split[1].lower().endswith('ok') and \
           status_split[2].lower().endswith('ok'):

            print(status_split[1]+' '+status_split[2])
            sys.exit(0)

        """  ERROR   """
        if status_split[1].lower().endswith('error') or \
           status_split[2].lower().endswith('error'):

            print(status_split[1]+' '+status_split[2])
            sys.exit(2)

        """  WARNING   """
        if status_split[1].lower().endswith('warning') or \
           status_split[2].lower().endswith('warning'):

            print(status_split[1]+' '+status_split[2])
            sys.exit(1)

        """  UNKNOWN   """
        print(status_split[1]+' '+status_split[2])
        sys.exit(3)

    def get_wan(self):
        """ ------------- WAN -----------
        This method send and treat the data for module WAN
        status_split ( the return of request http ) is of the form :
            ['WAN Link:',
            'WAN Configuration.... OK','',
            'Output to /var/log/VPlex/cli/health_check_full_scan.log', '', '']
        """

        self.send_request()

        """  OK   """
        if status_split[1].lower().endswith('ok'):
            print(status_split[1])
            sys.exit(0)

        """  WARNING   """
        if status_split[1].lower().endswith('warning'):
            print(status_split[1])
            sys.exit(1)

        """  ERROR   """
        if status_split[1].lower().endswith('error'):
            print(status_split[1])
            sys.exit(2)

        """  UNKNOWN   """
        print(status_split[1])
        sys.exit(3)

    def get_hardware(self):
        """ ------------- HARDWARE -----------
        This method send and treat the data for module hardware
        status_split ( the return of request http ) is of the form :
        ['Director Health Status:',
        'Checking Director Hardware.... OK',
        'Checking SSD Hardware......... OK', '',
        'Output to /var/log/VPlex/cli/health_check_full_scan.log', '', '']
        """
        self.send_request()

        """  OK   """
        if status_split[1].lower().endswith('ok') and \
           status_split[2].lower().endswith('ok'):

            print(status_split[1]+' '+status_split[2])
            sys.exit(0)

        """  ERROR   """
        if status_split[1].lower().endswith('error') or \
           status_split[2].lower().endswith('error'):

            print(status_split[1]+' '+status_split[2])
            sys.exit(2)

        """  WARNING   """
        if status_split[1].lower().endswith('warning') or \
           status_split[2].lower().endswith('warning'):

            print(status_split[1]+' '+status_split[2])
            sys.exit(1)

        """  UNKNOWN   """
        print(status_split[1]+' '+status_split[2])
        sys.exit(3)

    def get_clusterwitness(self):
        """ ------------- CLUSTER WITNESS -----------
        This method send and treat the data for module cluster-witness
        status_split ( the return of request http ) is of the form :
        ['Cluster Witness:',
        'Checking Cluster Witness.... OK', '',
        'Output to /var/log/VPlex/cli/health_check_full_scan.log', '', '']
        """
        self.send_request()

        """  OK   """
        if status_split[1].lower().endswith('ok'):
            print(status_split[1])
            sys.exit(0)

        """  WARNING   """
        if status_split[1].lower().endswith('warning'):
            print(status_split[1])
            sys.exit(1)

        """  ERROR   """
        if status_split[1].lower().endswith('error'):
            print(status_split[1])
            sys.exit(2)

        """  UNKNOWN   """
        print(status_split[1])
        sys.exit(3)

    def get_vpn(self):
        """ ------------- VPN -----------
        This method send and treat the data for module VPN
        status_split ( the return of request http ) is of the form :
         ['VPN Check:',
         'VPN Status.... OK', '',
         'Output to /var/log/VPlex/cli/health_check_full_scan.log', '', '']

        """
        self.send_request()

        """  OK   """
        if status_split[1].lower().endswith('ok'):
            print(status_split[1])
            sys.exit(0)

        """  WARNING   """
        if status_split[1].lower().endswith('warning'):
            print(status_split[1])
            sys.exit(1)

        """  ERROR   """
        if status_split[1].lower().endswith('error'):
            print(status_split[1])
            sys.exit(2)

        """  UNKNOWN   """
        print(status_split[1])
        sys.exit(3)

    def get_ioaborts(self):
        """ ------------- IO ABORTS -----------
        This method send and treat the data for module io-aborts
        status_split ( the return of request http ) is of the form :
        ['None']
        """
        self.send_request()

        """  OK   """
        if status_split[0].lower().endswith('none'):
            print("None io-aborts")
            sys.exit(0)

        else:
            print(status_split[0])
            sys.exit(2)


def main(argv=None):
    '''main fonction'''

    """get and test arguments """
    get_argument()

    """display arguments if DEBUG enabled"""
    if DEBUG:

        print("hostname: "+hostaddress)
        print("user: "+user)
        print("password: "+password)
        print("module: "+module)
        print("args cmd: "+arg_cmd)

    myvplex = Vplex()

    """   configuration      """
    if module == 'configuration':
        myvplex.get_configuration()

    """   BACK-END      """
    if module == 'back-end':
        myvplex.get_backend()

    """   FRONT-END      """
    if module == 'front-end':
        myvplex.get_frontend()

    """   CACHE      """
    if module == 'front-end':
        myvplex.get_cache()

    """   CONSISTENCY GROUP     """
    if module == 'consistency-group':
        myvplex.get_consistencygroup()

    """   WAN      """
    if module == 'wan':
        myvplex.get_wan()

    """   HARDWARE      """
    if module == 'hardware':
        myvplex.get_hardware()

    """   CLUSTER WITNESS      """
    if module == 'cluster_witness':
        myvplex.get_clusterwitness()

    """   VPN      """
    if module == 'vpn':
        myvplex.get_vpn()

    """   IO ABORTS     """
    if module == 'io-aborts':
        myvplex.get_ioaborts()


if __name__ == '__main__':
    main()
    sys.exit(3)
