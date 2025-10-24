<template>
  <OneDash
    :title="dashboardTitle"
    :stats="statsData"
    :charts="chartsData"
    :tables="tablesData"
    :loading="isLoading"
  >
    <!-- Слот для линейных графиков -->
    <template #chart-line="{ chart }">
      <LineChart :data="chart.data" :title="chart.title" :footer-text="chart.footerText" />
    </template>

    <!-- Слот для гистограмм -->
    <template #chart-bar="{ chart }">
      <BarChart :data="chart.data" :title="chart.title" />
    </template>

    <!-- Слот для тепловой карты -->
    <template #chart-heatmap="{ chart }">
      <HeatmapChart :data="chart.data" :title="chart.title" />
    </template>
    
    <template #chart-pie="{ chart }">
      <PieChart :data="chart.data" :title="chart.title" :show-failed-percentage="true" />
    </template>
  </OneDash>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import OneDash from './OneDash.vue'
import LineChart from '@/components/Charts/LineChart.vue'
import BarChart from '@/components/Charts/BarChart.vue'
import { useApiGet } from '@/utils/api/useApiGet'
import { api8000, api8001 } from '@/utils/apiUrl/urlApi'
import HeatmapChart from '../Charts/HeatmapChart.vue'
import PieChart from '../Charts/PieChart.vue'

const { useGet } = useApiGet()

// Refs
const dashboardTitle = ref('')
const activities = ref([])
const lastUpdated = ref(null)

// API запросы
const {
  data: statsResponse,
  isPending: statsLoading,
  error: statsError,
} = useGet(`${api8000}/statistics/dashboard/overview`, {}, { withCredentials: true })

const {
  data: chartsTablesResponse,
  isPending: chartsTablesLoading,
  error: chartsTablesError,
} = useGet(`${api8001}/generate/dashboard/generations`, {}, { withCredentials: true })

// Computed свойства для данных
const statsData = computed(() => {
  if (!statsResponse.value) return getDefaultStats()

  const apiStats = statsResponse.value
  const requiredStats = []

  if (apiStats.avg_sequence_length !== undefined) {
    requiredStats.push({
      value:
        typeof apiStats.avg_sequence_length === 'number'
          ? apiStats.avg_sequence_length.toFixed(2)
          : apiStats.avg_sequence_length.toString(),
      label: 'Средняя длина последовательности',
      icon: 'fas fa-ruler',
      type: getTypeByValue(apiStats.avg_sequence_length),
    })
  }

  if (apiStats.avg_success_rate !== undefined) {
    requiredStats.push({
      value:
        typeof apiStats.avg_success_rate === 'number'
          ? `${apiStats.avg_success_rate.toFixed(2)}%`
          : apiStats.avg_success_rate.toString(),
      label: 'Средняя успешность тестов',
      icon: 'fas fa-chart-line',
      type: getTypeByValue(apiStats.avg_success_rate),
    })
  }

  if (apiStats.total_sequences !== undefined) {
    requiredStats.push({
      value: apiStats.total_sequences?.toString() || '0',
      label: 'Всего последовательностей',
      icon: 'fas fa-list-ol',
      type: getTypeByValue(apiStats.total_sequences),
    })
  }

  return requiredStats.length > 0 ? requiredStats : getDefaultStats()
})

