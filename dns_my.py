import socket
import time

#work with my own dns server 
#guide taked from https://www.youtube.com/watch?v=sjNaoJ_-cvc&ab_channel=howCode
#from https://www.ietf.org/rfc/rfc1035.txt
#Network Working Group                                     P. Mockapetris
#Request for Comments: 1035                                           ISI
                                                           #November 1987
#Obsoletes: RFCs 882, 883, 973

#            DOMAIN NAMES - IMPLEMENTATION AND SPECIFICATION
#dig howcode.org @127.0.0.1
port = 53;
ip = "127.0.0.1";
time_life = 40;#time that 
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
sock.bind((ip,port));
t = time.monotonic();
print("it start works", time.monotonic());



def buidresponse(data):
    TransactionId = data[0:2];
    for byte in TransactionId:
        print("byte = ",byte);
    return TransactionId;
    

while 1:
    data, addr = sock.recvfrom(512);
    r = buidresponse(data);
    print(data);
    sock.sendto(r, addr);
    distance = time.monotonic() - t;
    if distance > time_life:
    #break infinite loop
       print("it works", time.monotonic(), "difference is = ", distance);
       break;