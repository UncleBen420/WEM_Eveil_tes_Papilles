<template>
  <div class="flex flex-col gap-4">
    <h1>Rechercher par Ingrédients</h1>
    <form @submit.prevent="fetch" class="-mt-4">
      <label>Type </label>
      <select v-model="type">
        <option value="entree">Entrée</option>
        <option value="plat">Plat</option>
        <option value="dessert">Dessert</option>
      </select>

      <label>Ingrédients</label>
      <textarea v-model="ingredients" placeholder="whisky,farine,oeuf"></textarea>

      <div>
        <button class="btn">Rechercher</button>
      </div>
    </form>

    <div v-if="results">
      <h1>Résultats</h1>
      <div v-if="loading">Loading ...</div>
      <RecipeList v-else-if="results.length" :recipes="results"/>
      <div v-else>Aucuns résulats trouvés.</div>
    </div>
  </div>
</template>

<script>
import BackendService from "../../services/backend.service";
import RecipeList from "../RecipeList.vue";

export default {
  name: "RecipeByIngredients",
  components: {RecipeList},
  data: () => ({
    loading: false,
    results: null,
    type: 'plat',
    ingredients: null,
  }),
  methods: {
    async fetch() {
      this.loading = true;
      try {
        const {data} = await BackendService.recipeByIngredients(this.type, this.ingredients.split(','));
        this.results = data;
      } catch (error) {
      }

      this.loading = false;
    }
  },
}
</script>

