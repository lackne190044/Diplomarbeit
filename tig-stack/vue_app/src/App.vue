<template>
  <div>
    <button @click="fetchRaw">Fetch data</button>
    <button @click="fetchImg">Fetch img</button>

    <div v-if="displayRawData">
       <table class="data-table">
        <thead>
          <tr>
            <th>Time</th>
            <th>Value</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in raw_results.Data.Raw" :key="index">
            <td>{{ item.time }}</td>
            <td>{{ item.value }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-else>
      <img :src="imgBlobUrl" />
    </div>
  </div>
</template>

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

<script>
import axios from 'axios';

export default {
  data() {
    return {
      raw_results: { Data: { Raw: null } },
      imgBlobUrl: null,
      displayRawData: null,
    };
  },
  methods: {
    fetchRaw() {
      this.displayRawData = true;
      axios.get('http://localhost:5000/data')
        .then(response => {
          console.log(response.data);
          this.raw_results = { Data: { Raw: response.data } };
        })
        .catch(error => {
          console.error(error);
        });
    },
    fetchImg() {
      this.displayRawData = false;
      axios.get('http://localhost:5000/data/img', { responseType: 'arraybuffer' })
        .then(response => {
          const blob = new Blob([response.data], { type: 'image/png' });
          this.imgBlobUrl = URL.createObjectURL(blob);
        })
        .catch(error => {
          console.error(error);
        });
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