// ИСПРАВЛЕННЫЙ computed для графиков
// ИСПРАВЛЕННЫЙ computed для графиков
// ИСПРАВЛЕННЫЙ computed для графиков с отладкой
// ИСПРАВЛЕННЫЙ computed для графиков с тестовыми данными
// ИСПРАВЛЕННЫЙ computed для графиков
const chartsData = computed(() => {
  const charts = []

  try {
    // 1. Добавляем линейный график с данными seed из api8001
    if (chartsTablesResponse.value && Array.isArray(chartsTablesResponse.value)) {
      console.log('📥 Данные для линейного графика (api8001):', chartsTablesResponse.value)
      const seedChart = createSeedLineChart(chartsTablesResponse.value)
      if (seedChart && seedChart.data) {
        charts.push(seedChart)
      }
    }

    // 2. Добавляем гистограмму из bit_distribution из api8000
    if (statsResponse.value?.bit_distribution) {
      console.log('📊 Данные для гистограммы (api8000):', statsResponse.value.bit_distribution)
      const bitDistributionChart = {
        title: 'Распределение битов по длинам последовательностей',
        type: 'bar',
        data: transformBitDistribution(statsResponse.value.bit_distribution),
      }
      if (bitDistributionChart.data && bitDistributionChart.data.labels) {
        charts.push(bitDistributionChart)
      }
    }

    // 3. Добавляем тепловую карту из heatmap_data из api8000
    if (statsResponse.value?.heatmap_data) {
      console.log('🔥 Данные для тепловой карты (api8000):', statsResponse.value.heatmap_data)
      const heatmapChart = {
        title: 'Тепловая карта 10 последних тестов последовательностей',
        type: 'heatmap',
        data: statsResponse.value.heatmap_data,
      }
      charts.push(heatmapChart)
    }

    // 4. Добавляем круговые диаграммы из worst_tests из api8000
    if (statsResponse.value?.worst_tests && Array.isArray(statsResponse.value.worst_tests)) {
      console.log('🥧 Данные для круговых диаграмм (api8000):', statsResponse.value.worst_tests)

      // Создаем отдельную круговую диаграмму для каждого худшего теста
      statsResponse.value.worst_tests.forEach((test, index) => {
        const pieChart = {
          title: `Тест: ${formatTestName(test.test_name)}`,
          type: 'pie',
          data: [test], // Передаем массив с одним тестом
          testInfo: test, // Дополнительная информация о тесте
        }
        charts.push(pieChart)
      })
    }
  } catch (error) {
    console.error('❌ Ошибка обработки графиков:', error)
  }

  console.log(
    '📈 Итоговые графики:',
    charts.map((chart) => ({
      type: chart.type,
      title: chart.title,
      hasData: !!chart.data,
    })),
  )

  return charts
})

// Добавьте вспомогательную функцию для форматирования названий тестов
const formatTestName = (testName) => {
  const names = {
    runs: 'Runs Test',
    matrix_rank: 'Matrix Rank',
    cumulative_sums: 'Cumulative Sums',
    longest_runs: 'Longest Runs',
    frequency: 'Frequency',
    autocorrelation: 'Autocorrelation',
    poker: 'Poker Test',
    serial: 'Serial Test',
  }
  return names[testName] || testName
}
// ИСПРАВЛЕННАЯ функция для создания линейного графика seed значений
const createSeedLineChart = (data) => {
  console.log('📥 ВХОДНЫЕ ДАННЫЕ ДЛЯ ЛИНЕЙНОГО ГРАФИКА:', data)

  if (!data || !Array.isArray(data) || data.length === 0) {
    console.warn('⚠️ Нет данных для создания линейного графика seed')
    return null
  }

  try {
    // Фильтруем только валидные данные
    const validData = data.filter((item) => item && item.seed !== undefined && item.created_at)

    console.log('📊 Валидные данные после фильтрации:', validData)

    if (validData.length === 0) {
      console.warn('⚠️ Нет валидных данных для графика seed')
      return null
    }

    // СОРТИРУЕМ данные по дате (от старых к новым) для правильного отображения
    const sortedData = [...validData].sort(
      (a, b) => new Date(a.created_at) - new Date(b.created_at),
    )

    console.log('📊 Отсортированные данные:', sortedData)

    // Извлекаем seed значения и даты
    const seedValues = sortedData.map((item) => {
      const seed = parseFloat(item.seed)
      return isNaN(seed) ? 0 : seed
    })

    const labels = sortedData.map((item) => {
      try {
        const date = new Date(item.created_at)
        return date.toLocaleTimeString('ru-RU', {
          hour: '2-digit',
          minute: '2-digit',
        })
      } catch {
        return '--:--'
      }
    })

    // Рассчитываем математическое ожидание (среднее значение)
    const meanValue = seedValues.reduce((sum, val) => sum + val, 0) / seedValues.length

    console.log('📊 Итоговые данные для линейного графика:', {
      labels,
      seedValues,
      meanValue,
    })

    return {
      title: 'Динамика Seed значений',
      type: 'line',
      footerText: `Математическое ожидание: ${meanValue.toFixed(6)}`,
      data: {
        labels,
        datasets: [
          {
            label: 'Seed значения',
            data: seedValues,
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
            data: Array(seedValues.length).fill(meanValue),
            borderColor: '#e53e3e',
            backgroundColor: 'transparent',
            borderWidth: 2,
            borderDash: [5, 5],
            tension: 0,
            fill: false,
            pointRadius: 0,
          },
        ],
      },
    }
  } catch (error) {
    console.error('❌ Ошибка создания линейного графика:', error)
    return null
  }
}

