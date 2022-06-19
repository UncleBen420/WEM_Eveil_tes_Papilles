<template>
  <div class="flex flex-col border rounded-xl p-4 gap-4">
    <h2>{{ recipe.title }}</h2>
    <div class="flex">
      <div class="flex flex-col gap-2 w-2/5">
        <img :src="recipe.image_link" alt="recipe image" class="rounded-xl"/>
      </div>

      <div class="flex-1 ml-8">
        <h3>Ingrédients ({{ recipe.nb_people }} personne{{ plural(recipe.nb_people) }})</h3>
        <ul class="list-disc ml-4">
          <li class="ml-4" v-for="ingredient in recipe.ingredients">
            <span class="underline">{{ ingredient.ingredient }}</span>
            <span>: {{ ingredient.quantity }} {{ ingredient.unit }}</span>
          </li>
        </ul>
      </div>
    </div>
    <div>
      <h3>Préparation ({{ recipe.duration }} minute)</h3>
      <p>{{ recipe.steps }}</p>
    </div>
    <div class="flex justify-between">
      <p>Score: {{recipe.score}}</p>
      <a :href="recipe.link" target="_blank" class="text-blue-500 text-sm lowercase">Plus d'infos</a>
    </div>
  </div>
</template>

<script>
export default {
  name: "Recipe",
  props: {
    recipe: {required: true},
  },
  methods: {
    capitalize(str) {
      if (!str) return '';
      return str?.substr(0, 1).toUpperCase() + str.substr(1);
    },
    plural(value) {
      return value > 0 ? 's' : '';
    },
  },
};
</script>
