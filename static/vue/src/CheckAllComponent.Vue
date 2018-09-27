<template>
  <ul class="check-all">
    <li v-for="(c, i, k) in choices" :key="k" v-bind:class="c.value" v-bind:style="c.selected ? '' : 'opacity:.5;'">
      <label style="width:100%; display:block;">
        <input type="checkbox" v-model="c.selected" v-bind:value="c.value" v-on:change="onCheckChange" />
        <slot name="'choice_'+i.toString()">
          <span v-text="c.text">
            
          </span>
        </slot>
      </label>
    </li>
  </ul>
</template>
<script>
  import {EventBus} from './EventBus.js'
  export default {
    name: 'check-all',
    props: ['choices'],
    data () {
      return {
      }
    },
    methods: {
      onCheckChange: function (e) {
        EventBus.$emit('check-all-option-checked', e.currentTarget)
      }
    }
  }
</script>
<style>
</style>
