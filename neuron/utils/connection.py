import socket


class Connection:
    def __init__(self, socket):
        self.socket = socket

    def __repr__(self):
        local_ip, local_port = self.socket.getsockname()
        remote_ip, remote_port = self.socket.getpeername()
        return f'<{self.__class__.__name__} ' + \
            f'from {local_ip}:{local_port} ' + \
            f'to {remote_ip}:{remote_port}>'

    def __enter__(self):
        return self

    def __exit__(self, exception, error, traceback):
        self.close()

    @classmethod
    def connect(cls, host, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        return cls(sock)

    def send(self, data):
        self.socket.sendall(data)

    def receive(self, length):
        current_len = 0
        msg = bytes()
        while current_len < length:
            remaining = length - current_len
            buff = self.socket.recv(remaining)

            if not buff and current_len != 0:
                raise RuntimeError('incomplete data')
            elif not buff and current_len == 0:
                return msg

            msg += buff
            current_len = len(msg)

        return msg

    def close(self):
        self.socket.close()
