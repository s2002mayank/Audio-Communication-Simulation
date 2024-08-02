from time import sleep
from threading import Thread, Lock, Condition
import socket

SERVER_IP = socket.gethostbyname(socket.gethostname())  #server ip address
SERVER_PORT = 7575  #port number


class Client:
    allClients = []        # every client object is added to this list
    availableClients = {}  # Dictionary implementation { str'client name' : client object -> client_socket,[IP, port]}

    def __init__(self, client_ptr):
        Client.allClients.append(self)
        self.cl_ptr = client_ptr
        self.name = None
        self.name = self.get_name()
        self.recipient_name = None
        self.recipient_name = self.get_recipient_name()
        print(f"received name {self.name} and recipient {self.recipient_name}")
        Client.availableClients[self.name] = self
        try:
            self.lobby()
        except ConnectionResetError:
            print("[CONNECTION RESET ERROR] Closing connection")
            self.close()
        except BrokenPipeError:
            print("[BROKEN PIPE] Closing connection")
            self.close()

    def lobby(self):
        cl = None
         # Enter a loop to keep searching for recipient in available clients
        while True:
            try:
                cl = Client.availableClients[self.recipient_name]
                if cl.get_recipient_name() == self.name:
                    break
                else:
                    print("recipient busy.")
                    sleep(1)
            except KeyError:
            #waiting for intended client to join { recognized solely by name}
                print("waiting...")
                sleep(1)
                continue
        if cl is not None:
            # found a client who wants to connect to self
            self.cl_ptr[0].send('go'.encode())
            self.converse(cl)
        self.close()
   
    def get_name(self):
        if self.name is None:
            # receive name
            self.name = self.cl_ptr[0].recv(512).decode().rstrip()  # 'UTF-8' to decode
            print(f"Client connected: {self.name}")
        return self.name

    def get_recipient_name(self):
        if self.recipient_name is None:
            # receive recipient name
            self.recipient_name = self.cl_ptr[0].recv(512).decode().rstrip()
            print(f"Client {self.name} wants to connect to {self.recipient_name}")
        return self.recipient_name

    # def getRecipientSocket(self):
    #     search list of available clients

    def converse(self, recipient_obj):
        print("establishing connection...")
        try:
            while True:
                self.send(recipient_obj, self.read())
        except KeyboardInterrupt:
            self.close()
        except OSError:
            self.close()

    def send(self, cl_object, data):
        cl_object.cl_ptr[0].send(data)

    def read(self):
        return self.cl_ptr[0].recv(1024)

    def close(self):
        try:
            Client.allClients.remove(self)
        except ValueError:
            print("Client does not exist in 'allClients' list")
        Client.availableClients.pop(self.get_name(), None)
        self.cl_ptr[0].close()
        print(f"Client {self.name} removed.")

def main():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"Binding socket on [{SERVER_IP}:{SERVER_PORT}]...")
    serversocket.bind((SERVER_IP, SERVER_PORT))
    print(f"Server is lisetening for connections...")
    serversocket.listen(2)

    while True:
        try:
            client_id = (serversocket.accept(),)
            thrd1 = Thread(target=client_handler, args=client_id)
            thrd1.start()
        except KeyboardInterrupt:
            serversocket.close()
            break

def client_handler(clientid):
    Client(clientid)

main()