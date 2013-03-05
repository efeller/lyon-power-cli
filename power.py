#!/usr/bin/env python
"""
Lyon power measurement CLI 

Maintainer: Eugen Feller <eugen.feller@inria.fr>
Version: 0.1

This is a command line interface (CLI) to the power measurements website in Lyon. 
It allows to obtain instant power values per server or group of servers. The CLI 
is based on the measures exported by the "GetWatts-json.php" file. 

Please see ./power.py for more information!
"""

import urllib2, base64
import argparse
import json
import time
import sys
import traceback

getwatts_no_auth_url = "http://wattmetre.lyon.grid5000.fr/GetWatts-json.php"
getwatts_auth_url = "https://helpdesk.grid5000.fr/supervision/lyon/wattmetre/GetWatts-json.php"


def send_http_request(url, username = "", password = ""):
    request = urllib2.Request(url)
    base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
    request.add_header("Authorization", "Basic %s" % base64string)
    request.add_header('Accept', 'application/json')   
    result = urllib2.urlopen(request)
    data = json.loads(result.read())
    result.close()
    return data 

def parse_user_input():
    parser = argparse.ArgumentParser(description="Lyon power measurement CLI v1.0 (c) Eugen Feller <eugen.feller@inria.fr>")
    subparsers = parser.add_subparsers(title='available commands',
                                       help='Additional help',
                                       dest="subparser_name")
    auth_parser = subparsers.add_parser('auth', help='Authenticated access')
    auth_parser.add_argument('--username', help="The Grid'5000 username", required=True)
    auth_parser.add_argument('--password', help="The Grid'5000 password", required=True)
    auth_parser.add_argument('--cluster', help="The cluster name", required=True)
    auth_parser.add_argument('--hosts', nargs='+', type=int, help="The list of hosts (e.g. 1 2 3 4)", required=True)
    auth_parser.add_argument('--granularity', type=int, default=1, help="The granularity (in seconds) between two measures (default: 1)")

    noauth_parser = subparsers.add_parser('noauth', help='Anonymous access')
    noauth_parser.add_argument('--cluster', help="The cluster name", required=True)
    noauth_parser.add_argument('--hosts', nargs='+', type=int, help="The list of hosts (e.g. 1 2 3 4)", required=True)
    noauth_parser.add_argument('--granularity', type=int, default=1, help="The granularity (in seconds) between two measures (default: 1)")
    
    args = parser.parse_args()
    return args

def compute_total_power(data, cluster, hosts):
    total_power = 0
    for host in hosts:
        total_power += data[cluster + "-" + str(host)]["watt"]

    return total_power

def get_measurement_time(data):
    return data[".last"]["timestamp"]

def start_polling(cluster, hosts, granularity, url, username="", password=""):
    while (1):
        try:
            data = send_http_request(url, username, password)
            measurement_time = get_measurement_time(data)
            total_power = compute_total_power(data, cluster, hosts)
            print measurement_time, total_power 
            time.sleep(granularity)
        except KeyboardInterrupt:
            return 0 
        except Exception, err:
            sys.stderr.write('Failed: %s\n' % str(err))
            return 1 
 
if __name__ == "__main__":
    args = parse_user_input() 
    if args.subparser_name == "noauth":
        start_polling(args.cluster, args.hosts, args.granularity, getwatts_no_auth_url)
    if args.subparser_name == "auth":
        start_polling(args.cluster, args.hosts, args.granularity, getwatts_auth_url, args.username, args.password) 
