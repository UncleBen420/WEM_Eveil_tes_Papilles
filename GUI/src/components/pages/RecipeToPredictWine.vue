<template>
  <div class="flex flex-col gap-4">
    <h1>Recherche de vins s'accordant bien avec une recette.</h1>
    <form @submit.prevent="fetch" class="-mt-4">
      <label>Recette</label>
      <input v-model="recipe" placeholder="tarte aux pommes">

      <div>
        <button class="btn">Rechercher</button>
      </div>
    </form>

    <Results :loading="loading" :results="results">
      <WineList :wines="results"/>
    </Results>
  </div>
</template>

<script>
import BackendService from "../../services/backend.service";
import Results from "../Results.vue";
import WineList from "../WineList.vue"

export default {
  name: "RecipeToPredictWine",
  components: {Results, WineList},
  data: () => ({
    loading: false,
    results: null,
    recipe: '',
  }),
  methods: {
    async fetch() {
      this.loading = true;

      try {
        const {data} = await BackendService.recipeToPredictWine(this.recipe);
        this.results = data.wine || [];
      } catch (error) {
      }

      this.loading = false;
    },
  },
}
</script>

