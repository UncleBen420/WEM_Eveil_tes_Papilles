<template>
  <div class="flex flex-col gap-4">
    <h1>Suggestion d'ingrédients pour une recette.</h1>
    <form @submit.prevent="fetch" class="-mt-4">
      <label>Recette</label>
      <input v-model="recipe" placeholder="tarte aux pommes">

      <div>
        <button class="btn">Rechercher</button>
      </div>
    </form>

    <Results :results="results" :loading="loading">
      <ul class="list-disc ml-4">
        <li v-for="ingredient in results">{{ingredient}}</li>
      </ul>
    </Results>
  </div>
</template>

<script>
import BackendService from "../../services/backend.service";
import Results from "../Results.vue";

export default {
  name: "RecipeSuggestion",
  components: {Results},
  data: () => ({
    loading: false,
    results: null,
    recipe: '',
  }),
  methods: {
    async fetch() {
      this.loading = true;

      try {
        const {data} = await BackendService.recipeSuggestion(this.recipe);
        this.results = data.ingredients || [];
        console.log(this.results);
      } catch (error) {
      }

      this.loading = false;
    }
  },
}
</script>

<style scoped>

</style>
