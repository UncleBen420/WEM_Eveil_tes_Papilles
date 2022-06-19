<template>
  <div class="flex flex-col gap-4">
    <h1>Rechercher par Paramètres</h1>
    <form @submit.prevent="fetch" class="-mt-4">
      <label>Type </label>
      <select v-model="type">
        <option value="entree">Entrée</option>
        <option value="plat">Plat</option>
        <option value="dessert">Dessert</option>
      </select>

      <label>Durée</label>
      <div class="flex gap-4 items-baseline">
        <p>Min</p>
        <input type="number" v-model="duration[0]">
        <p>Max</p>
        <input type="number" v-model="duration[1]">
      </div>

      <label>Nombre de personnes</label>
      <div class="flex gap-4 items-baseline">
        <p>Min</p>
        <input type="number" v-model="nbPeople[0]">
        <p>Max</p>
        <input type="number" v-model="nbPeople[1]">
      </div>

      <label>Score</label>
      <div class="flex gap-4 items-baseline">
        <p>Min</p>
        <input type="number" v-model="score[0]">
        <p>Max</p>
        <input type="number" v-model="score[1]">
      </div>

      <div>
        <button class="btn">Rechercher</button>
      </div>
    </form>

    <Results :results="results" :loading="loading">
      <RecipeList :recipes="results"/>
    </Results>
  </div>
</template>

<script>
import BackendService from "../../services/backend.service";
import RecipeList from "../RecipeList.vue";
import Results from "../Results.vue";

export default {
  name: "RecipeByParam",
  components: {Results, RecipeList},
  data: () => ({
    loading: false,
    results: null,
    type: 'plat',
    duration: [null, null],
    nbPeople: [null, null],
    score: [null, null],
  }),
  methods: {
    async fetch() {
      this.loading = true;
      this.results = [];

      try {
        const {data} = await BackendService.recipeByParam(this.type, this.duration, this.nbPeople, this.score);
        this.results = data;
      } catch (error) {
      }

      this.loading = false;
    },

  },
}
</script>

<style scoped>

</style>
