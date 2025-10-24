<template>
  <div class="service-card" :class="{ 'service-card--primary': isPrimary }">
    <!-- Заголовок карточки -->
    <div class="card-header">
      <div class="service-icon">{{ serviceIcon }}</div>
      <div class="service-info">
        <h3 class="service-name cyber-heading">{{ serviceName }}</h3>
        <p class="service-description futurism-elegant">{{ description }}</p>
      </div>
    </div>

    <!-- Основные метрики -->
    <div class="metrics-grid" v-if="showMetrics">
      <div class="metric-item">
        <span class="metric-label cyber-mono">ЭНТРОПИЯ</span>
        <span class="metric-value cyber-dynamic">{{ formattedEntropy }}</span>
        <div class="metric-bar">
          <div class="metric-fill" :style="{ width: entropyPercentage + '%' }"></div>
        </div>
      </div>
      <div class="metric-item">
        <span class="metric-label cyber-mono">СКОРОСТЬ</span>
        <span class="metric-value cyber-dynamic">{{ serviceData.speed }} зн/с</span>
        <div class="metric-bar">
          <div class="metric-fill" :style="{ width: speedPercentage + '%' }"></div>
        </div>
      </div>
      <div class="metric-item">
        <span class="metric-label cyber-mono">ОЦЕНКА</span>
        <span class="metric-value score-value cyber-dynamic">{{ serviceData.score }}/10</span>
        <div class="metric-bar">
          <div class="metric-fill" :style="{ width: scorePercentage + '%' }"></div>
        </div>
      </div>
    </div>

    <!-- Результаты тестов - теперь показываем все 8 тестов как в основном компоненте -->
    <div class="tests-section">
      <h4 class="tests-title cyber-mono">СТАТИСТИЧЕСКИЕ ТЕСТЫ</h4>
      
      <!-- Список тестов -->
      <div class="tests-list">
        <div 
          v-for="test in serviceTests" 
          :key="test.id"
          class="test-item"
          :class="getTestStatusClass(test.status)"
        >
          <!-- Индикатор прогресса -->
          <div class="test-progress-indicator">
            <div class="progress-circle">
              <div 
                class="progress-fill" 
                :style="{ transform: `rotate(${test.progress * 3.6}deg)` }"
              ></div>
              <div class="progress-text cyber-mono">
                {{ test.progress }}%
              </div>
            </div>
          </div>

          <!-- Информация о тесте -->
          <div class="test-info">
            <div class="test-header">
              <h5 class="test-name cyber-heading">{{ test.name }}</h5>
              <div class="test-status" :class="getStatusClass(test.status)">
                {{ getStatusText(test.status) }}
              </div>
            </div>
            <p class="test-description futurism-elegant">{{ test.description }}</p>
            
            <!-- Результат теста -->
            <div v-if="test.result" class="test-result">
              <span class="result-text cyber-mono">{{ test.result }}</span>
              <span v-if="test.duration" class="test-duration cyber-mono">
                {{ test.duration }}мс
              </span>
            </div>

            <!-- Причина пропуска -->
            <div v-if="test.skipReason" class="skip-reason futurism-elegant">
              {{ test.skipReason }}
            </div>

            <!-- Детали ошибки -->
            <div v-if="test.errorDetails" class="error-details futurism-elegant">
              {{ test.errorDetails }}
            </div>
          </div>

          <!-- Иконка статуса -->
          <div class="test-status-icon">
            <span v-if="test.status === 'success'">✅</span>
            <span v-else-if="test.status === 'error'">❌</span>
            <span v-else-if="test.status === 'skip'">⏭️</span>
            <span v-else-if="test.status === 'running'">⚡</span>
            <span v-else>⏳</span>
          </div>
        </div>
      </div>

      <!-- Сводка по тестам -->
      <div class="tests-summary" v-if="showSummary">
        <div class="summary-stats">
          <div class="stat-item">
            <span class="stat-value cyber-dynamic">{{ passedTests }}</span>
            <span class="stat-label cyber-mono">ПРОЙДЕНО</span>
          </div>
          <div class="stat-item">
            <span class="stat-value cyber-dynamic">{{ failedTests }}</span>
            <span class="stat-label cyber-mono">ОШИБОК</span>
          </div>
          <div class="stat-item">
            <span class="stat-value cyber-dynamic">{{ skippedTests }}</span>
            <span class="stat-label cyber-mono">ПРОПУЩЕНО</span>
          </div>
          <div class="stat-item">
            <span class="stat-value cyber-dynamic">{{ totalTests }}</span>
            <span class="stat-label cyber-mono">ВСЕГО</span>
          </div>
        </div>
      </div>

      <!-- Сообщение об ошибках -->
      <div class="error-message" v-if="hasErrors && showErrorSummary">
        <div class="error-content">
          <div class="error-icon">⚠️</div>
          <div class="error-text">
            <h5 class="cyber-heading">НЕКОТОРЫЕ ТЕСТЫ НЕ ПРОЙДЕНЫ</h5>
            <p class="futurism-elegant">
              {{ failedTests }} из {{ totalTests }} тестов завершились с ошибкой. 
              Остальные тесты выполнены успешно.
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Бейдж лучшего сервиса -->
    <div class="best-badge" v-if="isPrimary && serviceData.score >= 9.5">
      <span class="badge-icon">🏆</span>
      <span class="badge-text cyber-mono">ЛУЧШИЙ РЕЗУЛЬТАТ</span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  serviceData: {
    type: Object,
    required: true
  },
  serviceName: {
    type: String,
    required: true
  },
  serviceIcon: {
    type: String,
    default: '🔧'
  },
  isPrimary: {
    type: Boolean,
    default: false
  },
  description: {
    type: String,
    default: ''
  },
  showErrorSummary: {
    type: Boolean,
    default: true
  }
})

