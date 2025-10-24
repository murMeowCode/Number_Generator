<template>
  <div class="line-chart">
    <div class="chart-header">
      <h4>{{ title }}</h4>
      <div class="chart-legend" v-if="data.datasets && data.datasets.length">
        <div v-for="dataset in data.datasets" :key="dataset.label" class="legend-item">
          <span
            class="legend-color"
            :style="{
              backgroundColor: dataset.borderColor,
              border: dataset.borderDash ? '2px dashed ' + dataset.borderColor : 'none',
            }"
          ></span>
          <span class="legend-label">{{ dataset.label }}</span>
        </div>
      </div>
    </div>
    <div class="chart-container">
      <canvas ref="chartRef" :width="width" :height="height"></canvas>
    </div>
    <div class="chart-footer" v-if="footerText">
      {{ footerText }}
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch, onUnmounted } from 'vue'

export default {
  name: 'LineChart',
  props: {
    data: {
      type: Object,
      default: () => ({}),
    },
    title: {
      type: String,
      default: 'Line Chart',
    },
    width: {
      type: Number,
      default: 400,
    },
    height: {
      type: Number,
      default: 200,
    },
    footerText: String,
  },
  setup(props) {
    const chartRef = ref(null)
    let chartInstance = null

    const defaultData = {
      labels: ['10:00', '11:00', '12:00', '13:00', '14:00', '15:00'],
      datasets: [
        {
          label: 'Seed значения',
          data: [0.005, 0.006, 0.007, 0.008, 0.009, 0.01],
          borderColor: '#4299e1',
          backgroundColor: 'rgba(66, 153, 225, 0.1)',
          borderWidth: 2,
          tension: 0.4,
          fill: true,
          pointBackgroundColor: '#4299e1',
          pointBorderColor: '#ffffff',
          pointBorderWidth: 2,
          pointRadius: 4,
          pointHoverRadius: 6,
        },
        {
          label: 'Математическое ожидание',
          data: [0.0075, 0.0075, 0.0075, 0.0075, 0.0075, 0.0075],
          borderColor: '#e53e3e',
          backgroundColor: 'transparent',
          borderWidth: 2,
          borderDash: [5, 5],
          tension: 0,
          fill: false,
          pointRadius: 0,
        },
      ],
    }

    const renderChart = async () => {
      if (!chartRef.value) return

      const { Chart } = await import('chart.js/auto')

      if (chartInstance) {
        chartInstance.destroy()
      }

      const ctx = chartRef.value.getContext('2d')

      // Используем данные из props или дефолтные
      const chartData = props.data.datasets ? props.data : defaultData

      console.log('📊 LineChart данные:', props.data.datasets)

      chartInstance = new Chart(ctx, {
        type: 'line',
        data: chartData,
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              display: false, // Скрываем стандартную легенду, используем кастомную
            },
            tooltip: {
              mode: 'index',
              intersect: false,
              callbacks: {
                label: function (context) {
                  let label = context.dataset.label || ''
                  if (label) {
                    label += ': '
                  }
                  if (context.parsed.y !== null) {
                    label += context.parsed.y.toFixed(6)
                  }
                  return label
                },
              },
            },
          },
          scales: {
            y: {
              beginAtZero: false,
              grid: {
                color: 'rgba(0, 0, 0, 0.1)',
              },
              ticks: {
                callback: function (value) {
                  return value.toFixed(4)
                },
              },
              title: {
                display: true,
                text: 'Seed значение',
              },
            },
            x: {
              grid: {
                display: false,
              },
              title: {
                display: true,
                text: 'Время',
              },
            },
          },
          interaction: {
            mode: 'nearest',
            axis: 'x',
            intersect: false,
          },
          elements: {
            line: {
              tension: 0.4,
            },
          },
        },
      })
    }

    onMounted(() => {
      renderChart()
    })

    watch(
      () => props.data,
      () => {
        if (chartInstance) {
          chartInstance.destroy()
        }
        renderChart()
      },
      { deep: true },
    )

    onUnmounted(() => {
      if (chartInstance) {
        chartInstance.destroy()
      }
    })

    return {
      chartRef,
    }
  },
}
</script>

<style scoped>
.line-chart {
  background: var(--color-bg-elevated);
  border-radius: 8px;
  padding: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  border: 1px solid #e2e8f0;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  flex-wrap: wrap;
  gap: 12px;
}

.chart-header h4 {
  margin: 0;
  color: var(--color-text);
  font-size: 16px;
  font-weight: 600;
}

.chart-legend {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 6px;
}

.legend-color {
  width: 16px;
  height: 3px;
  border-radius: 2px;
  display: block;
}

.legend-label {
  font-size: 12px;
  color: #718096;
  font-weight: 500;
}

.chart-container {
  position: relative;
  height: 300px;
}

.chart-footer {
  margin-top: 12px;
  font-size: 12px;
  color: #718096;
  text-align: center;
  font-style: italic;
  padding: 8px;
  background-color: #f7fafc;
  border-radius: 4px;
}

/* Адаптивность */
@media (max-width: 768px) {
  .chart-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .chart-legend {
    justify-content: flex-start;
  }

  .line-chart {
    padding: 12px;
  }
}
</style>
