const { InfluxDB, Point } = require('@influxdata/influxdb-client');

const token = "6b0bd7cfadba46e46c53747166365971";
const org = "school";
const bucket = "telegraf";

const client = new InfluxDB({url: 'http://localhost:8086', token: token});

const queryApi = client.getQueryApi(org)

// const express = require('express')
// const app = express()
// const port = 3000


// app.listen(port, () => {
//   console.log(`Example app listening on port ${port}`)
// })


// app.get('/', (req, res) => {
//     res.send("Test thing");
// })

let i = 0;
const query = `from(bucket: "telegraf") |> range(start: -1h)`
queryApi.queryRows(query, {
    next(row, tableMeta) {
	const o = tableMeta.toObject(row)
	i++;
	console.log('${o._time} ${o._measurement}: ${o._field}=${o._value}');
	// res.send(output);

	if (i >= 100) {
	    // i want to break out here without exeting the apt.get thing
	    queryHandler.cancel();
	}
    },
    error(error) {
	console.error(error)
	console.log('Finished ERROR')
    },
    complete() {
	console.log('Finished SUCCESS')
    },
})
