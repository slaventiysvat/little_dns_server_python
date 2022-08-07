# little_dns_server_python

here I repeated lessons from one youtube channel where I use guide how to create my own dns server
Here i included some my own changes
So my task looks like:

# Write a DNS proxy server with support for the "black" list of domain names.

#1. For parameters, a configuration file is used, which is read when the server starts;

#2. "Black" list of domain names is in the configuration file;

#3. The address of the upstream server is also in the configuration file;

#4. The server accepts requests from DNS clients on a standard port;

#5. If the request contains a domain name included in the "black" list, the server returns to the client the response specified by the configuration file (options: not resolved, address in the local network, ...).

#6. If the request contains a domain name that is not included in the "black" list, the server redirects the request to the upstream server, waits for a response and returns it to the client.

#little user manual
main function has the name __main__.py, you can call dns server from root folder of repo using command python3 -m dns_app
configurations script for blacklist.json folder black_list, 
if you want to add new web cite for blacklist, use script black_list_create.py
configuration for dns_app - dns_config.json, rewrite config use script dns_config.py
forder with zone files in filder zone add here all webcites