// Функция для преобразования bit_distribution
const transformBitDistribution = (bitDistribution) => {
  if (!bitDistribution || !Array.isArray(bitDistribution)) {
    return getDefaultChartData('bar')
  }

  console.log('📊 Исходные данные bit_distribution:', bitDistribution)

  const labels = bitDistribution.map((item) => item.length_range)
  const avgOnesData = bitDistribution.map((item) => parseFloat(item.avg_ones) || 0)
  const avgZerosData = bitDistribution.map((item) => parseFloat(item.avg_zeros) || 0)

  const transformedData = {
    labels,
    datasets: [
      {
        label: 'Среднее количество 1',
        data: avgOnesData,
        backgroundColor: '#4299e1',
        borderColor: '#4299e1',
        borderWidth: 1,
        borderRadius: 4,
        barPercentage: 0.6,
        categoryPercentage: 0.8,
      },
      {
        label: 'Среднее количество 0',
        data: avgZerosData,
        backgroundColor: '#e53e3e',
        borderColor: '#e53e3e',
        borderWidth: 1,
        borderRadius: 4,
        barPercentage: 0.6,
        categoryPercentage: 0.8,
      },
    ],
  }

  console.log('📈 Преобразованные данные для гистограммы:', transformedData)
  return transformedData
}

const tablesData = computed(() => {
  if (!chartsTablesResponse.value) return getDefaultTables()

  const apiTables = chartsTablesResponse.value.tables || []
  if (Array.isArray(apiTables)) {
    return apiTables.map((table) => ({
      title: table.title || 'Таблица',
      type: table.type || 'users',
      data: table.data || {},
    }))
  }

  return getDefaultTables()
})

const isLoading = computed(() => statsLoading.value && chartsTablesLoading.value)

const error = computed(() => statsError.value || chartsTablesError.value)

// Watchers
watch(statsResponse, (newData) => {
  if (newData) {
    console.log('📊 Статистика загружена (api8000):', newData)
    lastUpdated.value = new Date().toLocaleString('ru-RU')
    addActivity({
      user: 'Система',
      action: 'статистика обновлена',
      type: 'success',
    })
  }
})

watch(chartsTablesResponse, (newData) => {
  if (newData) {
    console.log('📈 Данные для линейного графика загружены (api8001):', newData)
    addActivity({
      user: 'Система',
      action: 'графики и таблицы обновлены',
      type: 'success',
    })
  }
})

watch([statsError, chartsTablesError], ([statsErr, chartsErr]) => {
  if (statsErr || chartsErr) {
    console.error('❌ Ошибки загрузки:', { statsErr, chartsErr })
    addActivity({
      user: 'Система',
      action: 'ошибка загрузки данных',
      type: 'danger',
      details: statsErr?.message || chartsErr?.message,
    })
  }
})

// Methods
const refreshData = () => {
  window.location.reload()
}

const addTestActivity = () => {
  addActivity({
    user: 'Тестовая система',
    action: 'выполнено тестовое действие',
    type: 'warning',
    details: 'Это тестовая активность для демонстрации',
  })
}

const addActivity = (activity) => {
  activities.value.unshift({
    id: Date.now(),
    time: 'только что',
    ...activity,
  })

  if (activities.value.length > 10) {
    activities.value = activities.value.slice(0, 10)
  }
}

// Вспомогательные функции
const getTypeByValue = (value) => {
  if (typeof value === 'number') {
    if (value > 80) return 'success'
    if (value > 50) return 'warning'
    return 'danger'
  }
  return 'default'
}

// Дефолтные данные
const getDefaultStats = () => [
  {
    value: '0',
    label: 'Всего пользователей',
    icon: 'fas fa-users',
    type: 'default',
  },
  {
    value: '₽0',
    label: 'Общий доход',
    icon: 'fas fa-dollar-sign',
    type: 'default',
  },
  {
    value: '0%',
    label: 'Успешных операций',
    icon: 'fas fa-chart-line',
    type: 'default',
  },
  {
    value: '0',
    label: 'Ошибок сегодня',
    icon: 'fas fa-exclamation-triangle',
    type: 'default',
  },
]

