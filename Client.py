import socket
import pickle
import random


def ip_check(ip):
    q = ip.split('.')
    if q == ['localhost']:
        return True
    elif len(q) == 4:
        q1 = list(map(lambda x: True if 0 <= int(x) <= 255 else False, q))
        if not False in q1:
            return True
    else:
        return False


def encrypt_message(K, message):
    return ''.join([chr(ord(message[i]) + K) for i in range(len(message))])


def decrypt_message(K, message):
    return ''.join([chr(ord(message[i]) - K) for i in range(len(message))])


while True:
    host_name = input('Input a host name: ')
    port = int(input('Input a port: '))
    if ip_check(host_name):
        break
    else:
        print('Host name is not an ip-address or "localhost". Try again.')
sock = socket.socket()
sock.connect((host_name, port))

g, p, a = (random.randint(1000, 10000) for i in range(3))
A = (g**a) % p
sock.send(pickle.dumps((g, p, A)))
K = pickle.loads(sock.recv(1024))
print(f'g = {g}, p = {p}, A = {A}, K = {K}')

while True:
    msg = input('Input a message: ')
    sock.send(encrypt_message(K, msg).encode())
    data = sock.recv(1024)
    if msg.lower() in ('exit', 'close'):
        break
    print(f'Message: {data}')
    print(f'Decrypted message: {decrypt_message(K, data.decode())}')
sock.close()