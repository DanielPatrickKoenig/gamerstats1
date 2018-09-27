<template>
  <div id="app">
    <div class='main-header'>
      <label>
        Video Game Sales
        <!-- <ul><li class="gaming-simabout">About</li><li class="gaming-simoptions">Options</li><li class="gaming-simhelp">Help</li></ul> -->
      </label>
    </div>
    <div class="charts">
      <barChart :chartdata="comparisondata" :colors="chartColors" :textcolor="chartTextColor" title="Regional Sales"></barChart>
      <div class="rating-charts">
        <!-- <label class="ratings-title" v-text="Object.keys(ratings).length === 0 ? '' : 'Critic Ratings'"></label> -->
        <div slot="userinterface">
          <searchText :choices="checkChoices" :list="searchableContentFiltered" :exclusions="getExcludeList(selectedTags)" searchprompt="Search by game, system, producer or genre">
            <checkAll :choices="checkChoices" slot="filters">
          </checkAll>
          </searchText>
          <tagList v-if="selectedTags.length > 0" :tags="selectedTags">
            <svg class="rating-art" v-for="(s, i) in selectedTags" :key="'tag_'+i.toString()" :slot="'content_'+i.toString()">
              <defs>
                <clipPath :id="'mask_'+i.toString()">
                  <path xmlns="http://www.w3.org/2000/svg" :d="starsPath" fill="transparent" />
                </clipPath>
              </defs>
              <path xmlns="http://www.w3.org/2000/svg" :d="starsPath" />
              <rect :clip-path="'url(#mask_'+i.toString()+')'" xmlns="http://www.w3.org/2000/svg" x="0" y="0" :width="120*(ratings[s.text].Critic_Score/100)" height="24"></rect>
            </svg>
          </tagList>
          <label :class="shouldShowShortcuts ? 'favorites-icon open' : 'favorites-icon'" for="tag_favorites"></label>
          <input type="checkbox" v-model="shouldShowShortcuts" id="tag_favorites" />
          <ul v-if="shouldShowShortcuts" class="shortcuts-list">
            <li v-for="(s, k, i) in shortcuts" :key="'shortcut_'+i.toString()" v-on:click="doShortCut" :shortcut="k">
              <a>{{s.label}}</a>
            </li>
          </ul>
        </div>
        <!-- <ratingChart v-for="(r, k, i) in ratings" :key="i" v-bind:chartdata="r.Critic_Score !== undefined ? r.Critic_Score : 0" v-bind:color="chartColors[0]" v-bind:text="k" v-bind:total="100"></ratingChart> -->
      </div>
      <pieChart :chartdata="salesdata" :colors="chartColors" :textcolor="chartTextColor" title=" Sales by Genre" hovertitle='Global Sales'></pieChart>
    </div>
    <!-- <uiDrawer>
      <span slot="titletext">FILTERS</span>
      <div slot="userinterface">
        <checkAll :choices="checkChoices"></checkAll>
        <searchText :choices="checkChoices" :list="searchableContentFiltered" :exclusions="getExcludeList(selectedTags)"></searchText>
        <tagList :tags="selectedTags"></tagList>
      </div>
    </uiDrawer> -->
  </div>
</template>

