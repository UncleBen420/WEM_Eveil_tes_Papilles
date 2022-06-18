<template>
  <div>
    <h1 class="text-5xl">Éveil tes Papilles</h1>
    <div class="flex flex-wrap gap-x-8 gap-y-2 my-4">
      <button :class="`page-link ${route === 0 ? 'current' : ''}`" @click="goTo(0)">Ingrédients</button>
      <button :class="`page-link ${route === 1 ? 'current' : ''}`" @click="goTo(1)">Paramètres</button>
      <button :class="`page-link ${route === 2 ? 'current' : ''}`" @click="goTo(2)">Suggestion</button>
      <button :class="`page-link ${route === 3 ? 'current' : ''}`" @click="goTo(3)">Remplacement</button>
      <button :class="`page-link ${route === 4 ? 'current' : ''}`" @click="goTo(4)">Wine Pairing</button>
      <button :class="`page-link ${route === 5 ? 'current' : ''}`" @click="goTo(5)">Recipe Pairing</button>
    </div>
  </div>
  <RecipeByIngredients v-if="route === 0"/>
  <RecipeByParam v-else-if="route === 1"/>
  <RecipeSuggestion v-else-if="route === 2"/>
  <RecipeReplacement v-else-if="route === 3"/>
  <RecipeToPredictWine v-else-if="route === 4"/>
  <WineToPredictRecipe v-else-if="route === 5"/>
</template>

<script>
import RecipeByParam from "./components/pages/RecipeByParam.vue";
import RecipeByIngredients from "./components/pages/RecipeByIngredients.vue";
import RecipeSuggestion from "./components/pages/RecipeSuggestion.vue";
import RecipeReplacement from "./components/pages/RecipeReplacement.vue";
import RecipeToPredictWine from "./components/pages/RecipeToPredictWine.vue";
import WineToPredictRecipe from "./components/pages/WineToPredictRecipe.vue";

export default {
  name: 'App',
  components: {
    WineToPredictRecipe,
    RecipeToPredictWine,
    RecipeReplacement,
    RecipeSuggestion,
    RecipeByIngredients,
    RecipeByParam,
  },
  data: () => ({
    route: 0
  }),
  methods: {
    goTo(i) {
      this.route = i;
    }
  }
};
</script>

<style scoped>
.page-link {
  @apply cursor-pointer font-light text-blue-500;
}

.page-link.current {
  @apply underline;
}
</style>
