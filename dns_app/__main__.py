from dns_logik import load_zones,buildresponse
import socket
port = 53
ip = '127.0.0.1'

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
sock.bind((ip, port));

global zonedata;

zonedata = load_zones();

if __name__ == '__main__':
    while 1:
        data, addr = sock.recvfrom(512)
        r = buildresponse(data,zonedata)
        sock.sendto(r, addr)