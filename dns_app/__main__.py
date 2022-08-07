from dns_logik import load_zones,buildresponse,load_blacklist,getrecs
import socket
import json
#read config for dns

with open('dns_config.json') as f:
    # returns JSON object as 
    # a dictionary
    data = json.load(f);



port = data['port'];
ip = data['ip'];

ip_string = ip[0];
port_int = int(port[0]);

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
sock.bind((ip_string, port_int));

global blacklist;

global zonedata;

zonedata = load_zones();

#records, rectype, domainname = getrecs(data[12:],zonedata);

blacklist  = load_blacklist();

listb = blacklist['blacklist'];

if __name__ == '__main__':
    while 1:
        data, addr = sock.recvfrom(512)
        r = buildresponse(data,zonedata,listb)
        sock.sendto(r, addr)