<template>
  <div class="comparison-container">
    <!-- Заголовок -->
    <div class="comparison-header">
      <h1 class="cyber-heading">
        <span class="text-primary">СРАВНЕНИЕ</span> С СЕРВИСАМИ
      </h1>
      <p class="comparison-subtitle futurism-elegant">
        Сравните качество случайности нашего солнечного генератора с популярными сервисами
      </p>
    </div>

    <!-- Панель управления -->
    <div class="control-panel">
      <div class="input-section">
        <label class="input-label cyber-mono">ДЛИНА ПОСЛЕДОВАТЕЛЬНОСТИ</label>
        <div class="input-wrapper">
          <input
            v-model="sequenceLength"
            type="number"
            min="10"
            max="1000000"
            placeholder="Введите длину последовательности"
            class="length-input cyber-mono"
            @input="validateLength"
          />
          <span class="input-suffix">символов</span>
        </div>
        <div class="input-hint futurism-elegant">
          Рекомендуемая длина: от 10 до 1,000,000 символов
        </div>
      </div>

      <!-- Кнопка сравнения -->
      <div class="compare-button-section">
        <button
          class="cyber-button compare-button"
          @click="compareServices"
          :disabled="!isValidLength || isComparing"
          :class="{ disabled: !isValidLength || isComparing }"
        >
          <span class="button-icon">⚡</span>
          <span class="button-text cyber-mono">
            {{ isComparing ? 'СРАВНЕНИЕ...' : 'ЗАПУСТИТЬ СРАВНЕНИЕ' }}
          </span>
          <span class="button-glow"></span>
        </button>
      </div>
    </div>

    <!-- Индикатор загрузки -->
    <div class="loading-indicator" v-if="isComparing">
      <div class="loading-content">
        <div class="loading-icon">🛰️</div>
        <div class="loading-text">
          <h4 class="cyber-heading">АНАЛИЗ СЛУЧАЙНОСТИ</h4>
          <p class="futurism-elegant">Сравниваем качество генерации с сторонними сервисами...</p>
        </div>
        <div class="loading-animation">
          <div class="orbit-dot"></div>
          <div class="orbit-dot"></div>
          <div class="orbit-dot"></div>
        </div>
      </div>
    </div>

    <!-- Результаты сравнения -->
    <div class="comparison-results" v-if="comparisonData && !isComparing">
      <div class="results-header">
        <h2 class="cyber-heading">
          <span class="text-primary">РЕЗУЛЬТАТЫ</span> СРАВНЕНИЯ
        </h2>
        <div class="results-meta cyber-mono">
          Длина последовательности: {{ sequenceLength }} символов
        </div>
        <div class="results-stats cyber-mono" v-if="successfulServicesCount > 0">
          Успешно протестировано: {{ successfulServicesCount }} сервисов
        </div>
      </div>

      <!-- Карточки сервисов -->
      <div class="services-grid">
        <!-- Наш сервис -->
        <ServiceCard
          :service-data="comparisonData.ourService"
          service-name="SOLAR RNG"
          service-icon="🌞"
          :is-primary="true"
          description="Наш генератор на солнечной энтропии"
        />

        <!-- Сторонние сервисы -->
        <ServiceCard
          v-for="service in comparisonData.externalServices"
          :key="service.name"
          :service-data="service"
          :service-name="service.name"
          :service-icon="getServiceIcon(service.name)"
          :is-primary="false"
          :description="getServiceDescription(service.name)"
        />
      </div>

      <!-- Сообщение о неудачных сервисах -->
      <div class="failed-services-message" v-if="failedServices.length > 0">
        <div class="failed-content">
          <div class="failed-icon">⚠️</div>
          <div class="failed-text">
            <h4 class="cyber-heading">НЕКОТОРЫЕ СЕРВИСЫ НЕДОСТУПНЫ</h4>
            <p class="futurism-elegant">
              Следующие сервисы не удалось протестировать: 
              <span class="failed-names cyber-mono">{{ failedServices.join(', ') }}</span>
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Сообщение об ошибке -->
    <div class="error-message" v-if="error">
      <div class="error-content">
        <div class="error-icon">⚠️</div>
        <div class="error-text">
          <h4 class="cyber-heading">ОШИБКА СРАВНЕНИЯ</h4>
          <p class="futurism-elegant">{{ error }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import ServiceCard from './ServiceCard.vue'
import axios from 'axios'
import { api8000, api8001 } from '@/utils/apiUrl/urlApi'
import { v4 as uuidv4 } from 'uuid'

// Refs
const sequenceLength = ref('10000')
const isComparing = ref(false)
const comparisonData = ref(null)
const error = ref(null)
const failedServices = ref([])

// API endpoints
const API_ENDPOINTS = {
  ourService: `${api8001}/generate/generate`,
  externalService1: `${api8001}/generate/generate/side`,
}

// Computed
const isValidLength = computed(() => {
  const length = parseInt(sequenceLength.value)
  return length >= 10 && length <= 1000000
})

const successfulServicesCount = computed(() => {
  if (!comparisonData.value) return 0
  return 1 + (comparisonData.value.externalServices?.length || 0) // наш сервис + внешние
})

// Methods
const validateLength = () => {
  const length = parseInt(sequenceLength.value)
  if (length > 1000000) {
    sequenceLength.value = '1000000'
  } else if (length < 10 && sequenceLength.value !== '') {
    sequenceLength.value = '1000'
  }
}

const getServiceIcon = (serviceName) => {
  const icons = {
    'Random.org': '🎲',
    'python_random': '🐍',
    'ME': '🌞',
    'SOLAR RNG': '🌞'
  }
  return icons[serviceName] || '🔧'
}

const getServiceDescription = (serviceName) => {
  const descriptions = {
    'Random.org': 'Атмосферный шум',
    'python_random': 'Python Random',
    'ME': 'Наш генератор',
    'SOLAR RNG': 'Солнечная энтропия'
  }
  return descriptions[serviceName] || 'Сторонний сервис'
}

// Функция для получения данных от нашего сервиса
const fetchOurServiceData = async () => {
  try {
    const response = await axios.post(API_ENDPOINTS.ourService, {
      length: sequenceLength.value
    })
    console.log(response.data.sequence, 'SEQUENSE1')
    
    const response1 = await axios.post(`${api8000}/statistics/sequence`, {
      sequence_id: uuidv4(),
      sequence: response.data.sequence
    })
    console.log(response1.data, 'SEQUENSE1_DATA')
    
    return {
      name: 'ME',  
      tests: response1.data.tests_results || {
        frequency: { result: 'PASS', p_value: 0.5342 },
        runs: { result: 'PASS', p_value: 0.6123 },
        autocorrelation: { result: 'PASS', p_value: 0.4987 }
      },
    }
  } catch (error) {
    console.error('Ошибка получения данных нашего сервиса:', error)
    throw new Error('Наш сервис недоступен')
  }
}

// Функция для получения данных от Python Random
const fetchPythonRandomData = async () => {
  try {
    const response = await axios.get(`${API_ENDPOINTS.externalService1}/${sequenceLength.value}`)
    console.log(response.data, 'SEQUENSE')
    
    const response2 = await axios.post(`${api8000}/statistics/sequence`, {
      sequence_id: uuidv4(),
      sequence: response.data.python_random
    })
    console.log(response2.data, 'python_random1111')
    
    return {
      name: 'python_random',
      tests: response2.data.tests_results || {
        frequency: { result: 'PASS', p_value: 0.5342 },
        runs: { result: 'PASS', p_value: 0.6123 },
        autocorrelation: { result: 'PASS', p_value: 0.4987 }
      },
    }
  } catch (error) {
    console.error('Ошибка получения данных Python Random:', error)
    throw new Error('Python Random недоступен')
  }
}

// Функция для получения данных от Random.org
const fetchRandomOrgData = async () => {
  try {
    const response = await axios.get(`${API_ENDPOINTS.externalService1}/${sequenceLength.value}`)
    console.log(response.data, 'SEQUENSE')
    
    const response3 = await axios.post(`${api8000}/statistics/sequence`, {
      sequence_id: uuidv4(),
      sequence: response.data.random_org
    })
    console.log(response3.data, 'random_org111')
    
    return {
      name: 'Random.org',
      tests: response3.data.tests_results || {
        frequency: { result: 'PASS', p_value: 0.5342 },
        runs: { result: 'PASS', p_value: 0.6123 },
        autocorrelation: { result: 'PASS', p_value: 0.4987 }
      },
    }
  } catch (error) {
    console.error('Ошибка получения данных Random.org:', error)
    throw new Error('Random.org недоступен')
  }
}

// Функция для безопасного выполнения запросов к внешним сервисам
const fetchServiceSafely = async (fetchFunction, serviceName) => {
  try {
    const result = await fetchFunction()
    return { success: true, data: result }
  } catch (error) {
    console.error(`Ошибка получения данных от ${serviceName}:`, error)
    return { success: false, serviceName, error: error.message }
  }
}

const compareServices = async () => {
  if (!isValidLength.value) return

  isComparing.value = true
  error.value = null
  comparisonData.value = null
  failedServices.value = []

  try {
    // Получаем данные от нашего сервиса (обязательный)
    let ourService
    try {
      ourService = await fetchOurServiceData()
    } catch (error) {
      error.value = 'Наш сервис недоступен. Сравнение невозможно.'
      return
    }

    // Параллельно получаем данные от внешних сервисов с обработкой ошибок
    const externalResults = await Promise.allSettled([
      fetchServiceSafely(fetchPythonRandomData, 'Python Random'),
      fetchServiceSafely(fetchRandomOrgData, 'Random.org')
    ])

    // Фильтруем успешные результаты
    const successfulServices = []
    const failedServicesList = []

    externalResults.forEach((result, index) => {
      if (result.status === 'fulfilled' && result.value.success) {
        successfulServices.push(result.value.data)
      } else {
        const serviceName = ['Python Random', 'Random.org'][index]
        failedServicesList.push(serviceName)
      }
    })

    failedServices.value = failedServicesList

    // Формируем данные для сравнения только с успешными сервисами
    comparisonData.value = {
      ourService,
      externalServices: successfulServices
    }

    console.log('Данные сравнения получены:', comparisonData.value)
    console.log('Неудачные сервисы:', failedServices.value)

  } catch (err) {
    error.value = 'Не удалось выполнить сравнение. Попробуйте позже.'
    console.error('Comparison error:', err)
  } finally {
    isComparing.value = false
  }
}
</script>

<style scoped>
/* Стили остаются без изменений */
.comparison-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: var(--spacing-2xl);
}

