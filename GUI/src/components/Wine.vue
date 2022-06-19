<template>
  <div class="flex flex-col border rounded-xl p-4 gap-4">
    <div>
      <h2>{{ wine.title }}</h2>
      <p>Variété de grappe: {{ capitalize(wine.grape_variety) }}</p>
      <p>Pays: {{ capitalize(wine.country) }}</p>
    </div>
    <div>
      <h3>Description</h3>
      <p>{{ wine.description }}</p>
    </div>

    <div>
      <h3>S'accorde bien avec:</h3>
      <ul class="list-disc ml-4">
        <li class="ml-4" v-for="ingredient in wine.pairsWellWith">
          {{ ingredient.terms }}
        </li>
      </ul>
    </div>

    <div class="flex justify-end">
      <a :href="wine.link" target="_blank" class="text-blue-500 text-sm lowercase">Plus d'infos</a>
    </div>
  </div>
</template>

<script>
export default {
  name: "Recipe",
  props: {
    wine: {required: true},
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