// Вычисляемые свойства для метрик
const formattedEntropy = computed(() => {
  return props.serviceData.entropy?.toFixed(4) || '0.0000'
})

const entropyPercentage = computed(() => {
  return (props.serviceData.entropy || 0) * 100
})

const speedPercentage = computed(() => {
  const maxSpeed = 2000 // Максимальная ожидаемая скорость
  return Math.min((props.serviceData.speed / maxSpeed) * 100, 100)
})

const scorePercentage = computed(() => {
  return (props.serviceData.score / 10) * 100
})

const showMetrics = computed(() => {
  return props.serviceData.entropy !== undefined && 
         props.serviceData.speed !== undefined && 
         props.serviceData.score !== undefined
})

// Преобразуем данные сервиса в формат тестов
const serviceTests = computed(() => {
  // Если в serviceData уже есть тесты в нужном формате, используем их
  if (props.serviceData.tests && Array.isArray(props.serviceData.tests)) {
    return props.serviceData.tests
  }

  // Иначе создаем тесты из данных сервиса
  const testMapping = {
    frequency: {
      id: 1,
      name: 'ЧАСТОТНЫЙ ТЕСТ',
      description: 'Анализ распределения частот символов'
    },
    runs: {
      id: 2,
      name: 'ТЕСТ СЕРИЙ',
      description: 'Проверка последовательностей одинаковых символов'
    },
    poker: {
      id: 3,
      name: 'ПОКЕР-ТЕСТ',
      description: 'Анализ комбинаций символов'
    },
    serial: {
      id: 4,
      name: 'ПОСЛЕДОВАТЕЛЬНЫЙ ТЕСТ',
      description: 'Проверка последовательностей символов'
    },
    longest_runs: {
      id: 5,
      name: 'ТЕСТ САМЫХ ДЛИННЫХ СЕРИЙ',
      description: 'Анализ максимальных последовательностей'
    },
    cumulative_sums: {
      id: 6,
      name: 'ТЕСТ КУМУЛЯТИВНЫХ СУММ',
      description: 'Проверка накопленных сумм'
    },
    autocorrelation: {
      id: 7,
      name: 'ТЕСТ АВТОКОРРЕЛЯЦИИ',
      description: 'Анализ корреляции последовательности'
    },
    matrix_rank: {
      id: 8,
      name: 'ТЕСТ РАНГА МАТРИЦЫ',
      description: 'Проверка ранга бинарной матрицы'
    }
  }

  // Создаем массив тестов
  return Object.entries(testMapping).map(([key, testInfo]) => {
    const testData = props.serviceData.tests?.[key]
    
    let status = 'pending'
    let progress = 0
    let result = null
    let duration = null
    let skipReason = ''
    let errorDetails = ''

    if (testData) {
      if (testData.result === 'SKIP') {
        status = 'skip'
        progress = 100
        result = 'Пропущен'
        skipReason = testData.reason || 'короткая последовательность'
      } else if (testData.result === 'PASS') {
        status = 'success'
        progress = 100
        result = 'Пройден'
        if (testData.p_value !== null && testData.p_value !== undefined) {
          result += ` (p-value: ${testData.p_value.toFixed(4)})`
        }
      } else if (testData.result === 'FAIL') {
        status = 'error'
        progress = 100
        result = 'Не пройден'
        if (testData.p_value !== null && testData.p_value !== undefined) {
          result += ` (p-value: ${testData.p_value.toFixed(4)})`
        }
        errorDetails = testData.error_message || 'Тест не пройден по статистическим критериям'
      } else if (testData.result === 'RUNNING') {
        status = 'running'
        progress = testData.progress || 50
        result = 'Выполняется...'
      } else {
        // Если статус неизвестен, но данные есть - считаем выполненным
        status = 'success'
        progress = 100
        result = 'Завершен'
      }

      duration = testData.duration || null
    } else {
      // Если данных нет, но сервис завершил работу
      if (props.serviceData.status === 'completed') {
        status = 'success'
        progress = 100
        result = 'Завершен (данные недоступны)'
      }
    }

    return {
      ...testInfo,
      status,
      progress,
      result,
      duration,
      skipReason,
      errorDetails,
      serverData: testData
    }
  })
})

