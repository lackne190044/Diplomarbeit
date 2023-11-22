import io

from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

from flask import Flask, jsonify, render_template, Response

import matplotlib.pyplot as plt

app = Flask(__name__)

def get_data_from_influx(url, token, org, bucket):
    influx_db_data = []
    with InfluxDBClient(url=url, token=token, org=org) as client:
        query = 'from(bucket: "telegraf") |> range(start: -10m)'
        tables = client.query_api().query(query, org=org)
        for table in tables:
            for record in table.records:
                influx_db_data.append(record)
    client.close()
    return influx_db_data

def get_my_data_from_influx(url, token, org, bucket):
    with InfluxDBClient(url=url, token=token, org=org) as client:
        query_api = client.query_api()
        query = 'from(bucket:"telegraf")\
                |> range(start: -10m)\
                |> filter(fn:(r) => r._measurement == "my_measurement")\
                |> filter(fn:(r) => r.location == "Prague")\
                |> filter(fn:(r) => r._field == "temperature")'
        result = query_api.query(org=org, query=query)
        results = []
        for table in result:
            for record in table.records:
                results.append((record.get_field(), record.get_value(), record.get_measurement()))
        return results

def get_sensor_data(url, token, org, bucket):
    with InfluxDBClient(url=url, token=token, org=org) as client:
        query_api = client.query_api()
        query = 'from(bucket: "telegraf")\
                  |> range(start: -10m)\
                  |> filter(fn: (r) => r["_measurement"] == "system")\
                  |> filter(fn: (r) => r["_field"] == "load15")'
        result = query_api.query(org=org, query=query)
        results = []
        for table in result:
            for record in table.records:
                results.append((record.get_field(), record.get_value(), record.get_measurement(), record.get_time()))
        return results

@app.route('/api/data/img', methods=['GET'])
def get_png():
    data_to_png(influx_db_data)
    return render_template('index.html')

def data_to_png(data):
    x = []
    y = []
    for row in data:
        x.append(row[3])
        y.append(row[1])
    plt.plot(x, y)
    fig_size = plt.rcParams["figure.figsize"]
    fig_size[0] = 12
    fig_size[1] = 5
    plt.rcParams["figure.figsize"] = fig_size
    plt.savefig('./static/plot.png')
    plt.close()

@app.route('/api/data', methods=['GET'])
def get_data():
    data = influx_db_data
    # for _data in influx_db_data:
    #     data.append(_data)
    # return jsonify(data)

    # return render_template('index.html')
    return str(data)

if __name__ == '__main__':
    # You can generate an API token from the "API Tokens Tab" in the UI
    token = "6b0bd7cfadba46e46c53747166365971"
    org = "school"
    bucket = "telegraf"
    url = "http://localhost:8086"

    # influx_db_data = get_my_data_from_influx(url, token, org, bucket)
    # influx_db_data = get_my_data_from_influx(url, token, org, bucket)
    influx_db_data = get_sensor_data(url, token, org, bucket)

    app.run(debug=True)

