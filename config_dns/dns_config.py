import json

ip_dns = [ '127.0.0.1'];

port_dns = ['53'];

to_json = {'ip': ip_dns, 'port':  port_dns};

with open('dns_config.json', 'w') as f:
    json.dump(to_json, f)