// Вычисляемые свойства для сводки
const passedTests = computed(() => 
  serviceTests.value.filter(test => test.status === 'success').length
)

const failedTests = computed(() => 
  serviceTests.value.filter(test => test.status === 'error').length
)

const skippedTests = computed(() => 
  serviceTests.value.filter(test => test.status === 'skip').length
)

const totalTests = computed(() => serviceTests.value.length)

const hasErrors = computed(() => failedTests.value > 0)

const showSummary = computed(() => 
  serviceTests.value.some(test => 
    test.status === 'success' || test.status === 'error' || test.status === 'skip'
  )
)

// Методы
const getStatusClass = (status) => {
  const classes = {
    success: 'status-success',
    error: 'status-error',
    skip: 'status-skip',
    running: 'status-running',
    pending: 'status-pending'
  }
  return classes[status] || 'status-pending'
}

const getStatusText = (status) => {
  const texts = {
    success: 'УСПЕХ',
    error: 'ОШИБКА',
    skip: 'ПРОПУЩЕН',
    running: 'ВЫПОЛНЯЕТСЯ',
    pending: 'ОЖИДАНИЕ'
  }
  return texts[status] || 'ОЖИДАНИЕ'
}

const getTestStatusClass = (status) => {
  return `test-item--${status}`
}
</script>

<style scoped>
.service-card {
  position: relative;
  background: var(--color-bg-subtle);
  border: 1px solid var(--color-border);
  border-radius: var(--border-radius-xl);
  padding: var(--spacing-lg);
  transition: all var(--transition-normal);
  box-shadow: var(--shadow-md);
}

.service-card--primary {
  background: var(--color-primary-soft);
  border-color: var(--color-primary-muted);
  box-shadow: 
    var(--shadow-lg),
    0 0 30px rgba(var(--color-primary-rgb), 0.1);
}

.service-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-xl);
}

.service-card--primary:hover {
  box-shadow: 
    var(--shadow-xl),
    0 0 40px rgba(var(--color-primary-rgb), 0.2);
}

/* Заголовок карточки */
.card-header {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-lg);
}