<script>
import {EventBus} from './EventBus.js'
import PiehartComponent from './PieChartComponent.vue'
import BarhartComponent from './BarChartComponent.vue'
import RatingChartComponent from './RatingChartComponent.vue'
import uiDrawerComponent from './UIDrawerComponent.vue'
import CheckAllComponent from './CheckAllComponent.vue'
import SearchTextComponent from './SearchTextComponent.vue'
import TagListComponent from './TagListComponent.vue'
import axios from 'axios'
export default {
  name: 'app',
  components: {
    pieChart: PiehartComponent,
    barChart: BarhartComponent,
    ratingChart: RatingChartComponent,
    uiDrawer: uiDrawerComponent,
    checkAll: CheckAllComponent,
    searchText: SearchTextComponent,
    tagList: TagListComponent
  },
  data () {
    return {
      msg: 'Welcome to Your Vue.js App',
      chartColors: ['#00aeef', '#fdc689', '#7cc576', '#f26d7d', '#a186be', '#ec008c', '#c69c6d', '#ed145b', '#f26522', '#acd373', '#aba000', '#f5989d'],
      chartTextColor: '#eeeeee',
      checkChoices: [
        {text: 'Genres', value: 'genre', selected: true, cssClass: 'gaming-simgenre'},
        {text: 'Systems', value: 'system', selected: true, cssClass: 'gaming-simsystem'},
        {text: 'Publishers', value: 'publisher', selected: true, cssClass: 'gaming-simpublisher'},
        {text: 'Games', value: 'game', selected: true, cssClass: 'gaming-simgame'}
      ],
      searchableContent: {},
      searchableContentFiltered: {},
      searchExclusions: [],
      selectedTags: [],
      salesdata: {},
      yeardata: {},
      comparisondata: {},
      ratings: {},
      starsPath: 'M 11.037 0 l 3.411 6.911 l 7.625 1.108 l -5.518 5.379 l 1.303 7.594 l -6.821 -3.585 l -6.821 3.585 l 1.303 -7.594 L 0 8.019 l 7.626 -1.108 L 11.037 0 Z M 32.088 6.911 l -7.625 1.108 l 5.518 5.379 l -1.302 7.594 l 6.82 -3.585 l 6.821 3.585 l -1.303 -7.594 l 5.518 -5.379 l -7.626 -1.108 L 35.498 0 L 32.088 6.911 Z M 56.55 6.911 l -7.626 1.108 l 5.519 5.379 l -1.303 7.594 l 6.821 -3.585 l 6.82 3.585 l -1.302 -7.594 l 5.518 -5.379 l -7.626 -1.108 L 59.96 0 L 56.55 6.911 Z M 81.012 6.911 l -7.627 1.108 l 5.52 5.379 l -1.304 7.594 l 6.821 -3.585 l 6.82 3.585 l -1.303 -7.594 l 5.518 -5.379 l -7.625 -1.108 L 84.423 0 L 81.012 6.911 Z M 105.474 6.911 l -7.627 1.108 l 5.519 5.379 l -1.302 7.594 l 6.82 -3.585 l 6.821 3.585 l -1.304 -7.594 l 5.52 -5.379 l -7.626 -1.108 L 108.884 0 L 105.474 6.911 Z',
      shouldShowShortcuts: false,
      shortcuts: {
        NONE: {
          label: 'Everything',
          tags: []
        },
        NINTENDO_SYSTEMS: {
          label: 'Nintendo Consoles',
          tags: [{type: 'system', text: 'SNES'}, {type: 'system', text: 'NES'}, {type: 'system', text: 'N64'}, {type: 'system', text: 'GC'}]
        },
        PUBLISHING_GIANTS: {
          label: 'Publishing Giants',
          tags: [{type: 'publisher', text: 'Konami Digital Entertainment'}, {type: 'publisher', text: 'Capcom'}, {type: 'publisher', text: 'Acclaim Entertainment'}, {type: 'publisher', text: 'Namco Bandai Games'}]
        },
        NES_VS_MARIO: {
          label: 'All of NES vs Super Mario Bros.',
          tags: [{type: 'system', text: 'NES'}, {type: 'game', text: 'Super Mario Bros.'}]
        },
        N64_VS_GOLDENEYE: {
          label: 'All of N64 vs GoldenEye',
          tags: [{type: 'system', text: 'N64'}, {type: 'game', text: 'GoldenEye 007'}]
        },
        HANDHELDS: {
          label: 'Hand Helds',
          tags: [{type: 'system', text: 'PSP'}, {type: 'system', text: 'GB'}, {type: 'system', text: 'GBA'}, {type: 'system', text: 'DS'}, {type: 'system', text: '3DS'}]
        },
        MASS_EFFECT: {
          label: 'Mass Effect Series',
          tags: [{type: 'game', text: 'Mass Effect'}, {type: 'game', text: 'Mass Effect 2'}, {type: 'game', text: 'Mass Effect 3'}]
        },
        FIGHTING_CLASSICS: {
          label: 'Fighting Classics',
          tags: [{type: 'game', text: 'Mortal Kombat'}, {type: 'game', text: 'Killer Instinct'}, {type: 'game', text: 'Tekken'}, {type: 'game', text: 'Super Street Fighter II'}]
        },
        ALL_FIGHTING_VS_MORTAL_KOMBAT: {
          label: 'Fighting vs Mortal Kombat',
          tags: [{type: 'game', text: 'Mortal Kombat'}, {type: 'genre', text: 'Fighting'}]
        },
        ALL_PUZZLE_VS_TETRIS: {
          label: 'Puzzle vs Tetris',
          tags: [{type: 'game', text: 'Tetris'}, {type: 'genre', text: 'Puzzle'}]
        }
      },
      onUpdateSim: function (d) {
        var splitter = ':::'
        var _params = {}
        for (var i = 0; i < d.selectedTags.length; i++) {
          if (_params[d.selectedTags[i].type] === undefined) {
            _params[d.selectedTags[i].type] = []
          }
          _params[d.selectedTags[i].type].push(d.selectedTags[i].text)
        }
        var params = {splitter: splitter}
        for (var p in _params) {
          params[p] = _params[p].join(splitter)
        }
        console.log(params)
        axios.get('/gamerstats1/default/update', {params: params}).then(response => {
          var dta = response.data
          d.salesdata = dta.sales
          d.yeardata = dta.years
          d.comparisondata = dta.subset
          d.ratings = dta.ratings
          console.log(d.ratings)
        })
      }
    }
  },
  methods: {
    getExcludeList: function (el) {
      var outList = []
      for (var i = 0; i < el.length; i++) {
        outList.push(el[i].text)
      }
      return outList
    },
    doShortCut: function (e) {
      var self = this
      var shortcutKey = e.currentTarget.getAttribute('shortcut')
      console.log(shortcutKey)
      for (var s in self.$data.shortcuts) {
        if (s === shortcutKey) {
          self.$data.selectedTags = []
          for (var i = 0; i < self.$data.shortcuts[s].tags.length; i++) {
            self.addTag(self.$data.shortcuts[s].tags[i])
          }
          // self.$data.selectedTags = self.$data.shortcuts[s].tags
          self.$data.onUpdateSim(self.$data)
        }
      }
      self.$data.shouldShowShortcuts = false
    },
    addTag: function (t) {
      var self = this
      self.$data.selectedTags.push(t)
    }
  },
  created () {
    var self = this
    EventBus.$on('check-all-option-checked', (n) => {
      self.$data.searchableContentFiltered = {}
      for (var s in self.$data.searchableContent) {
        var isEnabled = false
        for (var i = 0; i < self.$data.checkChoices.length; i++) {
          if (self.$data.checkChoices[i].value === s && self.$data.checkChoices[i].selected) {
            isEnabled = true
          }
        }
        if (isEnabled) {
          self.$data.searchableContentFiltered[s] = self.$data.searchableContent[s]
        }
      }
    })
    EventBus.$on('search-term-clicked', (n) => {
      self.addTag({type: n.getAttribute('class'), text: n.innerHTML})
      self.$data.onUpdateSim(self.$data)
    })
    EventBus.$on('tag-deleted-clicked', (n) => {
      self.$data.selectedTags.splice(Number(n.getAttribute('tag-index')), 1)
      self.$data.onUpdateSim(self.$data)
    })

    axios.get('/gamerstats1/default/data').then(response => {
      var dta = response.data
      var game = dta.namelist
      var genre = dta.genrelist
      var system = dta.systemlist
      var publisher = dta.publisherlist
      self.$data.searchableContent = {genre: genre, system: system, publisher: publisher, game: game}
      self.$data.searchableContentFiltered = {genre: genre, system: system, publisher: publisher, game: game}

      self.$data.onUpdateSim(self.$data)
    })
  }
}
</script>

