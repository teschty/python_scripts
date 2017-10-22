#!/usr/bin/env python3
"""
Ideally command line API interaction
Do not over use this.


Example Usage:
geo 8.8.8.8 8.8.4.4
geo -f ip.txt
"""

from argparse import ArgumentParser
import re
import requests

# TODO: Add an all command argument flag that will show as much as possible.

def geo():
    URL = "http://ip-api.com/json/"

    parser = ArgumentParser(description="Return Geo IP Data.")
    # add optional argument of ipv4 ip address
    parser.add_argument("IP", metavar = "IP", type = str, help = "IPv4 Addresses separated by a space", nargs = "*")
    parser.add_argument("-f", "--file", help = ".txt file with IPv4 Addresses separated by newlines")

    # get arguments. have args become the IP arguments
    args = parser.parse_args().IP

    # get ip file argument
    file_args = parser.parse_args().file

    # no args. get user info.
    if not args and not file_args:
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

    # has file args
    elif file_args:
        with open(file_args) as file:
            ips = re.findall("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", file.read())
            ips = [ip for ip in ips if valid_ip(ip)]

            for single_ip in ips:
                request = requests.get(URL + single_ip)
                if request.status_code == 200:
                    data = request.json()
                    printer(data)

def printer(data):
    if data["status"] == "success":
        print("----------")
        if data["country"] != "":
            print("| IP:         {0[query]}\n| Country:    {0[country]} ({0[countryCode]})".format(data))
        if data["region"] != "":
            print("| Region:     {0[regionName]} ({0[region]})".format(data))
        if data["zip"] != "":
            print("| ZIP:        {0[zip]}".format(data))
        if data["isp"] != "":
            print("| ISP:        {0[isp]}".format(data))
    elif data["status"] == "fail":
        print("__________")
        print("| IP:         {0[query]}".format(data))
        print("| Status:     {0[status]}".format(data))
        print("| Message:    {0[message]}".format(data))


def valid_ip(address):
    try:
        host_bytes = address.split('.')
        valid = [int(b) for b in host_bytes]
        valid = [b for b in valid if b >= 0 and b<=255]
        return len(host_bytes) == 4 and len(valid) == 4
    except:
        return False

geo()
