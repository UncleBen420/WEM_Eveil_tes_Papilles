<template>
  <div class="flex flex-col gap-4">
    <h1>Remplacement d'ingrédients pour une recette.</h1>
    <form @submit.prevent="fetch" class="-mt-4">
      <label>Recette</label>
      <input v-model="recipe" placeholder="tarte aux pommes">
      <label>Ingrédients</label>
      <input v-model="ingredient" placeholder="whisky,farine,oeuf">

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
  name: "RecipeReplacement",
  components: {Results},
  data: () => ({
    loading: false,
    results: null,
    recipe: '',
    ingredient: '',
  }),
  methods: {
    async fetch() {
      this.loading = true;
      this.results = [];

      try {
        const {data} = await BackendService.recipeReplacement(this.recipe, this.ingredient);
        this.results = data.ingredient || [];
      } catch (error) {
      }

      this.loading = false;
    }
  },
}
</script>

<style scoped>

</style>
