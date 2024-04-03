import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

token = "6b0bd7cfadba46e46c53747166365971"
org = "school"
bucket = "telegraf"
# Store the URL of your InfluxDB instance
url="http://localhost:8086"

client = influxdb_client.InfluxDBClient(
    url=url,
    token=token,
    org=org
)

# Write script
write_api = client.write_api(write_options=SYNCHRONOUS)

p = influxdb_client.Point("my_measurement").tag("location", "Prague").field("temperature", 25.3)
write_api.write(bucket=bucket, org=org, record=p)

