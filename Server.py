import socket
import pickle
import random


def encrypt_message(K, message):
    return ''.join([chr(ord(message[i]) + K) for i in range(len(message))])


def decrypt_message(K, message):
    return ''.join([chr(ord(message[i]) - K) for i in range(len(message))])


open('Log.txt', mode='w').close()

b = random.randint(1000, 10000)
port = int(input('Input a port: '))
sock = socket.socket()
sock.bind(('', port))
print('Server start on: {}.\nPort: {}'.format(*sock.getsockname()))
sock.listen(1)
fl = False

while True:
    print('Waiting for connection.....')
    conn, addr = sock.accept()
    print('Connected: {}. Port: {}'.format(*addr))
    g, p, A = pickle.loads(conn.recv(1024))
    B = (g**b) % p
    K = (A**b) % p
    print(f'g = {g}, p = {p}, A = {A}, B = {B}, K = {K}')
    conn.send(pickle.dumps(K))
    while True:
        data = conn.recv(1024).decode()
        data_dec = decrypt_message(K, data)
        print(f'Data received.')
        print(f'Data: {data}')
        print(f'Decrypted data: {data_dec}')
        if data_dec.upper() == 'EXIT':
            conn.close()
            print('Connection closed.')
            break
        elif data_dec.upper() == 'CLOSE':
            fl = True
            conn.close()
            break
        else:
            conn.send(encrypt_message(K, data_dec).encode())
            print('Data sent.')
    if fl:
        sock.close()
        print('Socket closed')
        break

