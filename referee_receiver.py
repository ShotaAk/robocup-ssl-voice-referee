import socket
import ssl_gc_referee_message_pb2

class RefereeReceiver:
    def __init__(self, addr, port):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Avoid error 'Address already in use'.
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Construct a membership_request
        membership_request = socket.inet_aton(addr) + socket.inet_aton('0.0.0.0')
        # Send add membership request to socket
        self._sock.setsockopt(socket.IPPROTO_IP, 
            socket.IP_ADD_MEMBERSHIP, membership_request)
        # Bind the socket to an interfaces
        self._sock.bind((addr, port))

    def get_referee_message(self):
        rcv_data, addr = self._sock.recvfrom(1024)

        referee_msg = ssl_gc_referee_message_pb2.Referee()
        referee_msg.ParseFromString(rcv_data)
        return referee_msg

    def close(self):
        self._sock.close()