<style lang="scss">

$genreColor: #9e0039;
$systemColor: #406618;
$publisherColor: #0054a6;
$gameColor: #8c6239;
$bodyBackground: url('assets/bgImage.png');
$textColor: #ffffff;
$uiBackground: rgba(222,243,226,.9);
$chartTitleTextColor: #eeeeee;
$drawerOpenedHeight: 400px;
$drawerClosedHeight: 40px;
$drawerSpeed:.5s;

#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
body {
  background-color: #000000;
  padding: 0;
  margin: 0;
  background-image: $bodyBackground;
  background-position: center;
  background-size: cover;
}
div#main{
  /* max-width:1200px; */
  width:100%;
  /* margin:0 auto; */
    
}
div.search-text,
ul.tag-list{
  float:left;
}
div.search-text{
  max-width:780px;
  width:100%;
  position:relative;
  margin:0 10px;
  z-index:20;
  clear:left;
  margin-top:-5px;
  > input[type='text']{
    display:block;
    width:92%;
    max-width:770px;
    height:30px;
    font-size:12px;
    font-weight:bold;
    border:none;
    border-radius:68px;
    box-shadow: 0 0 4px #0afff1 inset;
    padding:0 12px;
    background-color: rgba(0,0,0,.5);
    color: #0afff1;
    outline: none;
  }
  > ul:not(.check-all){
    position:absolute;
    max-height:300px;
    overflow:auto;
    width:60%;
    margin:0;
    padding:0;
    > li{
      color:$textColor;
      padding:4px;
      margin:2px 0;
      font-family:Arial;
      font-weight:bold;
      font-size:12px;
      text-align: left;
      padding-left:25px;
    }
  }
}

