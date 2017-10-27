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

# TODO: handle the api limit or find another api that has more uses per minute.

def geo():
    """main program"""

    url = "http://freegeoip.net/json/"
    # empty dict. Save data as a dict with a set of IPs. ex: {country: {IP, IP, IP}}
    location_dict = {}

    """
    This will likely be moved to a notes repository.
    NOTE: Dictionary manipulation
    add new country with empty list as value. (list will allow duplicates.)
    location_data.update({country:[]})
    add new country with empty list as value. (set will not have duplicates.)
    location_data.update({country:set()})

    Check if something in dict:
    "a" in location_data (returns T or F)
    country in data

    Add stuff to set:
    location_data['a'].add("1")
    location_data[country].add(single_ip)
    """

    parser = ArgumentParser(description="Return Geo IP Data.")
    # add optional argument of ipv4 ip address
    parser.add_argument("IP", metavar="IP", type=str,
                        help="IPv4 Addresses separated by a space", nargs="*")
    parser.add_argument(
        "-f", "--file", help=".txt file with IPv4 Addresses separated by newlines")

    # get arguments. have args become the IP arguments
    args = parser.parse_args().IP

    # get ip file argument
    file_args = parser.parse_args().file

    # no args. get user info
    if not args and not file_args:
        print("NOTE: Run geo with -h for help")
        request = requests.get(url)
        if request.status_code == 200:
            data = request.json()
            printer(data)

    # has args
    elif args:
        for single_ip in args:
            if valid_ip(single_ip):
                request = requests.get(url + single_ip)
                if request.status_code == 200:
                    data = request.json()
                    printer(data)

    # has file args
    elif file_args:
        with open(file_args) as file:
            ips = re.findall(
                r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", file.read())
            ips = [ip for ip in ips if valid_ip(ip)]
            
            # Enforce Unique! if unique desired. Add flag later? Assume unique by default? Add flag for not uniqueness? Find whomst'd've is most active ip in list?
            # if unique ips desired:
            ips = set(ips)
            
        for single_ip in ips:
            request = requests.get(url + single_ip)
            if request.status_code == 200:
                data = request.json()
                printer_and_collector(data, location_dict)


def printer_and_collector(data, location_dict):
    """Displays information from json pulled from site"""
    print("----------")
    if data["country_name"] != "":
        print(
            "| IP:         {0[ip]}\n"
            "| Country:    {0[country_name]} ({0[country_code]})".format(data))
        
        # add country and begin set for IPs if the country hasn't shown up yet.
        if data["country_name"] not in location_dict:
            location_dict.update({data["country_name"]:set()})
        
        # add ip to set that is the value to the country key in the dict of countries. 
        location_dict[data["country_name"]].add(data["ip"])

    if data["region_code"] != "":
        print("| Region:     {0[region_name]} ({0[region_code]})".format(data))
    if data["zip_code"] != "":
        print("| ZIP:        {0[zip_code]}".format(data))


def printer(data):
    """Displays information from json pulled from site"""
    print("----------")
    if data["country_name"] != "":
        print(
            "| IP:         {0[ip]}\n"
            "| Country:    {0[country_name]} ({0[country_code]})".format(data))
    if data["region_code"] != "":
        print("| Region:     {0[region_name]} ({0[region_code]})".format(data))
    if data["zip_code"] != "":
        print("| ZIP:        {0[zip_code]}".format(data))


def valid_ip(address):
    """Check for IP validity with regex"""
    try:
        host_bytes = address.split('.')
        valid = [int(b) for b in host_bytes]
        valid = [b for b in valid if b >= 0 and b <= 255]
        return len(host_bytes) == 4 and len(valid) == 4
    except ValueError:
        return False


geo()
