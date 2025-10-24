<template>
  <div class="heatmap-chart">
    <div class="chart-header">
      <h4>{{ title }}</h4>
      <div class="chart-controls">
        <div class="legend">
          <div class="legend-item">
            <span class="legend-color success"></span>
            <span class="legend-label">PASS</span>
          </div>
          <div class="legend-item">
            <span class="legend-color warning"></span>
            <span class="legend-label">WARNING</span>
          </div>
          <div class="legend-item">
            <span class="legend-color danger"></span>
            <span class="legend-label">FAIL</span>
          </div>
        </div>
      </div>
    </div>

    <div class="chart-container">
      <!-- Отладочная информация -->
      <div v-if="debugInfo" class="debug-info">
        <p>
          Тестов: {{ testNames.length }}, Последовательностей: {{ sequenceIds.length }},
          Результатов: {{ results.length }}
        </p>
        <p>Пример результата: {{ sampleResult }}</p>
      </div>

      <div class="heatmap-grid">
        <!-- Заголовки тестов (Y-axis) -->
        <div class="y-axis-labels">
          <!-- Дополнительная пустая ячейка для выравнивания с заголовками X-axis -->
          <div class="y-label empty-corner"></div>
          <div v-for="testName in testNames" :key="testName" class="y-label">
            {{ formatTestName(testName) }}
          </div>
        </div>

        <!-- Основная сетка тепловой карты -->
        <div class="heatmap-content">
          <!-- Заголовки sequence_id (X-axis) -->
          <div class="x-axis-labels">
            <div
              v-for="sequenceId in sequenceIds"
              :key="sequenceId"
              class="x-label"
              :title="sequenceId"
            >
              {{ formatSequenceId(sequenceId) }}
            </div>
          </div>

          <!-- Ячейки тепловой карты -->
          <div class="heatmap-cells">
            <div v-for="testName in testNames" :key="testName" class="heatmap-row">
              <div
                v-for="sequenceId in sequenceIds"
                :key="sequenceId"
                class="heatmap-cell"
                :class="getCellClass(testName, sequenceId)"
                @mouseover="showTooltip($event, testName, sequenceId)"
                @mouseleave="hideTooltip"
              >
                <div class="cell-content">
                  {{ getCellStatus(testName, sequenceId) }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Tooltip -->
      <div
        v-if="tooltip.visible"
        class="heatmap-tooltip"
        :style="{
          left: tooltip.x + 'px',
          top: tooltip.y + 'px',
        }"
      >
        <div class="tooltip-content">
          <div class="tooltip-row">
            <strong>Тест:</strong> {{ formatTestName(tooltip.testName) }}
          </div>
          <div class="tooltip-row"><strong>Sequence ID:</strong> {{ tooltip.sequenceId }}</div>
          <div class="tooltip-row">
            <strong>Статус:</strong>
            <span
              :class="`status-${getCellStatus(tooltip.testName, tooltip.sequenceId)?.toLowerCase()}`"
            >
              {{ getCellStatus(tooltip.testName, tooltip.sequenceId) }}
            </span>
          </div>
          <div v-if="getCellDetails(tooltip.testName, tooltip.sequenceId)" class="tooltip-row">
            <strong>Детали:</strong> {{ getCellDetails(tooltip.testName, tooltip.sequenceId) }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'

export default {
  name: 'HeatmapChart',
  props: {
    data: {
      type: Object,
      required: true,
      validator: (value) => {
        return (
          value &&
          Array.isArray(value.results) &&
          Array.isArray(value.sequence_ids) &&
          Array.isArray(value.test_names)
        )
      },
    },
    title: {
      type: String,
      default: 'Тепловая карта 10 последних тестов',
    },
    debug: {
      type: Boolean,
      default: false,
    },
  },
  setup(props) {
    const tooltip = ref({
      visible: false,
      x: 0,
      y: 0,
      testName: '',
      sequenceId: '',
    })

    // Computed свойства для удобства
    const testNames = computed(() => props.data.test_names || [])
    const sequenceIds = computed(() => props.data.sequence_ids || [])
    const results = computed(() => props.data.results || [])

    // Отладочная информация
    const debugInfo = computed(() => props.debug)
    const sampleResult = computed(() => {
      if (results.value.length > 0) {
        const result = results.value[0]
        return {
          keys: Object.keys(result),
          values: result,
        }
      }
      return null
    })

    // Находим результат для конкретной ячейки - ИСПРАВЛЕННАЯ ФУНКЦИЯ
    const findResult = (testName, sequenceId) => {
      console.log(`🔍 Поиск: test_name=${testName}, sequence_id=${sequenceId}`)

      const result = results.value.find((result) => {
        // Проверяем разные возможные названия полей
        const hasTestName =
          result.test_name === testName ||
          result.test_name?.toLowerCase() === testName?.toLowerCase() ||
          result.test === testName

        const hasSequenceId =
          result.sequence_id === sequenceId ||
          result.sequence_id?.toLowerCase() === sequenceId?.toLowerCase() ||
          result.sequence === sequenceId ||
          result.id === sequenceId

        if (hasTestName && hasSequenceId) {
          console.log('✅ Найден результат:', result)
          return true
        }

        return false
      })

      if (!result) {
        console.log('❌ Результат не найден')
        console.log(
          'Доступные результаты:',
          results.value.map((r) => ({
            test_name: r.test_name,
            sequence_id: r.sequence_id,
            test: r.test,
            sequence: r.sequence,
            id: r.id,
          })),
        )
      }

      return result
    }

    // Получаем класс для ячейки
    const getCellClass = (testName, sequenceId) => {
      const result = findResult(testName, sequenceId)
      if (!result) {
        console.log(`❌ Нет данных для ячейки: ${testName} - ${sequenceId}`)
        return 'cell-empty'
      }

      // Ищем поле статуса в разных возможных вариантах
      const status = (result.status || result.result || result.passed || result.success)
        ?.toString()
        .toUpperCase()

      console.log(`🎨 Статус для ${testName}-${sequenceId}:`, status)

      switch (status) {
        case 'PASS':
        case 'PASSED':
        case 'TRUE':
        case 'SUCCESS':
          return 'cell-success'
        case 'WARNING':
        case 'WARN':
          return 'cell-warning'
        case 'FAIL':
        case 'FAILED':
        case 'FALSE':
        case 'ERROR':
          return 'cell-danger'
        default:
          console.log('❓ Неизвестный статус:', status)
          return 'cell-unknown'
      }
    }

    // Получаем статус для отображения в ячейке
    const getCellStatus = (testName, sequenceId) => {
      const result = findResult(testName, sequenceId)
      if (!result) return '-'

      // Ищем поле статуса в разных возможных вариантах
      const status = (result.status || result.result || result.passed || result.success)
        ?.toString()
        .toUpperCase()

      // Сокращаем для отображения
      switch (status) {
        case 'PASS':
        case 'PASSED':
        case 'TRUE':
        case 'SUCCESS':
          return 'PASS'
        case 'WARNING':
        case 'WARN':
          return 'WARN'
        case 'FAIL':
        case 'FAILED':
        case 'FALSE':
        case 'ERROR':
          return 'FAIL'
        default:
          return status || '?'
      }
    }

    // Получаем детали для tooltip
    const getCellDetails = (testName, sequenceId) => {
      const result = findResult(testName, sequenceId)
      if (!result) return ''

      // Ищем детали в разных возможных полях
      return result.details || result.message || result.info || result.description || ''
    }

    // Форматирование названий тестов
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

    // Форматирование ID (обрезаем для отображения)
    const formatSequenceId = (sequenceId) => {
      return sequenceId.substring(0, 8) + '...'
    }

    // Показ tooltip
    const showTooltip = (event, testName, sequenceId) => {
      tooltip.value = {
        visible: true,
        x: event.clientX + 10,
        y: event.clientY + 10,
        testName,
        sequenceId,
      }
    }

    // Скрытие tooltip
    const hideTooltip = () => {
      tooltip.value.visible = false
    }

    return {
      tooltip,
      testNames,
      sequenceIds,
      results,
      debugInfo,
      sampleResult,
      getCellClass,
      getCellStatus,
      getCellDetails,
      formatTestName,
      formatSequenceId,
      showTooltip,
      hideTooltip,
    }
  },
}
</script>

<style scoped>
.heatmap-chart {
  background: var(--color-bg-elevated);
  border-radius: var(--border-radius-lg);
  padding: var(--spacing-lg);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--color-border);
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-lg);
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

