<template>
  <div class="pie-chart">
    <div class="chart-header">
      <h4>{{ title }}</h4>
      <div class="test-info" v-if="testInfo">
        <div class="info-item">
          <span class="info-label">Всего последовательностей:</span>
          <span class="info-value">{{ testInfo.total_sequences }}</span>
        </div>
      </div>
    </div>

    <div class="chart-container">
      <canvas ref="chartRef" :width="width" :height="height"></canvas>
    </div>

    <div class="chart-summary" v-if="summary">
      <div class="summary-item">
        <span class="summary-label">Успешность:</span>
        <span class="summary-value success">{{ summary.successRate }}%</span>
      </div>
      <div class="summary-item">
        <span class="summary-label">Неудачи:</span>
        <span class="summary-value danger">{{ summary.failedRate }}%</span>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch, onUnmounted, computed } from 'vue'

export default {
  name: 'PieChart',
  props: {
    data: {
      type: Array,
      default: () => [],
    },
    title: {
      type: String,
      default: 'Круговая диаграмма',
    },
    width: {
      type: Number,
      default: 400,
    },
    height: {
      type: Number,
      default: 300,
    },
    showFailedPercentage: {
      type: Boolean,
      default: true,
    },
    testInfo: {
      type: Object,
      default: null,
    },
  },
  setup(props) {
    const chartRef = ref(null)
    let chartInstance = null

    // Вычисляем данные для одного теста
    const chartData = computed(() => {
      if (!props.data || !Array.isArray(props.data) || props.data.length === 0) {
        return getDefaultChartData()
      }

      const test = props.data[0] // Берем первый (и единственный) тест из массива
      const testName = test.test_name || 'Тест'
      const successRate = parseFloat(test.success_rate) || 0
      const failedRate = 100 - successRate

      return {
        labels: ['Успешные', 'Неудачные'],
        datasets: [
          {
            label: testName,
            data: props.showFailedPercentage ? [successRate, failedRate] : [successRate],
            backgroundColor: props.showFailedPercentage
              ? ['#48bb78', '#f56565'] // Зеленый для успеха, красный для неудач
              : ['#48bb78'], // Только зеленый если показываем только успешные
            borderColor: 'white',
            borderWidth: 2,
            hoverOffset: 8,
          },
        ],
      }
    })

    // Вычисляем summary для одного теста
    const summary = computed(() => {
      if (!props.data || props.data.length === 0) return null

      const test = props.data[0]
      const successRate = parseFloat(test.success_rate) || 0
      const failedRate = 100 - successRate

      return {
        successRate: successRate.toFixed(1),
        failedRate: failedRate.toFixed(1),
      }
    })

    const getDefaultChartData = () => {
      return {
        labels: ['Успешные', 'Неудачные'],
        datasets: [
          {
            label: 'Тест',
            data: [70, 30],
            backgroundColor: ['#48bb78', '#f56565'],
            borderColor: 'white',
            borderWidth: 2,
            hoverOffset: 8,
          },
        ],
      }
    }

    const renderChart = async () => {
      if (!chartRef.value) return

      const { Chart } = await import('chart.js/auto')

      if (chartInstance) {
        chartInstance.destroy()
      }

      const ctx = chartRef.value.getContext('2d')

      const dataToRender = chartData.value.datasets ? chartData.value : getDefaultChartData()

      chartInstance = new Chart(ctx, {
        type: 'pie',
        data: dataToRender,
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'bottom',
              labels: {
                usePointStyle: true,
                padding: 15,
              },
            },
            tooltip: {
              callbacks: {
                label: function (context) {
                  const label = context.label || ''
                  const value = context.parsed
                  return `${label}: ${value}%`
                },
              },
            },
          },
          cutout: '0%',
          animation: {
            animateScale: true,
            animateRotate: true,
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
      chartData,
      summary,
    }
  },
}
</script>

<style scoped>
.pie-chart {
  background: var(--color-bg-elevated);
  border-radius: var(--border-radius-lg);
  padding: var(--spacing-lg);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--color-border);
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: var(--spacing-lg);
  gap: var(--spacing-md);
}

.chart-header h4 {
  margin: 0;
  color: var(--color-text);
  font-size: 1.125rem;
  font-weight: var(--font-weight-semibold);
  font-family: 'Orbitron', sans-serif;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  flex: 1;
}

.test-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
  min-width: 120px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 8px;
}

.info-label {
  font-size: 11px;
  color: var(--color-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.info-value {
  font-size: 12px;
  font-weight: var(--font-weight-bold);
  color: var(--color-text);
  font-family: 'Share Tech Mono', monospace;
}

.chart-container {
  position: relative;
  height: 250px;
  margin: var(--spacing-md) 0;
}

.chart-summary {
  display: flex;
  justify-content: space-around;
  margin-top: var(--spacing-md);
  padding-top: var(--spacing-md);
  border-top: 1px solid var(--color-border);
}

.summary-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.summary-label {
  font-size: 11px;
  color: var(--color-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.summary-value {
  font-size: 14px;
  font-weight: var(--font-weight-bold);
  font-family: 'Share Tech Mono', monospace;
}

.summary-value.success {
  color: #48bb78;
}

.summary-value.danger {
  color: #f56565;
}

/* Адаптивность */
@media (max-width: 768px) {
  .chart-header {
    flex-direction: column;
    gap: var(--spacing-md);
  }

  .test-info {
    min-width: 100%;
  }

  .chart-container {
    height: 200px;
  }
}

@media (max-width: 480px) {
  .pie-chart {
    padding: var(--spacing-md);
  }

  .chart-container {
    height: 180px;
  }
}
</style>