.service-icon {
  font-size: 2.5rem;
  flex-shrink: 0;
}

.service-info {
  flex: 1;
}

.service-name {
  font-size: 1.3rem;
  margin: 0 0 var(--spacing-xs) 0;
  color: var(--color-text);
}

.service-card--primary .service-name {
  color: var(--color-primary);
}

.service-description {
  color: var(--color-text-muted);
  font-size: 0.9rem;
  margin: 0;
}

/* Метрики */
.metrics-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-lg);
}

.metric-item {
  text-align: center;
}

.metric-label {
  display: block;
  color: var(--color-text-muted);
  font-size: 0.7rem;
  text-transform: uppercase;
  margin-bottom: var(--spacing-xs);
}

.metric-value {
  color: var(--color-text);
  font-size: 1.1rem;
  font-weight: var(--font-weight-bold);
  margin-bottom: var(--spacing-xs);
}

.service-card--primary .metric-value {
  color: var(--color-primary);
}

.score-value {
  color: var(--color-success) !important;
}

.metric-bar {
  width: 100%;
  height: 4px;
  background: var(--color-border);
  border-radius: var(--border-radius-full);
  overflow: hidden;
}

.metric-fill {
  height: 100%;
  background: var(--color-primary);
  border-radius: var(--border-radius-full);
  transition: width var(--transition-slow);
}

.service-card--primary .metric-fill {
  background: var(--color-primary);
}

/* Секция тестов */
.tests-section {
  border-top: 1px solid var(--color-border);
  padding-top: var(--spacing-md);
}

.tests-title {
  color: var(--color-text-muted);
  font-size: 0.8rem;
  text-transform: uppercase;
  margin-bottom: var(--spacing-md);
}

.tests-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
  margin-bottom: var(--spacing-md);
}

/* Элемент теста */
.test-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  padding: var(--spacing-sm);
  border-radius: var(--border-radius-md);
  border: 1px solid var(--color-border);
  background: var(--color-bg-elevated);
  transition: all var(--transition-normal);
}

/* Статусы тестов */
.test-item--success {
  border-left: 3px solid var(--color-success);
  background: var(--color-success-soft);
}

.test-item--error {
  border-left: 3px solid var(--color-error);
  background: var(--color-error-soft);
}

.test-item--skip {
  border-left: 3px solid var(--color-warning);
  background: var(--color-warning-soft);
}

.test-item--running {
  border-left: 3px solid var(--color-primary);
  background: var(--color-primary-soft);
  animation: pulse-running 2s ease-in-out infinite;
}

.test-item--pending {
  border-left: 3px solid var(--color-border);
  opacity: 0.7;
}

@keyframes pulse-running {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.8; }
}

/* Индикатор прогресса */
.test-progress-indicator {
  flex-shrink: 0;
}

.progress-circle {
  position: relative;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--color-bg);
  border: 2px solid var(--color-border);
  display: flex;
  align-items: center;
  justify-content: center;
}

.progress-fill {
  position: absolute;
  top: -2px;
  left: -2px;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: conic-gradient(var(--color-primary) 0%, var(--color-border) 0%);
  mask: radial-gradient(transparent 55%, black 56%);
  -webkit-mask: radial-gradient(transparent 55%, black 56%);
}

.progress-text {
  font-size: 0.6rem;
  font-weight: var(--font-weight-bold);
  color: var(--color-text);
}

/* Информация о тесте */
.test-info {
  flex: 1;
  min-width: 0;
}

.test-header {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  margin-bottom: var(--spacing-xs);
}

.test-name {
  font-size: 0.8rem;
  margin: 0;
  color: var(--color-text);
}

.test-status {
  font-size: 0.6rem;
  padding: 2px 6px;
  border-radius: var(--border-radius-sm);
  font-weight: var(--font-weight-bold);
  text-transform: uppercase;
}

.status-success {
  background: var(--color-success);
  color: var(--color-text-inverted);
}

.status-error {
  background: var(--color-error);
  color: var(--color-text-inverted);
}

