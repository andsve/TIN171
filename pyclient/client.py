import socket

from messages import ToMessage

class Client:
    def __init__(self):
        self.socket = None
        
    def connect(self, server):
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect(server)
        except:
            return False
        return True
            
    def run(self):
        while True:
            data = self.client.recv(1024)
            print(ToMessage(data))
        
                        

def main(args):
    from sys import exit
    
    if len(args) == 2:
        addr = args[0]
        port = int(args[1])
    else:
        addr = "komugi.se"
        port = 8880
    
    server = (addr, port)
    client = Client()
    if not client.connect(server):
        print("Could not connect to: {0}".format(server))
        exit(-1)
        
    client.run()

if __name__ == '__main__':
    import sys
    main(sys.argv[1:])