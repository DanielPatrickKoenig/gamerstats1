<template>
  <div v-bind:class="open ? 'ui-drawer open' : 'ui-drawer'">
    <label class="open-toggle">
      <input type="checkbox" v-model="open"/>
      <slot name="titletext"></slot>
    </label>
    <slot name="userinterface"></slot>
  </div>
</template>
<script>
export default {
  data () {
    return {
      open: false
    }
  }
}
</script>