.legend {
  display: flex;
  gap: var(--spacing-md);
  align-items: center;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 6px;
}

.legend-color {
  width: 16px;
  height: 16px;
  border-radius: 4px;
  border: 1px solid rgba(0, 0, 0, 0.1);
}

.legend-color.success {
  background-color: #48bb78;
}

.legend-color.warning {
  background-color: #ed8936;
}

.legend-color.danger {
  background-color: #f56565;
}

.legend-label {
  font-size: 12px;
  color: var(--color-text-muted);
  font-weight: 500;
}

/* Отладочная информация */
.debug-info {
  background: #fff3cd;
  border: 1px solid #ffeaa7;
  border-radius: 4px;
  padding: 8px 12px;
  margin-bottom: 12px;
  font-size: 12px;
  color: #856404;
}

.debug-info p {
  margin: 4px 0;
}

.heatmap-grid {
  display: grid;
  justify-content: center;
  margin: 0 auto;
  background: white;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid var(--color-border);
}

.y-axis-labels {
  display: flex;
  flex-direction: column;
  background: #f8fafc;
  border-right: 1px solid var(--color-border);
  min-width: 150px;
}

.y-label {
  padding: 12px 16px;
  border-bottom: 1px solid var(--color-border);
  font-size: 12px;
  font-weight: 600;
  color: var(--color-border);
  display: flex;
  align-items: center;
  height: 50px;
  box-sizing: border-box;
}

