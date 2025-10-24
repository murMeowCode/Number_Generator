<template>
  <div class="bar-chart">
    <div class="chart-header">
      <h4>{{ title }}</h4>
    </div>
    <div class="chart-container">
      <canvas ref="chartRef" :width="width" :height="height"></canvas>
    </div>
    <div class="chart-summary" v-if="chartSummary">
      <div class="summary-item">
        <span class="summary-label">Среднее 1:</span>
        <span class="summary-value">{{ chartSummary.avgOnes }}</span>
      </div>
      <div class="summary-item">
        <span class="summary-label">Среднее 0:</span>
        <span class="summary-value">{{ chartSummary.avgZeros }}</span>
      </div>
      <div class="summary-item">
        <span class="summary-label">Всего диапазонов:</span>
        <span class="summary-value">{{ chartSummary.totalRanges }}</span>
      </div>
      <div class="summary-item" v-if="logScale">
        <span class="summary-label">Масштаб:</span>
        <span class="summary-value log-scale">Логарифмический</span>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch, onUnmounted, computed } from 'vue'

export default {
  name: 'BarChart',
  props: {
    data: {
      type: Object,
      default: () => ({}),
    },
    title: {
      type: String,
      default: 'Bar Chart',
    },
    width: {
      type: Number,
      default: 400,
    },
    height: {
      type: Number,
      default: 200,
    },
    summary: {
      type: Object,
      default: null,
    },
    showPeriodSelector: {
      type: Boolean,
      default: false,
    },
    showControls: {
      type: Boolean,
      default: true,
    },
    defaultLogScale: {
      type: Boolean,
      default: true,
    },
  },
  setup(props) {
    const chartRef = ref(null)
    const selectedPeriod = ref('month')
    const logScale = ref(props.defaultLogScale)
    let chartInstance = null

    // Вычисляем summary на основе данных
    const chartSummary = computed(() => {
      if (props.summary) {
        return props.summary
      }

      if (!props.data.datasets || props.data.datasets.length === 0) {
        return null
      }

      const onesDataset = props.data.datasets.find((d) => d.label && d.label.includes('1'))
      const zerosDataset = props.data.datasets.find((d) => d.label && d.label.includes('0'))

      if (!onesDataset || !zerosDataset || !onesDataset.data || !zerosDataset.data) {
        return null
      }

      const avgOnes = onesDataset.data.reduce((a, b) => a + b, 0) / onesDataset.data.length
      const avgZeros = zerosDataset.data.reduce((a, b) => a + b, 0) / zerosDataset.data.length

      return {
        avgOnes: avgOnes.toFixed(2),
        avgZeros: avgZeros.toFixed(2),
        totalRanges: onesDataset.data.length,
      }
    })

    const generateBarData = (period) => {
      const periods = {
        week: ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'],
        month: ['Нед 1', 'Нед 2', 'Нед 3', 'Нед 4'],
        year: ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн', 'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек'],
      }

      const labels = periods[period] || periods.month

      // Генерируем данные с большим разбросом для демонстрации логарифмической шкалы
      return {
        labels,
        datasets: [
          {
            label: 'Среднее количество 1',
            data: labels.map(() => Math.floor(Math.random() * 1000) + 1), // от 1 до 1000
            backgroundColor: '#4299e1',
            borderColor: '#4299e1',
            borderWidth: 1,
            borderRadius: 4,
          },
          {
            label: 'Среднее количество 0',
            data: labels.map(() => Math.floor(Math.random() * 1000) + 1), // от 1 до 1000
            backgroundColor: '#e53e3e',
            borderColor: '#e53e3e',
            borderWidth: 1,
            borderRadius: 4,
          },
        ],
      }
    }

    const getScaleOptions = () => {
      if (logScale.value) {
        return {
          type: 'logarithmic',
          beginAtZero: false,
          min: 1, // логарифмическая шкала не может начинаться с 0
          grid: {
            color: 'rgba(0, 0, 0, 0.1)',
          },
          title: {
            display: true,
            text: 'Среднее количество битов (лог. шкала)',
            font: {
              family: "'Exo 2', sans-serif",
              weight: 'bold',
            },
          },
          ticks: {
            font: {
              family: "'Exo 2', sans-serif",
            },
            callback: function (value, index, values) {
              // Форматируем метки для логарифмической шкалы
              if (value === 1) return '1'
              if (value === 10) return '10'
              if (value === 100) return '100'
              if (value === 1000) return '1000'
              if (value === 10000) return '10K'
              return ''
            },
          },
          afterBuildTicks: function (scale) {
            // Устанавливаем фиксированные деления для логарифмической шкалы
            scale.ticks = [1, 10, 100, 1000, 10000].map((v) => ({ value: v }))
          },
        }
      } else {
        return {
          beginAtZero: true,
          grid: {
            color: 'rgba(0, 0, 0, 0.1)',
          },
          title: {
            display: true,
            text: 'Среднее количество битов',
            font: {
              family: "'Exo 2', sans-serif",
              weight: 'bold',
            },
          },
          ticks: {
            font: {
              family: "'Exo 2', sans-serif",
            },
          },
        }
      }
    }

    const renderChart = async () => {
      if (!chartRef.value) return

      const { Chart } = await import('chart.js/auto')

      if (chartInstance) {
        chartInstance.destroy()
      }

      const chartData = props.data.datasets ? props.data : generateBarData(selectedPeriod.value)

      // Преобразуем данные для логарифмической шкалы (добавляем небольшое значение чтобы избежать 0)
      const processedData = {
        ...chartData,
        datasets: chartData.datasets.map((dataset) => ({
          ...dataset,
          data: dataset.data.map((value) => Math.max(value, 0.1)), // минимальное значение 0.1 для логарифма
        })),
      }

      const ctx = chartRef.value.getContext('2d')
      chartInstance = new Chart(ctx, {
        type: 'bar',
        data: processedData,
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'top',
              labels: {
                usePointStyle: true,
                padding: 15,
                font: {
                  family: "'Exo 2', sans-serif",
                },
              },
            },
            tooltip: {
              backgroundColor: 'rgba(0, 0, 0, 0.8)',
              titleFont: {
                family: "'Exo 2', sans-serif",
              },
              bodyFont: {
                family: "'Exo 2', sans-serif",
              },
              callbacks: {
                label: function (context) {
                  const label = context.dataset.label || ''
                  const rawValue = context.dataset.originalData
                    ? context.dataset.originalData[context.dataIndex]
                    : context.parsed.y
                  const value = context.parsed.y
                  return `${label}: ${rawValue.toFixed(2)}${logScale.value ? ' (лог: ' + value.toFixed(2) + ')' : ''}`
                },
                afterLabel: function (context) {
                  const datasetIndex = context.datasetIndex
                  const dataIndex = context.dataIndex
                  const label = context.label

                  if (props.data.originalData && props.data.originalData[dataIndex]) {
                    const originalData = props.data.originalData[dataIndex]
                    return [
                      `Диапазон: ${label}`,
                      `Кол-во последовательностей: ${originalData.sequence_count || 0}`,
                      `Средние 1: ${originalData.avg_ones || 0}`,
                      `Средние 0: ${originalData.avg_zeros || 0}`,
                    ]
                  }

                  return `Диапазон: ${label}`
                },
              },
            },
          },
          scales: {
            y: getScaleOptions(),
            x: {
              grid: {
                display: false,
              },
              title: {
                display: true,
                text: 'Диапазон длин последовательностей',
                font: {
                  family: "'Exo 2', sans-serif",
                  weight: 'bold',
                },
              },
              ticks: {
                font: {
                  family: "'Exo 2', sans-serif",
                },
              },
            },
          },
          interaction: {
            intersect: false,
            mode: 'index',
          },
        },
      })

      // Сохраняем оригинальные данные для отображения в tooltip
      chartData.datasets.forEach((dataset, index) => {
        if (chartInstance.data.datasets[index]) {
          chartInstance.data.datasets[index].originalData = [...dataset.data]
        }
      })
    }

    const handlePeriodChange = () => {
      renderChart()
    }

    const handleScaleChange = () => {
      renderChart()
    }

    onMounted(() => {
      renderChart()
    })

    watch(
      () => props.data,
      () => {
        console.log('📊 BarChart получил новые данные:', props.data)
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
      selectedPeriod,
      logScale,
      handlePeriodChange,
      handleScaleChange,
      chartSummary,
    }
  },
}
</script>

