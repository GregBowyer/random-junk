#!/usr/bin/env python
import asyncore, socket
from xdrlib import Unpacker

GANGLIA_METADATA_MESSAGE = 0x80
GANGLIA_METRIC_MESSAGE = 0x85
MAX_UDP_PACKET_SIZE = 65535
DEFAULT_PORT = 8649
DEFAULT_HOST = '' # i.e. bind to 0.0.0.0

class GangliaServer(asyncore.dispatcher):
    ''' Async core server that listens to the Ganglia port and dumps any
        incoming XDR packets conforming to the Hadoop format as derived from
        org.apache.hadoop.metrics.ganglia.GangliaContext31 '''

    def __init__(self, host=DEFAULT_HOST, port=DEFAULT_PORT):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.bind((host, port))

    def handle_read(self):
        # Not ever going to be bigger than the payload for UDP ?
        # Nothing in the XDR spec appears to provide continutation indicators
        data = self.recv(MAX_UDP_PACKET_SIZE)
        decoded_data = self.decode_data(data)
        if decoded_data:
            print decoded_data

    def decode_data(self, data):
        ''' Decodes 1 UDP Ganglia packet, returns a dict of the decoded data '''
        ret = {}
        xdr = Unpacker(data)

        message_type = xdr.unpack_int()

        if message_type == GANGLIA_METADATA_MESSAGE:
            ret = {
                'METRIC':       'METADATA',
                'hostname':     xdr.unpack_string(),
                'name':         xdr.unpack_string(),
                'spoof':        bool(xdr.unpack_int()),
                'metric_type':  xdr.unpack_string(),
                'metric_name':  xdr.unpack_string(),
                'units':        xdr.unpack_string(),
                'slope':        xdr.unpack_int(),
                'time_max':     xdr.unpack_int(),
                'data_max':     xdr.unpack_int()
            }

            assert xdr.unpack_int() == 1
            assert xdr.unpack_string() == 'GROUP'
            ret['group'] = xdr.unpack_string()

        elif message_type == GANGLIA_METRIC_MESSAGE:
            ret = {
                'type':      'METRIC',
                'hostname':  xdr.unpack_string(),
                'metric':    xdr.unpack_string(),
                'spoof':     bool(xdr.unpack_int()),
                'format':    xdr.unpack_string(),
                'value':     xdr.unpack_string()
            }

        xdr.done()

        return ret

def run_server():
    server = GangliaServer()
    asyncore.loop()

if __name__ == '__main__':
    run_server()
