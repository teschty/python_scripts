#!/usr/bin/python3
"""
Ideally command line API interaction
Do not over user this.



Example Usage:
geo 8.8.8.8 8.8.4.4
"""
from argparse import ArgumentParser
import re
import requests

# TODO: Add an all command argument flag that will show as much as possible.

def geo():
    URL = "http://ip-api.com/json/"

    parser = ArgumentParser(description='Return Geo IP Data.')
    # add optional argument of ipv4 ip address
    parser.add_argument('IP', metavar="IP", type=str, help="IPv4 Addresses separated by a space", nargs='*')

    # get arguments. have args become the IP arguments
    args = parser.parse_args().IP

    # no args. get user info.
    if not args:
        print("NOTE: Run geo with -h for help")
        request = requests.get(URL)
        if request.status_code == 200:
            data = request.json()
            printer(data)

    # has args
    elif args:
        for single_ip in args:
            request = requests.get(URL + single_ip)
            if request.status_code == 200:
                data = request.json()
                printer(data)

def printer(data):
    if data['status'] == "success":
        print("----------")
        if data['country'] != '':
            print("| IP:         {0[query]}\n| Country:    {0[country]} ({0[countryCode]})".format(data))
        if data['region'] != '':
            print("| Region:     {0[regionName]} ({0[region]})".format(data))
        if data['zip'] != '':
            print("| ZIP:        {0[zip]}".format(data))
        if data['isp'] != '':
            print("| ISP:        {0[isp]}".format(data))
    elif data['status'] == "fail":
        print("__________")
        print("| IP:         {0[query]}".format(data))
        print("| Status:     {0[status]}".format(data))
        print("| Message:    {0[message]}".format(data))

geo()
