import json, glob

#work with my own dns server 
#guide taked from https://www.youtube.com/watch?v=sjNaoJ_-cvc&ab_channel=howCode
#from https://www.ietf.org/rfc/rfc1035.txt
#Network Working Group                                     P. Mockapetris
#Request for Comments: 1035                                           ISI
                                                           #November 1987
#Obsoletes: RFCs 882, 883, 973

#            DOMAIN NAMES - IMPLEMENTATION AND SPECIFICATION
#dig howcode.org @127.0.0.1 #chek out server
#python3 dns_my.py          #call server

#The header contains the following fields:
 #                                   1  1  1  1  1  1
 #     0  1  2  3  4  5  6  7  8  9  0  1  2  3  4  5
 #   +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
 #   |                      ID                       |
 #   +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
 #   |QR|   Opcode  |AA|TC|RD|RA|   Z    |   RCODE   |
 #   +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
 #   |                    QDCOUNT                    |
 #   +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
 #   |                    ANCOUNT                    |
 #   +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
 #   |                    NSCOUNT                    |
 #   +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
 #   |                    ARCOUNT                    |
 #   +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+



def load_blacklist():
    blacklist_doc = {};
    with open('blacklist.json') as f:
    # returns JSON object as 
    # a dictionary
        blacklist_doc = json.load(f);
    return blacklist_doc;


def load_zones():

    jsonzone = {}
    zonefiles = glob.glob("./zones/*.zone")

    for zone in zonefiles:
        with open(zone) as zonedata:
            data = json.load(zonedata)
            zonename = data["$origin"]
            jsonzone[zonename] = data
    return jsonzone

def getflags(flags,flag_forbiddenw):

    byte1 = bytes(flags[:1])
    byte2 = bytes(flags[1:2])

    rflags = ''

    QR = '1'

    OPCODE = ''
    for bit in range(1,5):
        OPCODE += str(ord(byte1)&(1<<bit))

    AA = '1'

    TC = '0'

    RD = '0'

    # Byte 2

    RA = '0'

    Z = '000'

    if flag_forbiddenw == 1:
        RCODE = '0010';
    else:
        RCODE = '0000';

    return int(QR+OPCODE+AA+TC+RD, 2).to_bytes(1, byteorder='big')+int(RA+Z+RCODE, 2).to_bytes(1, byteorder='big')

def getquestiondomain(data):

    state = 0
    expectedlength = 0
    domainstring = ''
    domainparts = []
    x = 0
    y = 0
    for byte in data:
        if state == 1:
            if byte != 0:
                domainstring += chr(byte)
            x += 1
            if x == expectedlength:
                domainparts.append(domainstring)
                domainstring = ''
                state = 0
                x = 0
            if byte == 0:
                domainparts.append(domainstring)
                break
        else:
            state = 1
            expectedlength = byte
        y += 1

    questiontype = data[y:y+2]

    return (domainparts, questiontype)

def getzone(domain,zonedata):
    #zonedata = load_zones();
    zone_name = ".".join(domain)
    zonedata_out = '';
    try:
        zonedata_out = zonedata[zone_name]; 
    except: #default.com.zone
        #print("An exception occurred");
       zonedata_out = zonedata['default.com.'];
    
    return zonedata_out;

def getrecs(data,zonedata):
    domain, questiontype = getquestiondomain(data)
    qt = ""
    if questiontype == b'\x00\x01':
        qt = "a"

    zone = getzone(domain,zonedata)
    domain_out = domain;
    #undefined website(in this version of code dns server knows all websites)
    #if zone.get("$origin") == "default.com.":
    #   domain_out = ['default' ,'com.',''];
    zone_out = zone[qt];
    #return (zone_out, qt, domain)
    return (zone_out, qt, domain_out)

def buildquestion(domainname, rectype):
    qbytes = b''

    for part in domainname:
        length = len(part)
        qbytes += bytes([length])

        for char in part:
            qbytes += ord(char).to_bytes(1, byteorder='big')

    if rectype == 'a':
        qbytes += (1).to_bytes(2, byteorder='big')

    qbytes += (1).to_bytes(2, byteorder='big')

    return qbytes

def rectobytes(domainname, rectype, recttl, recval):

    rbytes = b'\xc0\x0c'

    if rectype == 'a':
        rbytes = rbytes + bytes([0]) + bytes([1])

    rbytes = rbytes + bytes([0]) + bytes([1])

    rbytes += int(recttl).to_bytes(4, byteorder='big')

    if rectype == 'a':
        rbytes = rbytes + bytes([0]) + bytes([4])

        for part in recval.split('.'):
            rbytes += bytes([int(part)])
    return rbytes

def buildresponse(data,zonedata,listb):

    # Transaction ID
    TransactionID = data[:2]

    #here we choose close website or not for user
    # Get answer for query
    records, rectype, domainname = getrecs(data[12:],zonedata);

    dnsquestion = buildquestion(domainname, rectype);

    #check blacklist
    merge_name = '';
    merge_name = domainname[0] + "." + domainname[1];
    flag_forbiddenw = 0;
    for stringw in listb:
        if merge_name == stringw:
            flag_forbiddenw = 1;

    # Get the flags
    Flags = getflags(data[2:4],flag_forbiddenw);

    # Question Count
    QDCOUNT = b'\x00\x01'

    # Answer Count
    ANCOUNT = len(getrecs(data[12:],zonedata)[0]).to_bytes(2, byteorder='big')

    # Nameserver Count
    NSCOUNT = (0).to_bytes(2, byteorder='big')

    # Additonal Count
    ARCOUNT = (0).to_bytes(2, byteorder='big')

    dnsheader = TransactionID+Flags+QDCOUNT+ANCOUNT+NSCOUNT+ARCOUNT

    # Create DNS body
    dnsbody = b''

    for record in records:
        dnsbody += rectobytes(domainname, rectype, record["ttl"], record["value"])

    return dnsheader + dnsquestion + dnsbody