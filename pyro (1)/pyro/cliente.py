from tkinter import *
import tkinter as tk
from tkinter import filedialog
import base64
import threading
import random
import Pyro4
import os

file_path = ""
file_download = ""
uri = ""

@Pyro4.expose
class ClientMethods:
    def requisicaoCriada(self, filename):

        filedata = server.downloadFile(filename)
        filedata = base64.b64decode(filedata['data'])

        with open("./clientFiles/" + file_download, "wb") as f:

            f.write(filedata)


server = Pyro4.Proxy("PYRONAME:file_receiver")


def receive_connection():

    global uri

    daemon = Pyro4.Daemon()
    uri = daemon.register(ClientMethods)

    ns = Pyro4.locateNS()
    ns.register("client_methods" , uri)

    daemon.requestLoop()

    filedata = server.downloadFile(file_download)
    filedata = base64.b64decode(filedata['data'])

    print(filedata)

    with open("./clientFiles/" + file_download, "wb") as f:

        f.write(filedata)


def get_file_path():
    global file_path
    file_path= filedialog.askopenfilename()
    caminho_entry.insert(0,file_path)

def upload_file():
    with open(file_path, "rb") as f:
        data = f.read()
        server.receive_file(file_path.split("/")[-1].encode("utf-8"), data)
    
def get_files():
    string = ""
    server.getFiles()
    files_str = server.returnFiles()

    for file in files_str:
        for file2 in file[2]:
            string += file2 + "\n"

    files_server.insert(tk.END, str(string))

def download_file():
    global file_download
    file_download = str(arquivo_entry.get())

    filedata = server.downloadFile(file_download)
    filedata = base64.b64decode(filedata['data'])

    print(filedata)

    with open("./clientFiles/" + file_download, "wb") as f:

        f.write(filedata)


def criarInteresse():
    global file_download
    file_download = str(arquivo_entry.get())
    tempoStr = str(tempo.get())

    server.criarInteresse(file_download, tempoStr, uri)

def excluirInteresse():
    server.excluirInteresse(uri)
    

menu_inicial = Tk()

menu_inicial.title("Pyro File Upload")
menu_inicial.geometry("600x600")

botao_arquivo = Button(menu_inicial, text="Selecione Arquivo", width=20, command=get_file_path).place(x=100,y=50)
caminho_entry = Entry(menu_inicial, width=70)
caminho_entry.place(x=10, y=80)

botao_upload = Button(menu_inicial, text="Upload", width=15, command=upload_file).place(x=10, y=110)
botao_upload = Button(menu_inicial, text="Arquivos", width=15, command=get_files).place(x=100, y=110)
botao_upload = Button(menu_inicial, text="Download", width=15, command=download_file).place(x=190, y=110)
botao_upload = Button(menu_inicial, text="Interesse", width=15, command=criarInteresse).place(x=280, y=110)

files_server = Text(menu_inicial, height = 10, width = 30)
files_server.place(x=10,y=150)

arquivo_entry = Entry(menu_inicial, width=60)
arquivo_entry.place(x=10, y=350)

tempo = Entry(menu_inicial, width=60)
tempo.place(x=10, y=400)

my_thread = threading.Thread(target=receive_connection)
my_thread.start()


botao_upload = Button(menu_inicial, text="Excluir Interesse", width=15, command=excluirInteresse).place(x=10, y=450)

menu_inicial.mainloop()