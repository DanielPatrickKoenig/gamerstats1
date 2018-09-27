<template>
  <div class='search-text'>
    <input type="text" v-on:keyup="onTextEntered" v-model="searchTerm" :placeholder="searchprompt" />
    <slot name="filters" v-if="searchTerm !== ''"></slot>
    <ul>
      <li v-for="(m,i) in matches" :key="i" v-text="m.text" v-bind:match-index="i" v-bind:class="m.listIndex" v-on:click="onSearchTermClicked"></li>
    </ul>
  </div>
</template>
<script>
  import {EventBus} from './EventBus.js'
  export default {
    data () {
      return {
        searchTerm: '',
        matches: []
      }
    },
    props: ['list', 'exclusions', 'searchprompt'],
    methods: {
      onSearchTermClicked: function (e) {
        EventBus.$emit('search-term-clicked', e.currentTarget)
      },
      onTextEntered: function (e) {
        var containsValue = function (list, val) {
          var con = false
          for (var i = 0; i < list.length; i++) {
            if (list[i] === val) {
              con = true
            }
          }
          return con
        }
        var self = this
        var matches = []
        if (self.$data.searchTerm !== '') {
          for (var n in this.list) {
            for (var i = 0; i < this.list[n].length; i++) {
              if (this.list[n][i].toLowerCase().split(self.$data.searchTerm.toLowerCase()).length > 1 && !containsValue(this.exclusions, this.list[n][i])) {
                matches.push({text: this.list[n][i], listIndex: n})
              }
            }
          }
        }
        self.$data.matches = matches
      }
    },
    watch: {
      list: function () {
        var self = this
        self.onTextEntered()
      }
    }
  }
</script>
<style>
</style>