.status-skip {
  background: var(--color-warning);
  color: var(--color-text-inverted);
}

.status-running {
  background: var(--color-primary);
  color: var(--color-text-inverted);
}

.status-pending {
  background: var(--color-border);
  color: var(--color-text);
}

.test-description {
  font-size: 0.7rem;
  color: var(--color-text-muted);
  margin: 0 0 var(--spacing-xs) 0;
  line-height: 1.3;
}

.test-result {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  margin-bottom: var(--spacing-xs);
}

.result-text {
  font-size: 0.7rem;
  color: var(--color-text);
  font-weight: var(--font-weight-medium);
}

.test-duration {
  font-size: 0.6rem;
  color: var(--color-text-light);
}

.skip-reason {
  font-size: 0.7rem;
  color: var(--color-warning);
  font-style: italic;
}

.error-details {
  font-size: 0.7rem;
  color: var(--color-error);
  font-style: italic;
  margin-top: var(--spacing-xs);
}

/* Иконка статуса */
.test-status-icon {
  flex-shrink: 0;
  font-size: 1rem;
}

/* Сводка тестов */
.tests-summary {
  border-top: 1px solid var(--color-border);
  padding-top: var(--spacing-md);
  margin-bottom: var(--spacing-md);
}

.summary-stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--spacing-sm);
}

.stat-item {
  text-align: center;
  padding: var(--spacing-sm);
  background: var(--color-bg-elevated);
  border-radius: var(--border-radius-md);
  border: 1px solid var(--color-border);
}

.stat-value {
  display: block;
  font-size: 1.2rem;
  font-weight: var(--font-weight-bold);
  color: var(--color-primary);
  margin-bottom: var(--spacing-xs);
}

.stat-label {
  font-size: 0.6rem;
  color: var(--color-text-muted);
  text-transform: uppercase;
}

/* Сообщение об ошибках */
.error-message {
  background: var(--color-error-soft);
  border: 1px solid var(--color-error);
  border-radius: var(--border-radius-md);
  padding: var(--spacing-md);
  margin-top: var(--spacing-md);
}

.error-content {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.error-icon {
  font-size: 1.2rem;
  flex-shrink: 0;
}

.error-text h5 {
  color: var(--color-error);
  margin: 0 0 var(--spacing-xs) 0;
  font-size: 0.8rem;
}

.error-text p {
  color: var(--color-text);
  margin: 0;
  font-size: 0.7rem;
}

/* Бейдж лучшего сервиса */
.best-badge {
  position: absolute;
  top: -10px;
  right: -10px;
  background: linear-gradient(135deg, var(--color-warning) 0%, #ffd700 100%);
  color: var(--color-text-inverted);
  padding: var(--spacing-xs) var(--spacing-sm);
  border-radius: var(--border-radius-full);
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  box-shadow: var(--shadow-md);
  animation: pulse 2s ease-in-out infinite;
}

.badge-icon {
  font-size: 0.8rem;
}

.badge-text {
  font-size: 0.6rem;
  font-weight: var(--font-weight-bold);
  text-transform: uppercase;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

/* Адаптивность */
@media (max-width: 768px) {
  .metrics-grid {
    grid-template-columns: 1fr;
    gap: var(--spacing-sm);
  }

  .card-header {
    flex-direction: column;
    text-align: center;
    gap: var(--spacing-sm);
  }

  .test-item {
    flex-direction: column;
    align-items: stretch;
    gap: var(--spacing-sm);
  }

  .test-header {
    justify-content: space-between;
  }

  .summary-stats {
    grid-template-columns: repeat(2, 1fr);
  }

  .error-content {
    flex-direction: column;
    text-align: center;
    gap: var(--spacing-sm);
  }
}

@media (max-width: 480px) {
  .service-card {
    padding: var(--spacing-md);
  }

  .metrics-grid {
    gap: var(--spacing-xs);
  }

  .metric-value {
    font-size: 1rem;
  }

  .test-item {
    padding: var(--spacing-xs);
  }

  .summary-stats {
    grid-template-columns: 1fr;
  }
}
</style>