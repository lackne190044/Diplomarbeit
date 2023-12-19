import io
import pytz

from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

from  fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

import matplotlib.pyplot as plt

influx_db_load_data = {
    'token': "6b0bd7cfadba46e46c53747166365971",
    'org': "school",
    'bucket': "telegraf",
    'url': "http://influxdb:8086"
}

app = FastAPI()

# CORS settings to allow requests from all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this to the specific origins you want to allow
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_data_from_influx(url, token, org, bucket, mesurement, field, host):
    influx_db_data = []
    with InfluxDBClient(url=url, token=token, org=org) as client:
        # start:   0  = the absolute start
        # start: -10m = last 10 minutes
        # start: -10d = last 10 days
        query = f'from(bucket: "telegraf")\
                 |> range(start: -10m)\
                 |> filter(fn: (r) => r["_measurement"] == "{mesurement}")\
                 |> filter(fn: (r) => r["_field"] == "{field}")\
                 |> filter(fn: (r) => r["host"] == "{host}")'
        tables = client.query_api().query(query, org=org)
        for table in tables:
            for record in table.records:
                time_gmt = record.get_time().astimezone(pytz.timezone('Europe/Paris'))
                influx_db_data.append({"time": time_gmt, "value": record.get_value()})
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
    plt.rcParams["figure.figsize"] = [12, 5]
    plt.savefig('/tmp/plot.png')
    plt.close()

@app.get('/data/img0')
def get_png0():
    data = get_data_from_influx(influx_db_load_data['url'], influx_db_load_data['token'], influx_db_load_data['org'], influx_db_load_data['bucket'],
                                "mem", "active", "bc690f07f6f3")
    data_to_png(data)
    return FileResponse('/tmp/plot.png')

@app.get('/data/img1')
def get_png1():
    data = get_data_from_influx(influx_db_load_data['url'], influx_db_load_data['token'], influx_db_load_data['org'], influx_db_load_data['bucket'],
                                "kernel", "context_switches", "bc690f07f6f3")
    data_to_png(data)
    return FileResponse('/tmp/plot.png')

@app.get('/data0')
def get_data0():
    data = get_data_from_influx(influx_db_load_data['url'], influx_db_load_data['token'], influx_db_load_data['org'], influx_db_load_data['bucket'],
                                "mem", "active", "bc690f07f6f3")
    return data

@app.get('/data1')
def get_data1():
    data = get_data_from_influx(influx_db_load_data['url'], influx_db_load_data['token'], influx_db_load_data['org'], influx_db_load_data['bucket'],
                                "kernel", "context_switches", "bc690f07f6f3")
    return data