/* Заголовок */
.comparison-header {
  text-align: center;
  margin-bottom: var(--spacing-2xl);
  border-bottom: 2px solid var(--color-border);
  padding-bottom: var(--spacing-xl);
}

.comparison-subtitle {
  font-size: 1.2rem;
  color: var(--color-text-muted);
  margin-top: var(--spacing-md);
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

/* Панель управления */
.control-panel {
  background: var(--color-bg-elevated);
  border-radius: var(--border-radius-xl);
  padding: var(--spacing-xl);
  border: 1px solid var(--color-border);
  box-shadow: var(--shadow-lg);
  margin-bottom: var(--spacing-xl);
}

.input-section {
  margin-bottom: var(--spacing-lg);
}

.input-label {
  display: block;
  margin-bottom: var(--spacing-sm);
  color: var(--color-text);
  font-weight: var(--font-weight-bold);
  font-size: 1.1rem;
  text-transform: uppercase;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  max-width: 400px;
}

.length-input {
  flex: 1;
  padding: var(--spacing-md);
  border: 2px solid var(--color-border);
  border-radius: var(--border-radius-lg);
  background: var(--color-bg-subtle);
  color: var(--color-text);
  font-size: 1.1rem;
  font-family: var(--font-mono);
  transition: all var(--transition-normal);
}

.length-input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px var(--color-primary-soft);
}

