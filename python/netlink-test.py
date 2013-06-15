#!/usr/bin/python

import errno
import socket
import struct
import sys
from collections import namedtuple


## linux/netlink.h
STRUCT_NLMSGHDR = 'IHHII'

NETLINK_ROUTE           = 0

# Core message types
NLMSG_NOOP, NLMSG_ERROR, NLMSG_DONE, NLMSG_OVERRUN = range(1, 5)

# Flags values
NLM_F_REQUEST           = 0x001
NLM_F_MULTI             = 0x002
NLM_F_ACK               = 0x004
NLM_F_ECHO              = 0x010

# Modifiers to GET request
NLM_F_ROOT              = 0x100
NLM_F_MATCH             = 0x200
NLM_F_ATOMIC            = 0x400
NLM_F_DUMP              = (NLM_F_ROOT | NLM_F_MATCH)


def netlink_pack(msgtype, flags, seq, pid, data):
    return struct.pack(STRUCT_NLMSGHDR, 16 + len(data),
            msgtype, flags, seq, pid) + data


def netlink_unpack(data):
    """Unpack a sequence of netlink packets."""
    out = []
    while data:
        length, msgtype, flags, seq, pid = struct.unpack(STRUCT_NLMSGHDR,
                data[:16])
        if len(data) < length:
            raise RuntimeError("Buffer overrun!")
        out.append((msgtype, flags, seq, pid, data[16:length]))
        data = data[length:]
    return out


## linux/rtnetlink.h
RTM_NEWLINK, RTM_DELLINK, RTM_GETLINK, RTM_SETLINK = range(16, 20)
RTM_NEWADDR, RTM_DELADDR, RTM_GETADDR = range(20, 23)

STRUCT_RTATTR = 'HH'


def rtattr_unpack(data):
    """Unpack a sequence of netlink attributes."""
    size = struct.calcsize(STRUCT_RTATTR)
    attrs = {}
    while data:
        rta_len, rta_type = struct.unpack(STRUCT_RTATTR, data[:size])
        assert len(data) >= rta_len
        rta_data = data[size:rta_len]
        padded = ((rta_len + 3) / 4) * 4
        attrs[rta_type] = rta_data
        data = data[padded:]

    if data:
        print >> sys.stderr, "garbage after rtattr"

    return attrs


## linux/if_link.h
STRUCT_IFINFOMSG = 'BxHiII'
IfInfoMsg = namedtuple('IfInfoMsg', 'family type index flags change attrs')

(IFLA_UNSPEC, IFLA_ADDRESS, IFLA_BROADCAST, IFLA_IFNAME, IFLA_MTU, IFLA_LINK,
        IFLA_QDISC, IFLA_STATS, IFLA_COST, IFLA_PRIORITY, IFLA_MASTER,
        IFLA_WIRELESS, IFLA_PROTINFO, IFLA_TXQLEN, IFLA_MAP, IFLA_WEIGHT,
        IFLA_OPERSTATE, IFLA_LINKMODE, IFLA_LINKINFO, IFLA_NET_NS_PID,
        IFLA_IFALIAS, IFLA_NUM_VF, IFLA_VFINFO_LIST, IFLA_STATS64,
        IFLA_VF_PORTS, IFLA_PORT_SELF,) = range(26)


def ifinfomsg_unpack(data):
    """Unpack struct ifinfomsg and its attributes."""
    size = struct.calcsize(STRUCT_IFINFOMSG)
    family, type, index, flags, change = struct.unpack(STRUCT_IFINFOMSG,
            data[:size])
    attrs = rtattr_unpack(data[size:])
    return IfInfoMsg(family, type, index, flags, change, attrs)


## linux/if_addr.h
STRUCT_IFADDRMSG = '4BI'
IfAddrMsg = namedtuple('IfAddrMsg', 'family prefixlen flags scope index attrs')

(IFA_UNSPEC, IFA_ADDRESS, IFA_LOCAL, IFA_LABEL, IFA_BROADCAST, IFA_ANYCAST,
        IFA_CACHEINFO, IFA_MULTICAST) = range(8)


def ifaddrmsg_unpack(data):
    """Unpack struct ifaddrmsg and its attributes."""
    size = struct.calcsize(STRUCT_IFADDRMSG)
    family, prefixlen, flags, scope, index = struct.unpack(STRUCT_IFADDRMSG,
            data[:size])
    attrs = rtattr_unpack(data[size:])
    return IfAddrMsg(family, prefixlen, flags, scope, index, attrs)


## rest of code

SEQ = 1


def wilddump(sock, msgtype, filter, family=0):
    """Send one NETLINK_ROUTE request and return a list of results."""
    global SEQ
    seq = SEQ
    SEQ += 1

    sock.send(netlink_pack(msgtype=msgtype,
            flags=NLM_F_ROOT | NLM_F_MATCH | NLM_F_REQUEST,
            seq=seq, pid=0,
            data=struct.pack('Bxxx', family)))

    working = True
    out = []
    while working:
        d = sock.recv(1000000)
        for msgtype, flags, mseq, pid, data in netlink_unpack(d):
            if mseq != seq:
                raise RuntimeError("seq mismatch")
            if msgtype == NLMSG_DONE:
                working = False
                break
            elif msgtype == NLMSG_ERROR:
                raise RuntimeError("rtnl error")
            elif msgtype == NLMSG_OVERRUN:
                raise RuntimeError("rtnl overrun")
            elif msgtype in filter:
                out.append(filter[msgtype](data))
            else:
                print ('Unknown message: type=0x%x flags=0x%x payload=%d bytes'
                        % (msgtype, flags, len(data)))

    return out


def main():
    s = socket.socket(socket.AF_NETLINK, socket.SOCK_RAW, NETLINK_ROUTE)
    #s.bind((0, 0))

    links = {}
    for ifi in wilddump(sock=s, msgtype=RTM_GETLINK,
            filter={RTM_NEWLINK: ifinfomsg_unpack}):
        links[ifi.index] = ifi

    addrs = {}
    for ifa in wilddump(sock=s, msgtype=RTM_GETADDR,
            filter={RTM_NEWADDR: ifaddrmsg_unpack}):
        addrs.setdefault(ifa.index, []).append(ifa)

    for index, ifi in links.items():
        if IFLA_ADDRESS in ifi.attrs:
            hwaddr = ':'.join(x.encode('hex') for x in ifi.attrs[IFLA_ADDRESS])
        else:
            hwaddr = '<no addr>'
        print "%d: %s %s" % (ifi.index,
                ifi.attrs[IFLA_IFNAME][:-1],
                hwaddr)
        for ifa in addrs.get(ifi.index, {}):
            address = ifa.attrs.get(IFA_ADDRESS)
            if not address:
                continue
            if ifa.family == socket.AF_INET:
                family = 'inet'
            elif ifa.family == socket.AF_INET6:
                family = 'inet6'
            else:
                print '  %d %s' % (ifa.family, address.encode('hex'))
                continue
            print '  %s %s' % (family, socket.inet_ntop(ifa.family, address))


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    except IOError, err:
        if err.errno != errno.EPIPE:
            raise
