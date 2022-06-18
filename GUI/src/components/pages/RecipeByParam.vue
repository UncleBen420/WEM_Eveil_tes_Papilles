<template>
  <div v-if="loading">Loading ...</div>
  <div v-else>
    <h1>Résultas</h1>
  </div>
</template>

<script>
import BackendService from "../../services/backend.service";

export default {
  name: "RecipeByParam",
  data: () => ({
    loading: true,
    results: null,
  }),
  methods: {
    async fetch() {
      try {
        const {data} = await BackendService.recipeByParam('dessert', [30, 120], [2,6], [2,4]);
        this.results = data;
      } catch (error) {
      }

      this.loading = false;
    }
  },
  mounted() {
    this.fetch();
  },
}
</script>

<style scoped>

</style>
