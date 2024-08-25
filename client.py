import socket
import threading

HOST='127.0.0.1'
# HOST='192.168.31.1'
PORT=6209

def listen_fmessages_frserver(client):

    while 1:

        message = client.recv(2048).decode('utf-8')
        if message != '':
            username = message.split("~")[0]
            content = message.split('~')[1]

            print(f"[{username}] {content}")
        else:
            print("message from client is empty")

def sendmessage_tserver(client):

    while 1:

        message = input("message: ")
        if message != '':
            client.sendall(message.encode())
        else:
            print("empty message")
            exit(0)


def communicate_to_server(client):
    
    username = input("Enter username: ")
    if username != '':
        client.sendall(username.encode())
    else:
        print("username can't be empty")
        exit(0)

    threading.Thread(target=listen_fmessages_frserver, args=(client, )).start()

    sendmessage_tserver(client)
 
def main():

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((HOST, PORT))
        print('successfully connected to the server')
    except:
        print(f'unable to connect to server {HOST} {PORT}')

    communicate_to_server(client)

if __name__=='__main__':
    main()
