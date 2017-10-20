#!/usr/bin/python3
"""
Ideally command line API interaction

Example Usage:
geo 8.8.8.8 203.0.113.1
"""
from argparse import ArgumentParser
import re
import requests


# TODO: IPV6 Support
# TODO: Add an all command argument flag that will show as much as possible.


def geo():
    URL = "http://ip-api.com/json/"

    parser = ArgumentParser(description='Return Geo IP Data.')
    # add optional argument of ipv4 ip address
    parser.add_argument('IP', metavar="IP", type=str, help="An IPv4 Address", nargs='*')
    args = parser.parse_args()

    args = args.IP
    print(len(args))
    print(type(args))
    print(args)

    if len(args)== 0:
        print("""Run "geo -h" for help. """)

    for single_ip in args:
        # # debug
        # print(single_ip)
        if is_ip(single_ip):
            request = requests.get(URL + single_ip)
            if request.status_code == 200:
                data = request.json()
                if data['status'] == "success":
                    # print("__________")
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
            else:
                print("Bad Request. HTTP Status Code: {.status_code}".format(request))
        else:
            # Completely invalid ips. Like... a.b.c.d
            print("__________")
            print("| IP:         " + single_ip)
            print("| Status:     " + "Invalid")
    print("----------")


def is_ip(string):
    # TODO: improve this regex for IPv4 addresses. Easily google-able. or just rely on the website?
    # regex should be used to get IP that site can handle
    if re.match('(\d{1,3}.){3}\d{1,3}', string):
        return string

geo()
