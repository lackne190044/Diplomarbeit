<script lang="ts">
import axios from 'axios';

export default {
  data() {
    return {
      hosts: ['3e9d28342037'],

      raw_results: {},
      imgBlobUrl: {},

      displayRawData: {},
      displayImg: {},

      Measure: null,
      field: null,
      host: null,

      time_0: null,
      time_0_unit: 'm', 

      time_1: null,
      time_1_unit: 'm', 
    };
  },
  methods: {
    fetchRaw(measure, field, host) {
      this.displayRawData[host] = true;
      this.displayImg[host] = false;
      
      const url = `http://localhost:5000/data?mesure=${measure}&field=${field}&host=${host}&start=${this.time_0 + this.time_0_unit}&stop=${this.time_1 + this.time_1_unit}`
      axios.get(url)
        .then(response => {
          console.log(response.data);
          this.raw_results[host] = response.data;
        })
        .catch(error => {
          console.error(error);
        });
    },
    fetchImg(measure, field, host) {
      this.displayRawData[host] = false;
      this.displayImg[host] = true;
      console.log(this.time_0);
      console.log(this.time_0_unit);
      const url = `http://localhost:5000/data/img?mesure=${measure}&field=${field}&host=${host}&start=${this.time_0 + this.time_0_unit}&stop=${this.time_1 + this.time_1_unit}`
      axios.get(url, { responseType: 'arraybuffer' })
        .then(response => {
          const blob = new Blob([response.data], { type: 'image/png' });
          this.imgBlobUrl[host] = URL.createObjectURL(blob);
        })
        .catch(error => {
          console.error(error);
        });
    },
    close(host) {
      this.displayRawData[host] = false;
      this.displayImg[host] = false;
    },
  },
  beforeDestroy() {
    // Clean up the blob URL to prevent memory leaks
    if (this.imgBlobUrl) {
      URL.revokeObjectURL(this.imgBlobUrl);
    }
  },
};
</script>

<style>
.data-table {
  border-collapse: collapse;
  width: 100%;
}

.data-table th, .data-table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

.data-table th {
  background-color: #f2f2f2;
}
</style>


<template>
  <div class="container">
    <div class="row bg-primary mt-2 mb-1">
      <div
	class="col"
	data-bs-toggle="tooltip"
	data-bs-placement="top"
	data-bs-title="Tooltip on top"
      >
	Name
      </div>
      <div class="col">Data</div>
      <div class="col">Image</div>
      <div class="col">Time</div>
      <div class="col">Closing</div>
    </div>

    <div class="row bg-secondary rounded mt-2 mb-1">
      <div class="col">Test 1</div>
      <div class="col"><button @click="fetchRaw('mem', 'active', hosts[0])">Fetch table</button></div>
      <div class="col"><button @click="fetchImg('mem', 'active', hosts[0])">Fetch image</button></div>
      <div class="col">
	<input v-model="time_0" type="number" min="-999999" max="999999" />
	<select v-model="time_0_unit" name="time" id="time"> 
	  <option value="s">Seconds</option> 
	  <option value="m">Minutes</option> 
	  <option value="d">Days</option> 
	</select>
	<input v-model="time_1" type="number" min="-999999" max="999999" />
	<select v-model="time_1_unit" name="time" id="time"> 
	  <option value="s">Seconds</option> 
	  <option value="m">Minutes</option> 
	  <option value="d">Days</option> 
	</select>
      </div>
      <div class="col"><button @click="close(hosts[0])">Close</button></div>
      <div v-if="displayImg[hosts[0]]">
	<img :src="imgBlobUrl[hosts[0]]" />
      </div>
      <div v-if="displayRawData[hosts[0]]">
	 <table class="data-table">
	  <thead>
	    <tr>
	      <th>Time</th>
	      <th>Value</th>
	    </tr>
	  </thead>
	  <tbody>
	    <tr v-for="(item, index) in raw_results[hosts[0]]" :key="index">
	      <td>{{ item.time }}</td>
	      <td>{{ item.value }}</td>
	    </tr>
	  </tbody>
	</table>
      </div>
    </div>
  </div>
</template>

<style>
  .container {
    position: absolute;
    width: 100%;
    top: 25px;
    left: 10%;
  }
</style>
