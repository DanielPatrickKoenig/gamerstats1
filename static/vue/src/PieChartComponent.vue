<template>
  <div class="pie-chart">
    <div v-bind:id="chartid"></div>
  </div>
</template>
<script>
  import echarts from 'echarts'
  export default {
    data () {
      return {
        message: 'sup dude',
        chartid: 'CHART_' + Math.random().toString().split('.').join('') + Math.random().toString().split('.').join('') + Math.random().toString().split('.').join(''),
        chartObject: undefined
      }
    },
    props: ['chartdata', 'colors', 'textcolor', 'title', 'hovertitle'],
    watch: {
      chartdata: function () {
        var self = this
        if (document.getElementById(self.$data.chartid) !== undefined) {
          var _data = []
          var _values = []
          var _keys = []
          console.log(this.chartdata)
          for (var k in this.chartdata) {
            _keys.push(k)
            _values.push(this.chartdata[k])
            _data.push({name: k, value: this.chartdata[k]})
          }
          var option = {
            title: {
              text: this.title,
              textStyle: {
                color: this.textcolor
              },
              x: 'left'
            },
            color: this.colors,
            tooltip: {
              trigger: 'item',
              formatter: '{a} <br/>{b}: {c} ({d}%)'
            },
            // legend: {
            //   orient: 'vertical',
            //   x: 'left',
            //   y: 'center',
            //   data: _keys,
            //   textStyle: {
            //     color: this.textcolor
            //   }
            // },
            series: [
              {
                name: this.hovertitle,
                type: 'pie',
                radius: ['50%', '70%'],
                selectedMode: 'single',
                clockwise: true,
                label: {
                  normal: {
                    textStyle: {
                      fontSize: 12,
                      color: '#eeeeee'
                    }
                  }
                },
                labelLine: {
                  normal: {
                    lineStyle: {
                      color: '#eeeeee'
                    }
                  }
                },
                data: _data
              }
            ]
          }
          console.log(self.$data.chartObject)
          self.$data.chartObject.setOption(option)
        }
      }
    },
    mounted: function () {
      var self = this
      self.$data.chartObject = echarts.init(document.getElementById(self.$data.chartid))
    }
  }
</script>