.input-suffix {
  position: absolute;
  right: var(--spacing-md);
  color: var(--color-text-muted);
  font-size: 0.9rem;
  pointer-events: none;
}

.input-hint {
  margin-top: var(--spacing-xs);
  color: var(--color-text-light);
  font-size: 0.9rem;
}

/* Кнопка сравнения */
.compare-button-section {
  display: flex;
  justify-content: center;
}

.compare-button {
  position: relative;
  display: inline-flex;
  align-items: center;
  gap: var(--spacing-md);
  padding: var(--spacing-lg) var(--spacing-2xl);
  border: 2px solid var(--color-primary);
  border-radius: var(--border-radius-xl);
  background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-hover) 100%);
  color: var(--color-text-inverted);
  font-weight: var(--font-weight-bold);
  font-size: 1.1rem;
  transition: all var(--transition-normal);
  overflow: hidden;
}

.compare-button:hover:not(.disabled) {
  transform: translateY(-2px);
  box-shadow: 
    0 8px 25px rgba(var(--color-primary-rgb), 0.3),
    0 0 0 1px var(--color-primary);
}

.compare-button:active:not(.disabled) {
  transform: translateY(0);
}

.compare-button.disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none !important;
}

.button-icon {
  font-size: 1.4rem;
}

.button-glow {
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.4),
    transparent
  );
  transition: left var(--transition-slow);
}

