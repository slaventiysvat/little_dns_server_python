import socket
from sys import byteorder
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


def getflags(flags):
    byte1 = bytes(flags[0:1]);
    byte2 = bytes(flags[1:2]);
    rflags = "";
    QR = "1";
    OPCODE = "";
    for bit in range(1,5):
        OPCODE = OPCODE + str(ord(byte1)&(1<<bit)); 
    AA = "";
    TC = "0"; #Truncation
    RD = ""; 
    RA = "0";
    Z = "000";
    RCODE = "0000";
    return int((QR+OPCODE+AA+TC+RD),2).to_bytes(1,byteorder = "big") + int(RA+Z+RCODE,2).to_bytes(1,byteorder = "big");

def buidresponse(data):
    #Get Transaction ID
    TransactionId = data[0:2];
    TID = "";
    for byte in TransactionId:
        TID = TID + hex(byte)[2:];
        #print("byte = ",byte);

    #Get Flags
    Flags = getflags(data[2:4]);
    print(Flags);
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