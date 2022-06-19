<template>
  <div class="flex flex-col gap-4">
    <h1>Recherche de recettes s'accordant bien avec un vin.</h1>
    <form @submit.prevent="fetch" class="-mt-4">
      <label>Vin</label>
      <input v-model="wine" placeholder="bourbon">

      <div>
        <button class="btn">Rechercher</button>
      </div>
    </form>

    <Results :loading="loading" :results="results">
      <RecipeList :recipes="results"/>
    </Results>
    <pre>{{results}}</pre>
  </div>
</template>

<script>
import BackendService from "../../services/backend.service";
import Results from "../Results.vue";
import RecipeList from "../RecipeList.vue"

export default {
  name: "WineToPredictRecipe",
  components: {Results, RecipeList},
  data: () => ({
    loading: false,
    results: null,
    wine: '',
  }),
  methods: {
    async fetch() {
      this.loading = true;

      try {
        const {data} = await BackendService.wineToPredictRecipe(this.wine);
        this.results = data.recipe || [];
      } catch (error) {
      }

      this.loading = false;
    }
  },
}
</script>

<style scoped>

</style>