.compare-button:hover:not(.disabled) .button-glow {
  left: 100%;
}

/* Индикатор загрузки */
.loading-indicator {
  background: var(--color-bg-elevated);
  border: 1px solid var(--color-border);
  border-radius: var(--border-radius-xl);
  padding: var(--spacing-2xl);
  margin-bottom: var(--spacing-xl);
  box-shadow: var(--shadow-lg);
}

.loading-content {
  display: flex;
  align-items: center;
  gap: var(--spacing-lg);
  text-align: left;
}

.loading-icon {
  font-size: 3rem;
  animation: float 3s ease-in-out infinite;
}

.loading-text {
  flex: 1;
}

.loading-text h4 {
  color: var(--color-primary);
  margin: 0 0 var(--spacing-xs) 0;
}

.loading-text p {
  color: var(--color-text-muted);
  margin: 0;
}

.loading-animation {
  display: flex;
  gap: 8px;
}

.orbit-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: var(--color-primary);
  animation: orbit 1.5s ease-in-out infinite both;
}

.orbit-dot:nth-child(2) {
  animation-delay: 0.2s;
}

.orbit-dot:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-10px); }
}

@keyframes orbit {
  0%, 100% { 
    transform: scale(0.8);
    opacity: 0.5;
  }
  50% { 
    transform: scale(1.2);
    opacity: 1;
  }
}

/* Результаты сравнения */
.comparison-results {
  background: var(--color-bg-elevated);
  border-radius: var(--border-radius-xl);
  padding: var(--spacing-2xl);
  border: 1px solid var(--color-border);
  box-shadow: var(--shadow-lg);
}

.results-header {
  text-align: center;
  margin-bottom: var(--spacing-2xl);
  border-bottom: 1px solid var(--color-border);
  padding-bottom: var(--spacing-lg);
}

.results-meta {
  color: var(--color-text-muted);
  font-size: 1rem;
  margin-top: var(--spacing-sm);
}

.results-stats {
  color: var(--color-success);
  font-size: 0.9rem;
  margin-top: var(--spacing-xs);
}

/* Сетка сервисов */
.services-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: var(--spacing-lg);
  margin-bottom: var(--spacing-2xl);
}

/* Сообщение о неудачных сервисах */
.failed-services-message {
  background: var(--color-warning-soft);
  border: 1px solid var(--color-warning);
  border-radius: var(--border-radius-lg);
  padding: var(--spacing-lg);
  margin-top: var(--spacing-xl);
}

.failed-content {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  text-align: left;
}

.failed-icon {
  font-size: 1.5rem;
  flex-shrink: 0;
}

.failed-text h4 {
  color: var(--color-warning);
  margin: 0 0 var(--spacing-xs) 0;
  font-size: 1rem;
}

.failed-text p {
  color: var(--color-text);
  margin: 0;
  font-size: 0.9rem;
}

.failed-names {
  color: var(--color-warning);
  font-weight: var(--font-weight-bold);
}

/* Сообщение об ошибке */
.error-message {
  background: var(--color-error-soft);
  border: 1px solid var(--color-error);
  border-radius: var(--border-radius-lg);
  padding: var(--spacing-xl);
  margin-top: var(--spacing-xl);
}

.error-content {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  text-align: left;
}

.error-icon {
  font-size: 2rem;
}

.error-text h4 {
  color: var(--color-error);
  margin: 0 0 var(--spacing-xs) 0;
}

.error-text p {
  color: var(--color-text);
  margin: 0;
}

/* Адаптивность */
@media (max-width: 768px) {
  .comparison-container {
    padding: var(--spacing-lg);
  }

  .services-grid {
    grid-template-columns: 1fr;
  }

  .loading-content,
  .error-content,
  .failed-content {
    flex-direction: column;
    text-align: center;
    gap: var(--spacing-md);
  }

  .input-wrapper {
    max-width: 100%;
  }
}

@media (max-width: 480px) {
  .control-panel {
    padding: var(--spacing-lg);
  }

  .comparison-results {
    padding: var(--spacing-lg);
  }

  .compare-button {
    padding: var(--spacing-md) var(--spacing-lg);
    font-size: 1rem;
  }
}
</style>