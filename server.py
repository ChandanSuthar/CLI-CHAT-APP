import socket
import threading

HOST='127.0.0.1'
# HOST='192.168.31.1'
PORT=6209
LISTENER_LIMIT=5
active_clients=[]

def listenf_umessages(client, username):
    
    while 1:

        message= client.recv(2048).decode('utf-8')
        if message != '':
            final_msg = username + '~' + message
            ONAIR(final_msg)
        else:
            print(f"The message sent from client {username} is empty")

def SM_client(client, message):
    client.sendall(message.encode())

def ONAIR(message):
    for user in active_clients:
        SM_client(user[1],message)

def client_handler(client):
    
    while 1:
         
         username = client.recv(2048).decode('utf-8')
         if username != '':
             active_clients.append((username, client))
             prompt_message = "SERVER~" + f"{username} has been added to the chat"
             ONAIR(prompt_message)
             break
         else:
             print("client username is empty")
    threading.Thread(target=listenf_umessages, args=(client, username, )).start()

def main():
    server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #SOCK_DGRAM for UDP

    try:
        server.bind((HOST,PORT))
        print(f'server is running on {HOST} {PORT}')
    except:
        print(f'unable to bind to host->{HOST} and port->{PORT}')

    server.listen(LISTENER_LIMIT)

    while 1:

        client, address = server.accept()
        print(f'successfully connected to client {address[0]} {address[1]}')

        threading.Thread(target=client_handler, args=(client, )).start()

if __name__=='__main__':
    main()

