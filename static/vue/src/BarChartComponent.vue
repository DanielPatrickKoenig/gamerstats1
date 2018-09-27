<template>
  <div class="bar-chart">
    <div v-bind:id="chartid"></div>
  </div>
</template>
<script>
  import echarts from 'echarts'
  export default {
    data () {
      return {
        chartid: 'CHART_' + Math.random().toString().split('.').join('') + Math.random().toString().split('.').join('') + Math.random().toString().split('.').join(''),
        chartObject: undefined
      }
    },
    props: ['chartdata', 'colors', 'textcolor', 'title'],
    watch: {
      chartdata: function () {
        var self = this
        if (document.getElementById(self.$data.chartid) !== undefined) {
          var _legendData = []
          var _xData = []
          var _series = []
          for (var c in this.chartdata) {
            _xData.push(c)
            if (_legendData.length === 0) {
              for (var leg in this.chartdata[c]) {
                _legendData.push(leg)
                _series.push({name: leg, type: 'bar', gap: 0, label: '', data: []})
              }
            }
          }

          for (var i = 0; i < _xData.length; i++) {
            for (var j = 0; j < _legendData.length; j++) {
              _series[j].data.push(this.chartdata[_xData[i]][_legendData[j]])
            }
          }
          var option = {
            title: {
              text: this.title,
              textStyle: {
                color: this.textcolor
              }
            },
            color: this.colors,
            tooltip: {
              trigger: 'axis',
              axisPointer: {
                type: 'shadow'
              }
            },
            legend: {
              data: _legendData,
              textStyle: {
                color: this.textcolor
              }
            },
            textStyle: {
              color: this.textcolor
            },
            toolbox: {
              show: true,
              orient: 'vertical',
              left: 'right',
              top: 'center'
            },
            calculable: true,
            xAxis: [
              {
                type: 'category',
                axisTick: {show: false},
                data: _xData
              }
            ],
            yAxis: [
              {
                type: 'value'
              }
            ],
            series: _series
          }
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
