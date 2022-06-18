<template>
  <div class="flex flex flex-wrap -m-4">
    <div v-for="recipe in recipes" class="w-full lg:w-1/2 xl:w-1/3 p-4">
      <Recipe :recipe="recipe.recipes"></Recipe>
    </div>
  </div>
</template>

<script>
import Recipe from "./Recipe.vue"

export default {
  name: 'RecipeList',
  components: {Recipe},
  props: {
    recipes: {required: true}
  }
}
</script>
