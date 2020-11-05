#!/usr/bin/env python3

import struct

class handler:
    def __init__(self, sock):
        self.sock = sock
    def send(self, data):
        payloaded_packet = struct.pack('>I', len(data)) + data
        self.sock.sendall(payloaded_packet)
    def recv(self):
        payloaded_packet_length = self.recvall(4)
        if not payloaded_packet_length: return ""
        payloaded_packet_length = struct.unpack('>I', payloaded_packet_length)[0]
        return self.recvall(payloaded_packet_length)
    def recvall(self, n):
        payloaded_packet = "".encode("UTF-8")
        while len(payloaded_packet) < n:
            frame = self.sock.recv(n - len(payloaded_packet))
            if not frame:
                return None
            payloaded_packet += frame
        return payloaded_packet
