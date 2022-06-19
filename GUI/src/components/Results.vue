<template>
  <div v-if="results || loading">
    <h1>Résultats</h1>
    <div v-if="loading">Loading ...</div>
    <slot v-else-if="results.length"/>
    <div v-else>Aucuns résulats trouvés.</div>
  </div>
</template>

<script>
export default {
  name: 'Results',
  props: {
    loading: { required: true},
    results: { default: null}
  }
}
</script>