div.search-text > ul > li,
ul.check-all > li{
  display:block;
}

ul.tag-list{
  width:35%;
  float: right;
  > li {
    display:block;
    float:left;
    padding:1px 8px 3px 8px;
    background-color:transparent;
    border-radius:0px;
    margin:2px;
    color:$textColor;
    width: 92%;

    > span:first-child{
      font-family: Arial;
      font-weight: 700;
      font-size: 12px;
      padding-left: 22px;
      padding-top: 1px;
      display: inline-block;
      max-width: 170px;
    }

    > span:not(:first-child){
      display: inline-block;
      background-color: transparent;
      color: #ff0000;
      border-radius: 20px;
      width: 15px;
      height: 16px;
      font-size: 10px !important;
      margin-right: -4px;
      margin-top: -1px !important;
      text-align:center;
      cursor:pointer;
      float:right;
    }

    > span:not(:first-child)::before{
      content:'\2716';
      text-align: center;
    }
  } 
}

ul.tag-list > li{
  background-size: 27px 27px;
  box-shadow:0 1px 0 rgba(10,241,255,.3);
}

ul.check-all > li{
  background-size: 24px 24px;
}

div.search-text ul:not(.check-all) > li{
  background-size: 22px 22px;
  box-shadow:0 1px 0 rgba(10,241,255,.3);
}

ul.tag-list,
ul.check-all,
div.search-text ul{
  overflow-x: hidden;
  >li {
    background-position: 1px 1px;
    background-repeat: no-repeat;
  }
  /*
  > li.genre{
    background-color:$genreColor;
  }
  > li.system{
    background-color:$systemColor;
  }
  > li.publisher{
    background-color:$publisherColor;
  }
  > li.game{
    background-color:$gameColor;
  }
  */
}

