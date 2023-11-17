const { InfluxDB, Point } = require('@influxdata/influxdb-client');

// This is a test thing
const token = "6b0bd7cfadba46e46c53747166365971";
const org = "school";
const bucket = "telegraf";

const client = new InfluxDB({url: 'http://localhost:8086', token: token});

const queryApi = client.getQueryApi(org)

const query = `from(bucket: "telegraf") |> range(start: -1h)`
queryApi.queryRows(query, {
  next(row, tableMeta) {
    const o = tableMeta.toObject(row)
    console.log(`${o._time} ${o._measurement}: ${o._field}=${o._value}`)
  },
  error(error) {
    console.error(error)
    console.log('Finished ERROR')
  },
  complete() {
    console.log('Finished SUCCESS')
  },
})

