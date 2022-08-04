import socket
#work with my own dns server 
#guide taked from https://www.youtube.com/watch?v=sjNaoJ_-cvc&ab_channel=howCode
#from https://www.ietf.org/rfc/rfc1035.txt
#Network Working Group                                     P. Mockapetris
#Request for Comments: 1035                                           ISI
                                                           #November 1987
#Obsoletes: RFCs 882, 883, 973

#            DOMAIN NAMES - IMPLEMENTATION AND SPECIFICATION
port = 53;
ip = "127.0.0.1";
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
sock.bind((ip,port));

while 1:
    data, addr = sock.recvfrom(512);
    print(data)