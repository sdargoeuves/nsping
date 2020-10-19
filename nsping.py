import os
import ipaddress
import sys
import socket
import csv          # "old" way to export to csv
import pandas as pd # easier way to export to csv
import platform     # For getting the operating system name
import subprocess   # For executing a shell command


def nsping():
    #Check that we have input_file as argument
    if len(sys.argv) >= 2:
        input_file = sys.argv[1]
    else:
        err_msg = "##ERR## You need to specify the source file as an argument:\npython3 nsping.py input_file" 
        sys.exit(err_msg)
    
    src_list = []
    result = []
    key_names = ["ID", "Source", "IP", "Hostname", "Ping"]
    
    #Confirm the file exists, and add the values in src_list
    if os.path.isfile(input_file) == True:
        with open(input_file, 'r') as file:
            input = file.read()
        for line in input.split("\n"):
            if line != "":
                src_list.append(line)
    else:
        err_msg = "##ERR## Input file '%(input_file)' does not exist"
        sys.exit(err_msg)
    
    id = 0
    for src_entry in src_list:
        id += 1
        output_nslookup = nslookup(src_entry)
        ip = output_nslookup[0]
        hostname = output_nslookup[1]

        if ip != "NSLOOKUP_FAILED":
            result_ping = ping(ip)
        else:
            result_ping = "NOT_ATTEMPTED"
        #result.append(dict(Source = src_entry, IP = ip, Hostname = hostname, Ping = result_ping))
        result.append(dict(zip(key_names, [id, src_entry, ip, hostname, result_ping])))
    
    #using pandas to export to CSV
    df = pd.DataFrame(result)
    date = pd.Timestamp('today').strftime("%Y%m%d") + "-" + pd.Timestamp('now').strftime("%H%M")
    output_file = "".join([date,"-output-",input_file[:-3],"csv"])
    
    df.to_csv(output_file, sep=";", index=False)
    
    #using old way of CSV export
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