ul.check-all,
ul.tag-list{
    margin:0;
    padding:0;
}


div.pie-chart,
div.line-chart,
div.bar-chart{
  display:inline;
  float: right;
}
div.pie-chart > div{
  width:500px;
  height:400px;
}

div.line-chart > div,
div.bar-chart > div{
  width:1200px;
  height:300px;
  box-shadow: 0 -1px 0 rgba(255,255,255,.2) inset; 
  margin-bottom:4px;
}

div.charts{
  max-width:1200px;
  
  position:relative;
  max-width:1200px;
  width:100%;
  margin:0 auto;
}

div.ui-drawer{
  position: fixed;
  width: 100%;
  bottom: 0;
  left:0;
  background-color:$uiBackground;
  input[type='checkbox']{
    display:none;
  }
  > label.open-toggle{
    width: 100%;
    display: block;
    text-align: center;
    height:30px;
    padding-top:8px;
    background-color:rgba(0,0,0,.2);
    + div{
      margin:0 auto;
      max-width:1200px;
      width:100%;
    }
  }
  > label > span{
    margin:0 10px;
    font-size:14px;
    font-family:Arial;
  }
}

@keyframes opened {
  from {height: $drawerClosedHeight;}
  to {height: $drawerOpenedHeight;}
}

div.ui-drawer.open{
  height: $drawerOpenedHeight;
  animation-name: opened;
  animation-duration: $drawerSpeed;
  > label::after{
    content:'\21E3';
    font-size:25px;
  }
  > label::before{
    content:'\21E3';
    font-size:25px;
  }
}

@keyframes closed {
  from {height: $drawerOpenedHeight;}
  to {height: $drawerClosedHeight;}
}

div.ui-drawer:not(.open){
  height: $drawerClosedHeight;
  animation-name: closed;
  animation-duration: $drawerSpeed;
  > label::after{
    content:'\21E1';
    font-size:25px;
  }
  > label::before{
    content:'\21E1';
    font-size:25px;
  }
}

ul.check-all{
  width:100%;
  height:40px;
  padding-left:10px;
  > li:first-child{
    border-radius:50px 0 0 50px;
  }
  > li:last-child{
    border-radius:0 50px 50px 0;
  }
  > li:not(:last-child){
    box-shadow:-9px 0 0 #000000 inset, -10px 0 0 rgba(10,255,241,.4) inset;
  }
  > li{
    float:left;
    margin-top:4px;   
    width:104px; 
    color:$textColor;
    font-family:Arial;
    font-weight:bold;
    text-align:left;
    padding:5px 0;
    font-size:12px;
    input[type='checkbox']{
      display:none;
    }
    > label {
      padding-left: 28px;
    }
  }
}

ul.tag-list{
  max-height: 340px;
  position: absolute;
  width: 245px;
  z-index: 100;
  right: 0;
  overflow-y: auto;
  top: 33px;
  min-height: 340px;
  box-shadow: -1px 0 0 rgba(10,241,255,.3)
}

div.rating-charts{
  width:700px;
  display: inline-block;
  text-align: left;
  margin-top:12px;
  position: relative;
  height:374px;
  box-shadow: 1px 0 0 rgba(10,241,255,.3);
  > div.rating-chart{
    margin: 6px 0;
    border-radius: 0 20px 20px 0;
    overflow: hidden;
    width: 100%;
    height: 30px;
    background-color: #cccccc;
    span{
      display:block;
      padding:9px;
      font-family:Arial;
      font-size:11px;
    }
  }
}

label.ratings-title{
  color:$chartTitleTextColor;
  font-family:Arial;
  font-size:18px;
  font-weight:bold;
}

