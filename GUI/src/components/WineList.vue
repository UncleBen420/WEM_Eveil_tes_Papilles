<template>
  <div class="flex flex flex-wrap -m-4">
    <div v-for="wine in wines" class="w-full lg:w-1/2 xl:w-1/3 p-4">
      <Wine :wine="wine.recipes"/>
    </div>
  </div>
</template>

<script>
import Wine from "./Wine.vue"

export default {
  name: 'WineList',
  components: {Wine},
  props: {
    wines: {required: true}
  }
}
</script>
