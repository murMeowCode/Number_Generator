<template>
  <div class="one-dash">
    <!-- Заголовок -->
    <div class="dashboard-header">
      <h1>{{ title }}</h1>
      <div class="header-actions">
        <slot name="header-actions"></slot>
      </div>
    </div>

    <!-- Статистика -->
    <div class="stats-grid" v-if="stats && stats.length && !loading">
      <div
        v-for="(stat, index) in stats"
        :key="index"
        class="stat-card"
        :class="`stat-${stat.type || 'default'}`"
      >
        <div class="stat-icon">
          <i :class="stat.icon"></i>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ stat.value }}</div>
          <div class="stat-label">{{ stat.label }}</div>
        </div>
      </div>
    </div>

    <!-- Графики -->
    <div class="charts-section" v-if="charts && charts.length">
      <!-- Первая строка: линейный график и гистограмма -->
      <div class="charts-row" v-if="hasRegularCharts">
        <div v-for="chart in regularCharts" :key="chart.type" class="chart-container regular-chart">
          <!-- Линейные графики -->
          <template v-if="chart.type === 'line'">
            <slot name="chart-line" :chart="chart" v-if="$slots['chart-line']">
              <div class="chart-placeholder">
                <h3>{{ chart.title }}</h3>
                <p>Линейный график: слот chart-line не предоставлен</p>
              </div>
            </slot>
          </template>

          <!-- Гистограммы -->
          <template v-else-if="chart.type === 'bar'">
            <slot name="chart-bar" :chart="chart" v-if="$slots['chart-bar']">
              <div class="chart-placeholder">
                <h3>{{ chart.title }}</h3>
                <p>Гистограмма: слот chart-bar не предоставлен</p>
              </div>
            </slot>
          </template>
        </div>
      </div>

      <!-- Вторая строка: тепловая карта -->
      <div class="charts-row" v-if="hasHeatmapChart">
        <div v-for="chart in heatmapCharts" :key="chart.type" class="chart-container heatmap-chart">
          <!-- Тепловые карты -->
          <template v-if="chart.type === 'heatmap'">
            <slot name="chart-heatmap" :chart="chart" v-if="$slots['chart-heatmap']">
              <div class="chart-placeholder">
                <h3>{{ chart.title }}</h3>
                <p>Тепловая карта: слот chart-heatmap не предоставлен</p>
              </div>
            </slot>
          </template>
        </div>
      </div>

      <!-- Третья строка: круговая диаграмма -->
      <h3>ДВА САМЫХ ТЯЖЕЛО ПРОХОДИМЫХ ТЕСТОВ</h3>
      <div class="charts-row" v-if="hasPieChart">
        <div v-for="chart in pieCharts" :key="chart.type" class="chart-container pie-chart">
          <!-- Круговые диаграммы -->
          
          <template v-if="chart.type === 'pie'">
            <slot name="chart-pie" :chart="chart" v-if="$slots['chart-pie']">
              <div class="chart-placeholder">
                <h3>{{ chart.title }}</h3>
                <p>Круговая диаграмма: слот chart-pie не предоставлен</p>
              </div>
            </slot>
          </template>
        </div>
      </div>

      <!-- Другие типы графиков -->
      <div class="charts-row" v-if="hasOtherCharts">
        <div v-for="chart in otherCharts" :key="chart.type" class="chart-container other-chart">
          <div class="chart-placeholder">
            <h3>{{ chart.title }}</h3>
            <p>Тип графика: {{ chart.type }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Таблицы -->
    <div class="tables-section" v-if="tables && tables.length">
      <div v-for="(table, index) in tables" :key="index" class="table-container">
        <h3>{{ table.title }}</h3>
        <slot :name="`table-${table.type}`" :table="table" v-if="$slots[`table-${table.type}`]">
          <div class="table-placeholder">
            <p>Таблица типа "{{ table.type }}": слот не предоставлен</p>
          </div>
        </slot>
      </div>
    </div>

    <!-- Кастомный контент -->
    <div class="custom-section" v-if="$slots.custom">
      <slot name="custom"></slot>
    </div>

    <!-- Состояние загрузки -->
    <div v-if="loading" class="loading-overlay">
      <div class="loading-spinner">
        <i class="fas fa-spinner fa-spin"></i>
        <img src="@/assets/loader.svg" alt="Loading..." class="loader-svg" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  title: {
    type: String,
    default: 'Дашборд',
  },
  stats: {
    type: Array,
    default: () => [],
  },
  charts: {
    type: Array,
    default: () => [],
  },
  tables: {
    type: Array,
    default: () => [],
  },
  loading: {
    type: Boolean,
    default: false,
  },
})

// Computed свойства для разделения графиков по типам
const regularCharts = computed(() => {
  return props.charts.filter((chart) => chart.type === 'line' || chart.type === 'bar')
})

const heatmapCharts = computed(() => {
  return props.charts.filter((chart) => chart.type === 'heatmap')
})

const pieCharts = computed(() => {
  return props.charts.filter((chart) => chart.type === 'pie')
})

const otherCharts = computed(() => {
  return props.charts.filter(
    (chart) =>
      chart.type !== 'line' &&
      chart.type !== 'bar' &&
      chart.type !== 'heatmap' &&
      chart.type !== 'pie',
  )
})

