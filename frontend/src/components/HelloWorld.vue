<template>
  <div>
    <h1>{{ message }}</h1>
  </div>
</template>

<script>
export default {
  data() {
    return {
      message: '',
    };
  },
  mounted() {
    fetch('http://127.0.0.1:5000/')
      .then(response => response.text())
      .then(data => {
        this.message = data;
      })
      .catch(error => console.error('Error fetching data:', error));
  },
};
</script>

<style scoped>
h1 {
  color: blue;
}
</style>