<style scoped>
.bar-chart {
  background: var(--color-bg-elevated);
  border-radius: var(--border-radius-lg);
  padding: var(--spacing-lg);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--color-border);
  font-family: 'Exo 2', sans-serif;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-md);
  flex-wrap: wrap;
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
}

.chart-controls {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  flex-wrap: wrap;
}

.control-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: var(--color-text);
  cursor: pointer;
  font-family: 'Exo 2', sans-serif;
}

.scale-toggle {
  width: 16px;
  height: 16px;
  cursor: pointer;
}

.period-select {
  padding: 6px 12px;
  border: 1px solid var(--color-border);
  border-radius: var(--border-radius-md);
  font-size: 14px;
  background: var(--color-bg);
  color: var(--color-text);
  font-family: 'Exo 2', sans-serif;
}

.chart-container {
  position: relative;
  height: 300px;
  margin: var(--spacing-md) 0;
}

.chart-summary {
  display: flex;
  justify-content: space-around;
  margin-top: var(--spacing-md);
  padding-top: var(--spacing-md);
  border-top: 1px solid var(--color-border);
  flex-wrap: wrap;
  gap: var(--spacing-md);
}

.summary-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 80px;
}

.summary-label {
  font-size: 12px;
  color: var(--color-text-muted);
  margin-bottom: 4px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.summary-value {
  font-size: 14px;
  font-weight: var(--font-weight-bold);
  color: var(--color-text);
  font-family: 'Share Tech Mono', monospace;
}

.summary-value.log-scale {
  color: var(--color-primary);
  font-weight: var(--font-weight-bold);
}

@media (max-width: 768px) {
  .chart-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .chart-controls {
    width: 100%;
    justify-content: space-between;
  }

  .chart-summary {
    justify-content: flex-start;
  }
}
</style>
