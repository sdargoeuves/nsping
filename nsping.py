"""
Welcome to NSPING.py
"""

import os
import sys
import platform     # For getting the operating system name
import subprocess   # For executing a shell command
import socket
import ipaddress
#import csv          # other way to export to csv
import argparse
import pandas as pd # easier way to export to csv


def nsping():
    """
    Main function for nsping
    """
    #Check that we have input_file as argument, using argparse
    parser = argparse.ArgumentParser(description=
            "NSPING needs a source file as an argument")
    parser.add_argument("input_file", help="Source File",type=str)
    args = parser.parse_args()
    input_file = args.input_file

    #define variables
    src_list = []
    result = []
    key_names = ["ID", "Source", "IP", "Hostname", "Ping"]
    
    #Confirm the file exists, and add the values in src_list
    if os.path.isfile(input_file):
        with open(input_file, 'r') as file:
            input_read = file.read()
        for line in input_read.split("\n"):
            if line != "":
                src_list.append(line)
    else:
        err_msg = f'##ERR## Input file \'{input_file}\' does not exist'
        sys.exit(err_msg)
    
    #loop through each entry
    id_ref = 0
    for src_entry in src_list:
        id_ref += 1
        output_nslookup = nslookup(src_entry)
        ip = output_nslookup[0]
        hostname = output_nslookup[1]

        if ip != "NSLOOKUP_FAILED":
            result_ping = ping(ip)
        else:
            result_ping = "NOT_ATTEMPTED"
        result.append(dict(zip(key_names, [
            id_ref,
            src_entry,
            ip,
            hostname,
            result_ping,])))
    
    #using pandas to export to CSV
    df = pd.DataFrame(result)
    date = pd.Timestamp('today').strftime("%Y%m%d") + "-" + pd.Timestamp('now').strftime("%H%M")
    output_file = "".join(["output-", os.path.splitext(input_file)[0], "-", date, ".csv"])
    df.to_csv(output_file, sep=";", index=False)   
    
    #other way of creating CSV export
    #keys = result[0].keys()
    #print(keys)
    #with open(str("output-old-"+input_file), "w", newline="")  as output_file:
    #    dict_writer = csv.DictWriter(output_file, keys)
    #    dict_writer.writeheader()
    #    dict_writer.writerows(result)

def ping(host):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """
    # Option for the number of packets as a function of
    param = '-n' if platform.system().lower()=='windows' else '-c'
    # Building the command. Ex: "ping -c 2 -w 2 google.com"
    command = ['ping', param, '1', "-w", "2", host]

    return subprocess.call(command, stdout=subprocess.DEVNULL) == 0


def nslookup(src_entry):
    """
    socket.gethostbyaddr(ip) returns:
    - Host Name <--- this is what we want
    - Alias list for the IP address if any
    - IP address of the host
    """
    try:
        # the src_entry is an IP address
        ip = str(ipaddress.ip_address(src_entry))
        try:
            hostname = socket.gethostbyaddr(src_entry)[0]
        except socket.herror:
            hostname = "NSLOOKUP_FAILED"
        #print("src_entry: %s | hostname: %s | ip: %s" % (src_entry, hostname, ip))

    except ValueError:
        #the entry is not an IP address
        hostname = src_entry
        try:
            ip = socket.gethostbyname(src_entry)
        except socket.gaierror:
            ip = "NSLOOKUP_FAILED"
        #print("src_entry: %s | hostname: %s | ip: %s" % (src_entry, hostname, ip))

    return [ip, hostname]

if __name__ == "__main__":
    nsping()
