// app.ts
const message = 'Hello, World!';
console.log(message);
const { InfluxDB } = require('@influxdata/influxdb-client'); // You can generate an API token from the "API Tokens Tab" in the UI
const token = '6b0bd7cfadba46e46c53747166365971';
const org = 'school';
const bucket = 'telegraf';
const client = new InfluxDB({ url: 'http://localhost:8086', token: token });
