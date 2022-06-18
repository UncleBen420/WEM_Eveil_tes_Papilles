<template>
  <div v-if="loading">Loading ...</div>
  <div v-else>
    <h1>Résultas</h1>
  </div>
</template>

<script>
import BackendService from "../../services/backend.service";

export default {
  name: "RecipeReplacement",
  data: () => ({
    loading: true,
    results: null,
  }),
  methods: {
    async fetch() {
      try {
        const {data} = await BackendService.recipeReplacement('flan au chocolat', ['chocolat']);
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
