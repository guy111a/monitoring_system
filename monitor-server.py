


import socket
import threading 
from pymongo import MongoClient
import json
import pickle


host = '0.0.0.0'
port = 60005
udpPort = 60001
udpHost = ''
mongo_host = '10.*.*.*'

mydatabase = "monitoring"
mycollection ="monitoring_data"

ip_address = socket.gethostbyname(socket.gethostname())

def handle(client):
    while True:
        data = client.recv(1024)#.decode()
        # print(f'> {data}')
        client = MongoClient(f'mongodb://{mongo_host}:27017/')
        db = client[mydatabase]
        collection = db[mycollection]
        mydata = pickle.loads(data)
        print(mydata)
        print(type(mydata))
        collection.insert_one(mydata,  bypass_document_validation=False )
        print(f'disconnected')
        break

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port))
    s.listen(1)

    print(f"Mon_Server listening on IP : {ip_address}, port: {port}")
    while True:
        con, addr = s.accept()
        print(f'{addr} connected')

        thread = threading.Thread(target = handle, args = (con, ))
        thread.start()