div.main-header{
  width:100%;
  text-align:center;
  font-size:22px;
  font-family:Arial;
  font-weight:bold;
  background-color:rgba(255,255,255,.4);
  color:#000000;
  padding:10px 0;
  margin-bottom:10px;
  > label {
    max-width:1200px;
    margin: 0 auto;
    display:block;
    text-align: left;
    > ul{
      float: right;
      display: block;
      padding: 0;
      margin: 0 auto;
      > li{
        float: left;
        margin: 0 8px;
        display:block;
        font-size: 14px;
        color: #bdf610;
      }
    }
  }
}
svg.rating-art{
  width: 196px;
  height: 24px;
  margin-left: 22px;
  margin-top: 2px;
  path{
    fill:rgba(255,255,255,.2);
  }
  rect{
    fill:#eeda00;
    stroke: transparent;
  }
}
li.genre{ 
  background-image: url("/gamerstats1/static/vue/src/assets/genre.svg");
}
li.system{
  background-image: url("/gamerstats1/static/vue/src/assets/system.svg");
}
li.publisher{
  background-image: url("/gamerstats1/static/vue/src/assets/publisher.svg");
}
li.game{
  background-image: url("/gamerstats1/static/vue/src/assets/game.svg");
}
label.favorites-icon{
  color: #0afff1;
  display: inline-block;
  float: right;
  font-size: 17px;
  text-align: center;
  position: absolute;
  right: 10px;
  top: -2px;
  width: 24px;
  height: 24px;
  border-radius: 50px;
  box-shadow: 0 0 0 1px #0afff1;
  cursor: pointer;
  z-index: 101;
}
label.favorites-icon.open{
  color:#000000;
  background-color: #0afff1;
}
label.favorites-icon::before{
  content: "\2605";
  
}

label.favorites-icon + input[type='checkbox']{
  display: none;
}

ul.shortcuts-list{
  position: absolute;
  right: 0;
  top: 26px;
  width: 200px;
  display: block;
  z-index: 102;
  max-height: 300px;
  background-color: rgba(50,50,50,.9);
  overflow-y: auto;
  padding: 0;
  margin: 0;
  > li{
    display: block;
    float: none;
    clear: both;
    padding: 3px 4px;
    margin: 4px;
    background-color: #0afff1;
    color: #000;
    cursor: pointer;
    font-size: 11px;
    border-radius: 6px;
    opacity: .7;
    > a{
      color: #000000;
      text-decoration: none;
    }
  }
  > li:hover{
    opacity: 1;
  }
}

@font-face {
  font-family: "gameing-simulator";  
  src:  url("/gamerstats1/static/src/vue/assets/fonts/gameing-simulator.eot?qhfh8m");  
  src:  url("/gamerstats1/static/src/vue/assets/fonts/gameing-simulator.eot?qhfh8m#iefix") format("embedded-opentype"),
  url("/gamerstats1/static/src/vue/assets/fonts/gameing-simulator.ttf?qhfh8m") format("truetype"),
  url("/gamerstats1/static/src/vue/assets/fonts/gameing-simulator.woff?qhfh8m") format("woff"),
  url("/gamerstats1/static/src/vue/assets/fonts/gameing-simulator.svg?qhfh8m#gameing-simulator") format("svg");
  font-weight: normal;
  font-style: normal;
}
[class^="gaming-sim"], 
[class*=" gaming-sim"] {  
  /* use !important to prevent issues with browser extensions that change fonts */  
  font-family: "gameing-simulator" !important;
  speak: none;
  font-style: normal;
  font-weight: normal;
  font-variant: normal;
  text-transform: none;
  line-height: 1;
    /* Better Font Rendering =========== */  
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
.gaming-simabout:before {  content: "\e900";}.gaming-simgame:before {  content: "\e901";}.gaming-simgenre:before {  content: "\e902";}.gaming-simhelp:before {  content: "\e903";}.gaming-simoptions:before {  content: "\e904";}.gaming-simpublisher:before {  content: "\e905";}.gaming-simsystem:before {  content: "\e906";}
</style>
