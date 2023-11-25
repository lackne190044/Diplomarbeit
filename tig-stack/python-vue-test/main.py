import io

from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

from flask import Flask, jsonify, render_template, redirect

import matplotlib.pyplot as plt

app = Flask(__name__)

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

def get_data_from_influx(url, token, org, bucket):
    influx_db_data = []
    with InfluxDBClient(url=url, token=token, org=org) as client:
        # start:   0  = the absolute start
        # start: -10m = last 10 minutes
        # start: -10d = last 10 days
        query = 'from(bucket: "telegraf")\
                 |> range(start: -10m, stop: now())\
                 |> filter(fn: (r) => r["_measurement"] == "mem")\
                 |> filter(fn: (r) => r["_field"] == "active")\
                 |> filter(fn: (r) => r["host"] == "ddc940b2a846")'
        tables = client.query_api().query(query, org=org)
        for table in tables:
            for record in table.records:
                influx_db_data.append({"time": record.get_time(), "value": record.get_value()})
        client.close()
        return influx_db_data

def get_mqtt_data(url, token, org, bucket):
    with InfluxDBClient(url=url, token=token, org=org) as client:
        query_api = client.query_api()
        query = 'from(bucket: "telegraf")\
                  |> range(start: -10m)\
                  |> filter(fn: (r) => r["_measurement"] == "mqtt_consumer")\
                  |> filter(fn: (r) => r["_field"] == "value")\
                  |> filter(fn: (r) => r["topic"] == "telegraf/sensors/test/1")'
        result = query_api.query(org=org, query=query)
        results = []
        for table in result:
            for record in table.records:
                # results.append((record.get_field(), record.get_value(), record.get_measurement(), record.get_time()))
                influx_db_data.append({"time": record.get_time(), "value": record.get_value()})
        client.close()
        return results

def data_to_png(data):
    x = []
    y = []
    for row in data:
        x.append(row["time"])
        y.append(row["value"])
    plt.plot(x, y)
    fig_size = plt.rcParams["figure.figsize"]
    fig_size[0] = 12
    fig_size[1] = 5
    plt.rcParams["figure.figsize"] = fig_size
    plt.savefig('./static/plot.png')
    plt.close()

@app.route('/api/data/img', methods=['GET'])
def get_png():
    data = get_data_from_influx(url, token, org, bucket)
    data_to_png(data)
    return render_template('index.html')

@app.route('/api/data', methods=['GET'])
def get_data():
    data = get_data_from_influx(url, token, org, bucket)
    return jsonify(data)

@app.route('/', methods=['GET'])
def home_redirect():
    return redirect('/api/data')

if __name__ == '__main__':
    # Saving token, org, bucket and the influxdb url
    token = "6b0bd7cfadba46e46c53747166365971"
    org = "school"
    bucket = "telegraf"
    url = "http://localhost:8086"

    app.run(host="0.0.0.0", port=5000, debug=True)
