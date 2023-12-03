<template>
  <button @click="fetchData">Fetch data</button>
</template>

<script>
import axios from 'axios';

export default {
  methods: {
    fetchData() {
      axios.get('http://localhost:5000/data')
        .then(response => {
          console.log(response.data);
          // do something with response.data
        })
        .catch(error => {
          console.error(error);
        });
    }
  }
}
</script>
