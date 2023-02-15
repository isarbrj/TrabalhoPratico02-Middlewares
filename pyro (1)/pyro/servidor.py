import Pyro4
import os
import base64
import threading
import time

users = []
files = []

stop_Flag = False

my_thread = None

def testClient():
    global users
    while True:
        while not stop_Flag:

            files = []
            filenames = os.walk("./files/")
            files = filenames
        
            print(users)

            filenames = next(files, (None, None, []))[2] 


            new_users = []

            for u in users:
                if u[1] in filenames:
                    client = Pyro4.Proxy(u[0])
                    client.requisicaoCriada(u[1])

                elif int(u[2]) > 0:
                    u[2] = int(u[2]) - 1
                    new_users.append(u)

            time.sleep(1)
            users = new_users

@Pyro4.expose
class FileReceiver:

    def __init__(self):
        global my_thread
        self.getFiles()

        my_thread = threading.Thread(target=testClient)
        my_thread.start()

    def receive_file(self, filename, filedata):
        global my_thread
        global stop_Flag

        stop_Flag = True

        filename = base64.b64decode(filename['data']).decode('utf-8')
        filedata = base64.b64decode(filedata['data'])

        with open("./files/" + filename, "wb") as f:
            f.write(filedata)

        stop_Flag = False

    def getFiles(self):
        global files
        files = []
        filenames = os.walk("./files/")
        files = filenames
    
    def returnFiles(self):
        return files
    
    def downloadFile(self, filename):
        
        print(filename)

        with open("./files/" + filename, "rb") as f:
            return f.read()
        
    def criarInteresse(self, filename, tempo, uriClient):
        global stop_Flag

        stop_Flag = True

        time.sleep(2)
        
        user = [uriClient, filename, tempo]
        users.append(user)
        
        stop_Flag = False

    def excluirInteresse(self, uri):
        global users
        global my_thread
        global stop_Flag
    
        stop_Flag = True

        time.sleep(2)

        for interesse in users:

            if str(uri).split(":")[-1] in str(interesse[0]):
                users.remove(interesse)
        

        stop_Flag = False

daemon = Pyro4.Daemon()

uri = daemon.register(FileReceiver)

print("URI: ", uri)

ns = Pyro4.locateNS()
ns.register("file_receiver", uri)

print("Server running...")
daemon.requestLoop()