const getDefaultCharts = () => [
  {
    title: 'Динамика Seed значений',
    type: 'line',
    data: getDefaultLineChartData(),
  },
  {
    title: 'Распределение битов',
    type: 'bar',
    data: getDefaultBarChartData(),
  },
]

const getDefaultLineChartData = () => {
  return {
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
      },
    ],
  }
}

const getDefaultBarChartData = () => {
  return {
    labels: ['10-20', '21-30', '31-40', '41-50', '51-60'],
    datasets: [
      {
        label: 'Среднее количество 1',
        data: [5, 8, 12, 15, 18],
        backgroundColor: '#4299e1',
      },
      {
        label: 'Среднее количество 0',
        data: [5, 7, 8, 10, 12],
        backgroundColor: '#e53e3e',
      },
    ],
  }
}

const getDefaultChartData = (type) => {
  return type === 'bar' ? getDefaultBarChartData() : getDefaultLineChartData()
}

const getDefaultTables = () => []

// Lifecycle
onMounted(() => {
  console.log('🚀 Dashboard компонент загружен')
})
</script>

<style scoped>
/* Стили остаются без изменений */
.actions-container {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  flex-wrap: wrap;
}

.header-actions {
  display: flex;
  gap: var(--spacing-sm);
  align-items: center;
}

.btn {
  padding: 10px 16px;
  border: 1px solid;
  border-radius: var(--border-radius-md);
  font-size: 14px;
  font-weight: var(--font-weight-medium);
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all var(--transition-normal);
  font-family: 'Rajdhani', 'Exo 2', sans-serif;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none !important;
}

.btn-primary {
  background: var(--color-vanilla-light);
  color: var(--color-midnight);
  border-color: var(--color-midnight);
  box-shadow: var(--shadow-md);
}

.btn-primary:hover:not(:disabled) {
  background: var(--color-dark);
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

.btn-accent {
  background: var(--color-midnight-medium);
  color: var(--color-vanilla);
  border-color: var(--color-midnight-medium);
  box-shadow: var(--shadow-sm);
}

.btn-accent:hover:not(:disabled) {
  background: var(--color-midnight-light);
  border-color: var(--color-midnight-light);
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
}

.last-updated {
  font-size: 12px;
  color: var(--color-text-muted);
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 12px;
  background: var(--color-primary-soft);
  border-radius: var(--border-radius-md);
  border: 1px solid var(--color-border);
  font-family: 'Share Tech Mono', monospace;
}

.recent-activity {
  margin-top: var(--spacing-xl);
  background: var(--color-bg-elevated);
  border-radius: var(--border-radius-lg);
  padding: var(--spacing-lg);
  box-shadow: var(--shadow-indigo);
  border: 1px solid var(--color-border);
}

.custom-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-lg);
  padding-bottom: var(--spacing-md);
  border-bottom: 1px solid var(--color-border);
}

.custom-header h3 {
  margin: 0;
  color: var(--color-text);
  font-size: 1.25rem;
  font-weight: var(--font-weight-semibold);
  font-family: 'Orbitron', sans-serif;
  text-transform: uppercase;
  letter-spacing: 1px;
  background: var(--color-accent);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

@media (max-width: 768px) {
  .actions-container {
    flex-direction: column;
    align-items: stretch;
    gap: var(--spacing-sm);
  }

  .custom-header {
    flex-direction: column;
    gap: var(--spacing-md);
    align-items: flex-start;
  }

  .header-actions {
    width: 100%;
    justify-content: space-between;
  }

  .btn {
    justify-content: center;
  }
}

.btn {
  position: relative;
  overflow: hidden;
}

.btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.2);
  transition: left var(--transition-slow);
}

.btn:hover::before {
  left: 100%;
}

.btn:active {
  transform: translateY(0);
}

.btn-primary:active {
  background: var(--color-midnight);
}

.btn i {
  font-size: 0.9em;
  transition: transform var(--transition-fast);
}

.btn:hover:not(:disabled) i {
  transform: scale(1.1);
}

.fa-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.btn:disabled {
  background: var(--color-bg-muted);
  color: var(--color-text-muted);
  border-color: var(--color-border);
  box-shadow: none;
}
</style>