const hasRegularCharts = computed(() => regularCharts.value.length > 0)
const hasHeatmapChart = computed(() => heatmapCharts.value.length > 0)
const hasPieChart = computed(() => pieCharts.value.length > 0)
const hasOtherCharts = computed(() => otherCharts.value.length > 0)
</script>

<style scoped>
.one-dash {
  position: relative;
  min-height: 400px;
  padding: 0 2rem;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-xl);
  padding-bottom: var(--spacing-md);
  border-bottom: 1px solid var(--color-border);
}

.dashboard-header h1 {
  margin: 0;
  color: var(--color-text);
  font-size: 1.75rem;
  font-weight: var(--font-weight-bold);
  font-family: 'Orbitron', sans-serif;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-xl);
}

/* Стили для секции графиков */
.charts-section {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
  margin-bottom: var(--spacing-xl);
}

.charts-row {
  display: grid;
  gap: var(--spacing-lg);
}

/* Первая строка: линейный график и гистограмма - 2 колонки */
.charts-row:first-child {
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
}

/* Вторая строка: тепловая карта - 1 колонка на всю ширину */
.charts-row:nth-child(2) {
  grid-template-columns: 1fr;
}

/* Третья строка: круговая диаграмма - 1 колонка */
.charts-row:nth-child(3) {
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
}

/* Четвертая строка и далее: другие графики */
.charts-row:nth-child(n + 4) {
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
}

/* Базовые стили для контейнеров графиков */
.chart-container {
  background: var(--color-bg-elevated);
  border-radius: var(--border-radius-lg);
  padding: var(--spacing-lg);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--color-border);
  min-height: 300px;
}

/* Специфичные стили для тепловой карты */
.heatmap-chart {
  min-height: 500px;
  width: 100%;
}

/* Стили для круговой диаграммы */
.pie-chart {
  min-height: 350px;
}

.chart-container h3 {
  margin: 0 0 var(--spacing-md) 0;
  color: var(--color-text);
  font-size: 1.125rem;
  font-weight: var(--font-weight-semibold);
}

.chart-placeholder,
.table-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 200px;
  color: var(--color-text-muted);
  text-align: center;
}

/* Остальные стили без изменений */
.stat-card {
  display: flex;
  align-items: center;
  padding: var(--spacing-lg);
  background: var(--color-bg-elevated);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--color-border);
  transition: all var(--transition-normal);
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.stat-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  border-radius: var(--border-radius-md);
  margin-right: var(--spacing-md);
  font-size: 1.25rem;
}

.stat-default .stat-icon {
  background: var(--color-primary-soft);
  color: var(--color-primary);
}

.stat-success .stat-icon {
  background: var(--color-success-soft);
  color: var(--color-success);
}

.stat-warning .stat-icon {
  background: var(--color-warning-soft);
  color: var(--color-warning);
}

.stat-danger .stat-icon {
  background: var(--color-danger-soft);
  color: var(--color-danger);
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: var(--font-weight-bold);
  color: var(--color-text);
  margin-bottom: var(--spacing-xs);
  font-family: 'Share Tech Mono', monospace;
}

.stat-label {
  font-size: 0.875rem;
  color: var(--color-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.tables-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: var(--spacing-lg);
  margin-bottom: var(--spacing-xl);
}

.table-container {
  background: var(--color-bg-elevated);
  border-radius: var(--border-radius-lg);
  padding: var(--spacing-lg);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--color-border);
}

.table-container h3 {
  margin: 0 0 var(--spacing-md) 0;
  color: var(--color-text);
  font-size: 1.125rem;
  font-weight: var(--font-weight-semibold);
}

.custom-section {
  margin-top: var(--spacing-xl);
}

.loading-overlay {
  position: absolute;
  top: 350px;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(var(--color-bg-rgb), 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10;
}

.loading-spinner {
  text-align: center;
  color: var(--color-primary);
}

.loading-spinner i {
  font-size: 2rem;
  margin-bottom: var(--spacing-md);
}

/* Адаптивность для мобильных устройств */
@media (max-width: 768px) {
  .dashboard-header {
    flex-direction: column;
    gap: var(--spacing-md);
    align-items: flex-start;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .charts-section {
    gap: var(--spacing-md);
  }

  .charts-row {
    grid-template-columns: 1fr !important;
    gap: var(--spacing-md);
  }

  .chart-container {
    padding: var(--spacing-md);
    min-height: 250px;
  }

  .heatmap-chart {
    min-height: 400px;
  }

  .pie-chart {
    min-height: 300px;
  }

  .tables-section {
    grid-template-columns: 1fr;
  }

  .table-container {
    padding: var(--spacing-md);
  }
}

/* Адаптивность для очень маленьких экранов */
@media (max-width: 480px) {
  .dashboard-header h1 {
    font-size: 1.5rem;
  }

  .stat-card {
    padding: var(--spacing-md);
  }

  .stat-icon {
    width: 40px;
    height: 40px;
    font-size: 1rem;
  }

  .stat-value {
    font-size: 1.25rem;
  }

  .chart-container,
  .table-container {
    padding: var(--spacing-sm);
  }

  .heatmap-chart {
    min-height: 350px;
  }

  .pie-chart {
    min-height: 250px;
  }
}
</style>
