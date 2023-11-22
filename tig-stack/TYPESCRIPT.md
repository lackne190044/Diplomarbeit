## Installation

npm init
npm install typescript
npm i @influxdata/influxdb-client
npm i --save-dev @types/node

## Compile code

npx tsc

## Starting the containers again

sudo docker-compose up --build

## For the test thing

# Install

npm init -y influx-node-app
npm i -g typescript && npm i --save-dev @types/node
tsc --init
npm install --save @influxdata/influxdb-client
npm install --save @influxdata/influxdb-client-apis

# Run

node index.js

# TODO:

- Maby use express to host the node thing onto server
- Then call the server from normal js and output the data
- Make data pretty

# Changes in Plan!!!!!

- Access the influxdb using python
- Throwing it into App.vue or something like it
- Using matplotlib or something for graphs (MABY)
