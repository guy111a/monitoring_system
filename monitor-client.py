
import socket
import pickle


host = '10.*.*.*'
port = 60005


def getData():
    import os
    import psutil
    import json
    import time


    hostname = socket.gethostname()
    # Getting loadover15 minutes
    load1, load2, load15 = psutil.getloadavg()
    cpu_usage = (load15/os.cpu_count()) * 100
    vMem = psutil.virtual_memory()[2]
    ram_used = psutil.virtual_memory()[3]/1000000000
    temps = psutil.sensors_temperatures()
    process = psutil.pids()
    # for p in process:
    #     print(psutil.Process(p))
    d = dict();
    d["agent_id"] = str(hostname)
    d["num_of_proc"] = str(len(process))
    d["cpu_avg_load"] = str(int(cpu_usage))
    d["cpu_usage"] = str(round(cpu_usage))
    d["vMem"] = str(vMem)
    d["ram_used"] = str(round(ram_used))
    d["temps"] = json.dumps(temps)
    d["time_stamp"] = time.time()
    
    return d


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    data = getData()
    s.sendall(pickle.dumps(data))
    print('sent')
    


