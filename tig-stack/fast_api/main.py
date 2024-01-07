import io
import pytz

from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

from  fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

import matplotlib.pyplot as plt
import numpy as np

influx_db_load_data = {
    'token': "6b0bd7cfadba46e46c53747166365971",
    'org': "school",
    'bucket': "telegraf",
    # 'url': "http://172.31.182.123:8086",
    'url': "http://influxdb:8086",
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

def get_data_from_influx(url, token, org, bucket, mesurement, field, host, topic):
    influx_db_data = []
    with InfluxDBClient(url=url, token=token, org=org) as client:
        # start:   0  = the absolute start
        # start: -10m = last 10 minutes
        # start: -10d = last 10 days
        if topic != "":
            query = f'from(bucket: "telegraf")\
                     |> range(start: -15m)\
                     |> filter(fn: (r) => r["_measurement"] == "{mesurement}")\
                     |> filter(fn: (r) => r["_field"] == "{field}")\
                     |> filter(fn: (r) => r["host"] == "{host}")\
                     |> filter(fn: (r) => r["topic"] == "{topic}")'
        else:
            query = f'from(bucket: "telegraf")\
                     |> range(start: -15m)\
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

def data_to_png(data):
    x = []
    y = []
    for row in data:
        x.append(row["time"])
        y.append(row["value"])

    # Check if y is not empty
    if not y:
        print("Empty data. Cannot generate plot.")
        return

    # Calculate analytics
    average_value = np.mean(y)
    
    if len(y) > 0:
        highest_point = max(y)
        lowest_point = min(y)
    else:
        highest_point = None
        lowest_point = None    

    # Plot the data
    plt.plot(x, y)

    # Annotate analytics on the plot
    plt.axhline(y=average_value, color='r', linestyle='--', label=f'Average: {average_value:.2f}')
    plt.scatter(x[y.index(highest_point)], highest_point, color='g', marker='.', label=f'Highest: {highest_point:.2f}')
    plt.scatter(x[y.index(lowest_point)], lowest_point, color='b', marker='.', label=f'Lowest: {lowest_point:.2f}')

    # Set plot parameters
    plt.rcParams["figure.figsize"] = [12, 5]
    plt.legend()
    plt.savefig('/tmp/plot.png')
    plt.close()

@app.get('/data/img')
def get_png(mesure: str="mqtt_consumer", field: str="value", host: str="6e2afc2e10d4", topic: str=""):
    data = get_data_from_influx(influx_db_load_data['url'], influx_db_load_data['token'], influx_db_load_data['org'], influx_db_load_data['bucket'],
                                mesure, field, host, topic)
    data_to_png(data)
    return FileResponse('/tmp/plot.png')

@app.get('/data')
def get_data(mesure: str="mqtt_consumer", field: str="value", host: str="6e2afc2e10d4", topic: str=""):
    data = get_data_from_influx(influx_db_load_data['url'], influx_db_load_data['token'], influx_db_load_data['org'], influx_db_load_data['bucket'],
                                mesure, field, host, topic)
    return data

