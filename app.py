

import time
import flask
from flask import Flask
from flask import send_file
from flask import render_template
from flask import request, jsonify, redirect
from pymongo import MongoClient
import pymongo 
import pandas as pd

chart_template = 'chart.html'
port = '3344'

client = MongoClient('mongodb://10.*.*.*:27017/')
mydb = client["monitoring"]
mycol = mydb["monitoring_data"]

app = flask.Flask(__name__)
app.config["DEBUG"] = True #False #True



@app.route('/charts', methods=('POST', 'GET')) 
def slash():
    # moving 
    return redirect("/home", code=102)


@app.route('/charts/home', methods=('POST', 'GET')) 
def base():

    result = mycol.find({}, {'agent_id':1, "_id":0})
    df = pd.DataFrame(list(result))
    df = df.sort_values(by=['agent_id'], ascending=False)
    df_fixed = pd.Series(df['agent_id'].unique())
    hosts_list = df_fixed.values.tolist()
    # print(hosts_list)
    return render_template(chart_template, hosts = hosts_list, search="show")


@app.route('/charts/showData', methods=('POST', 'GET'))  
def show_data():

    if 'host' in request.args:
        hostToShow = request.args['host']
        qnt = int(request.args['number'])
        print(f'searching for {hostToShow}, last {qnt} items.')
        result = mycol.find({"agent_id": { "$eq": hostToShow} } ).sort('time_stamp',-1).limit(qnt)
        data = []

        for item in result:
            data.append(item)

        df = pd.DataFrame(data)
        print(df)

        numOfRecords = []
        index = range(1,qnt+1)
        for i in index:
            numOfRecords.append(i)

        num_of_proc = df["num_of_proc"]
        proc = num_of_proc.to_list()
        proc = [int(float(i)) for i in proc]


        vmem = df['vMem']
        mem = vmem.to_list()
        mem = [int(float(i)) for i in mem]

        data_dict = {
            "hostname" : hostToShow, 
            "records" : numOfRecords, 
            "proc": proc, 
            "mem": mem, 
            # "tmp": tmp
        }

        if hostToShow != "banana":

            cpu_load = df['cpu_usage']
            cpu = cpu_load.to_list()
            cpu = [int(float(i)) for i in cpu]
            data_dict["cpu"] = cpu 

            ram_used = df['ram_used']
            ram = ram_used.to_list()   
            ram = [int(float(i)) for i in ram]
            data_dict["ram"] = ram

        return render_template(chart_template, data=data_dict, information="show")
    else:
        return redirect("/home", code=1001)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