.y-label:last-child {
  border-bottom: none;
}

/* Пустая угловая ячейка для выравнивания */
.empty-corner {
  background: #f8fafc;
  border-bottom: 1px solid var(--color-border);
  height: 50px;
}

.heatmap-content {
  flex: 1;
  overflow-x: auto;
}

.x-axis-labels {
  display: flex;
  background: #f8fafc;
  border-bottom: 1px solid var(--color-border);
  min-width: max-content;
  height: 50px;
}

.x-label {
  padding: 8px 12px;
  border-right: 1px solid var(--color-border);
  font-size: 10px;
  color: var(--color-border);
  text-align: center;
  min-width: 120px;
  cursor: help;
  font-family: 'Share Tech Mono', monospace;
  box-sizing: border-box;
  display: flex;
  align-items: center;
  justify-content: center;
}

.x-label:last-child {
  border-right: none;
}

.heatmap-cells {
  min-width: max-content;
}

.heatmap-row {
  display: flex;
  border-bottom: 1px solid #f1f5f9;
}

.chart-container {
  background: var(--color-bg-elevated);
  width: 1360px;
  margin: auto;
}

.heatmap-row:last-child {
  border-bottom: none;
}

.heatmap-cell {
  min-width: 120px;
  height: 50px;
  border-right: 1px solid #f1f5f9;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
  box-sizing: border-box;
}

.heatmap-cell:last-child {
  border-right: none;
}

.heatmap-cell:hover {
  transform: scale(1.05);
  z-index: 2;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.cell-content {
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* Цвета ячеек */
.cell-empty {
  background-color: #f8fafc;
  color: #cbd5e0;
}

.cell-success {
  background-color: #c6f6d5;
  color: #22543d;
  border-color: #9ae6b4;
}

.cell-warning {
  background-color: #eecc09;
  color: #742a2a;
  border-color: #feb2b2;
}

.cell-danger {
  background-color: #fed7d7;
  color: #742a2a;
  border-color: #feb2b2;
}

.cell-unknown {
  background-color: #edf2f7;
  color: #4a5568;
}

/* Tooltip */
.heatmap-tooltip {
  position: fixed;
  background: rgba(0, 0, 0, 0.9);
  color: white;
  padding: 12px;
  border-radius: 6px;
  font-size: 12px;
  z-index: 1000;
  pointer-events: none;
  max-width: 300px;
  backdrop-filter: blur(4px);
}

.tooltip-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.tooltip-row {
  display: flex;
  gap: 8px;
}

.tooltip-row strong {
  min-width: 80px;
  color: #e2e8f0;
}

.status-pass {
  color: #68d391;
}

.status-warning {
  color: #f6ad55;
}

.status-fail {
  color: #fc8181;
}

/* Адаптивность */
@media (max-width: 768px) {
  .chart-header {
    flex-direction: column;
    gap: var(--spacing-md);
    align-items: flex-start;
  }

  .legend {
    flex-wrap: wrap;
  }

  .y-label {
    font-size: 10px;
    padding: 8px 12px;
  }

  .x-label {
    min-width: 100px;
    font-size: 9px;
  }

  .heatmap-cell {
    min-width: 100px;
  }

  .empty-corner {
    height: 50px;
  }
}
.heatmap-grid {
  display: flex;
  background: white;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid var(--color-border);
}

/* Добавьте этот новый стиль */
.heatmap-content {
  flex: 1;
  overflow-x: auto;
  min-width: 0; /* Важно: предотвращает растягивание */
}

.x-axis-labels {
  display: flex;
  background: #f8fafc;
  border-bottom: 1px solid var(--color-border);
  min-width: max-content;
  height: 50px;
}

/* Обновите стиль x-label */
.x-label {
  padding: 8px 12px;
  border-right: 1px solid var(--color-border);
  font-size: 10px;
  color: var(--color-border);
  text-align: center;
  min-width: 120px; /* Фиксированная ширина */
  width: 120px; /* Фиксированная ширина */
  flex: 0 0 120px; /* Фиксированная ширина без растягивания */
  cursor: help;
  font-family: 'Share Tech Mono', monospace;
  box-sizing: border-box;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Обновите стиль heatmap-cell */
.heatmap-cell {
  min-width: 120px; /* Фиксированная ширина */
  width: 120px; /* Фиксированная ширина */
  flex: 0 0 120px; /* Фиксированная ширина без растягивания */
  height: 50px;
  border-right: 1px solid #f1f5f9;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
  box-sizing: border-box;
}
</style>
