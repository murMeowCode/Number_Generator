<script setup>
import { ref, provide } from 'vue'
import ContainerGenerate from '@/components/Generate/ContainerGenerate.vue'
import MyTest from '@/components/Tests/MyTest.vue'
import TestResultsVisualization from '@/components/Tests/TestResultsVisualization.vue'

// Данные тестов, которые будут передаваться в правую колонку
const tests = ref([
  {
    id: 1,
    name: 'ЧАСТОТНЫЙ ТЕСТ',
    description: 'Анализ распределения частот символов',
    status: 'pending',
    progress: 0,
    duration: null,
    result: null,
  },
  {
    id: 2,
    name: 'ТЕСТ СЕРИЙ',
    description: 'Проверка последовательностей одинаковых символов',
    status: 'pending',
    progress: 0,
    duration: null,
    result: null,
  },
  {
    id: 3,
    name: 'ПОКЕР-ТЕСТ',
    description: 'Анализ комбинаций символов',
    status: 'pending',
    progress: 0,
    duration: null,
    result: null,
  },
  {
    id: 4,
    name: 'ПОСЛЕДОВАТЕЛЬНЫЙ ТЕСТ',
    description: 'Проверка последовательностей символов',
    status: 'pending',
    progress: 0,
    duration: null,
    result: null,
  },
  {
    id: 5,
    name: 'ТЕСТ САМЫХ ДЛИННЫХ СЕРИЙ',
    description: 'Анализ максимальных последовательностей',
    status: 'pending',
    progress: 0,
    duration: null,
    result: null,
  },
  {
    id: 6,
    name: 'ТЕСТ КУМУЛЯТИВНЫХ СУММ',
    description: 'Проверка накопленных сумм',
    status: 'pending',
    progress: 0,
    duration: null,
    result: null,
  },
  {
    id: 7,
    name: 'ТЕСТ АВТОКОРРЕЛЯЦИИ',
    description: 'Анализ корреляции последовательности',
    status: 'pending',
    progress: 0,
    duration: null,
    result: null,
  },
  {
    id: 8,
    name: 'ТЕСТ РАНГА МАТРИЦЫ',
    description: 'Проверка ранга бинарной матрицы',
    status: 'pending',
    progress: 0,
    duration: null,
    result: null,
  },
])

const isAnalyzing = ref(false)
const analysisComplete = ref(false)

// Функции для управления тестами
const startTests = () => {
  isAnalyzing.value = true
  analysisComplete.value = false

  // Сбрасываем тесты перед запуском
  tests.value.forEach((test) => {
    test.status = 'pending'
    test.progress = 0
    test.duration = null
    test.result = null
  })
}

const updateTestProgress = (testId, progress, status = 'running') => {
  const test = tests.value.find((t) => t.id === testId)
  if (test) {
    test.progress = progress
    test.status = status
  }
}

const completeTest = (testId, result, isSuccess = true) => {
  const test = tests.value.find((t) => t.id === testId)
  if (test) {
    test.status = isSuccess ? 'success' : 'error'
    test.result = result
    test.progress = 100
  }
}

const completeAllTests = () => {
  analysisComplete.value = true
  isAnalyzing.value = false
}

const resetAnalysis = () => {
  tests.value.forEach((test) => {
    test.status = 'pending'
    test.progress = 0
    test.duration = null
    test.result = null
  })
  analysisComplete.value = false
  isAnalyzing.value = false
}

// НОВАЯ ФУНКЦИЯ: Обновление данных тестов из дочернего компонента
const setTestResults = (serverResults) => {
  console.log('📊 Получены данные тестов с сервера:', serverResults)

  // Маппинг ключей сервера на ID тестов
  const testMapping = {
    frequency: 1, // Частотный тест
    runs: 2, // Тест серий
    poker: 3, // Покер-тест
    serial: 4, // Последовательный тест
    longest_runs: 5, // Тест самых длинных серий
    cumulative_sums: 6, // Тест кумулятивных сумм
    autocorrelation: 7, // Тест автокорреляции
    matrix_rank: 8, // Тест ранга матрицы
  }

  let hasSkippedTests = false
  let hasCompletedTests = false

  // Обновляем тесты данными с сервера
  Object.entries(serverResults).forEach(([testKey, testData]) => {
    const testId = testMapping[testKey]
    if (testId) {
      const test = tests.value.find((t) => t.id === testId)
      if (test) {
        // Сохраняем исходные данные с сервера
        test.serverData = testData

        // Формируем понятное сообщение для пользователя
        let resultMessage = ''
        let status = 'pending'
        let skipReason = ''

        if (testData) {
          if (testData.result === 'SKIP') {
            // Тест пропущен из-за короткой последовательности
            resultMessage = 'Пропущен'
            status = 'skip'
            skipReason = 'короткая последовательность'
            hasSkippedTests = true
            hasCompletedTests = true
          } else if (testData.result === 'PASS') {
            // Тест пройден успешно
            resultMessage = 'Пройден'
            if (testData.p_value !== null && testData.p_value !== undefined) {
              resultMessage += ` (p-value: ${testData.p_value.toFixed(4)})`
            }
            status = 'success'
            hasCompletedTests = true
          } else if (testData.result === 'FAIL') {
            // Тест не пройден
            resultMessage = 'Не пройден'
            if (testData.p_value !== null && testData.p_value !== undefined) {
              resultMessage += ` (p-value: ${testData.p_value.toFixed(4)})`
            }
            status = 'error'
            hasCompletedTests = true
          } else {
            // Неизвестный статус
            resultMessage = testData.result || 'Неизвестный статус'
            status = 'pending'
          }
        } else {
          resultMessage = 'Данные недоступны'
          status = 'pending'
        }

        // Обновляем результат теста
        test.result = resultMessage
        test.status = status
        test.skipReason = skipReason // Добавляем причину пропуска

        // Если тест пропущен, устанавливаем прогресс 100%
        if (status === 'skip') {
          test.progress = 100
        }

        // Добавляем длительность если есть
        if (testData && testData.duration) {
          test.duration = testData.duration
        }
      }
    }
  })

  console.log('✅ Тесты обновлены данными с сервера')

  // Проверяем, все ли тесты завершены
  const allTestsCompleted = tests.value.every(
    (test) => test.status === 'success' || test.status === 'error' || test.status === 'skip',
  )

  // Если все тесты завершены, обновляем флаги
  if (allTestsCompleted && hasCompletedTests) {
    analysisComplete.value = true
    isAnalyzing.value = false
    console.log('🎯 Все тесты завершены, анализ окончен')
  }

  // Проверяем, есть ли пропущенные тесты
  const skippedTests = tests.value.filter((test) => test.status === 'skip')
  if (skippedTests.length > 0) {
    console.log(`ℹ️ Пропущено тестов: ${skippedTests.length} (короткая последовательность)`)
  }

  // Логируем итоговую статистику
  const passedTests = tests.value.filter((test) => test.status === 'success').length
  const failedTests = tests.value.filter((test) => test.status === 'error').length
  const totalCompleted = tests.value.filter(
    (test) => test.status === 'success' || test.status === 'error' || test.status === 'skip',
  ).length

  console.log(
    `📈 Итоговая статистика: ${passedTests} пройдено, ${failedTests} ошибок, ${skippedTests.length} пропущено, ${totalCompleted}/${tests.value.length} завершено`,
  )
}

// Функция для проверки наличия данных тестов
const hasTestData = () => {
  return tests.value.some(
    (test) =>
      test.status !== 'pending' ||
      test.progress > 0 ||
      test.result !== null ||
      test.serverData !== undefined,
  )
}
// Передаем функции в дочерние компоненты
provide('testControls', {
  tests,
  startTests,
  updateTestProgress,
  completeTest,
  completeAllTests,
  resetAnalysis,
  setTestResults, // ДОБАВЛЯЕМ ЭТУ ФУНКЦИЮ
})
</script>

<template>
  <div class="two-column-layout" data-aos="zoom-in">
    <!-- Левая колонка - управление генерацией -->
    <div class="column left-column">
      <div class="left-column-content">
        <MyTest class="left-component" />
      </div>
    </div>

    <!-- Правая колонка - отображение тестов -->
    <div class="column right-column">
      <!-- Отображение тестов если есть данные -->
      <TestResultsVisualization
        v-if="hasTestData()"
        :tests="tests"
        :is-analyzing="isAnalyzing"
        :analysis-complete="analysisComplete"
        @repeat-analysis="resetAnalysis"
      />

      <!-- Заглушка если нет данных тестов -->
      <div v-else class="tests-placeholder">
        <div class="placeholder-content">
          <div class="placeholder-icon">📊</div>
          <h3 class="placeholder-title">ЗДЕСЬ БУДУТ ОТОБРАЖАТЬСЯ ТЕСТЫ</h3>
          <p class="placeholder-description">
            Сгенерируйте последовательность, чтобы увидеть результаты статистических тестов
          </p>
          <div class="placeholder-features">
            <div class="feature-item">
              <span class="feature-icon">✅</span>
              <span class="feature-text">8 статистических тестов </span>
            </div>
            <div class="feature-item">
              <span class="feature-icon">📈</span>
              <span class="feature-text">Визуализация результатов</span>
            </div>
            <div class="feature-item">
              <span class="feature-icon">⚡</span>
              <span class="feature-text">Реальное время выполнения</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.two-column-layout {
  display: grid;
  grid-template-columns: 1.6fr 1fr;
  gap: var(--spacing-2xl);
  align-items: start;
  min-height: 80vh;
  padding: var(--spacing-xl);
  max-width: 2000px;

  position: relative;
}

.column {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: fit-content;
}

/* Левая колонка - компоненты в строку */
.left-column {
  max-width: 900px;
  display: flex;
  justify-self: end;
}

.left-column-content {
  display: flex;
  flex-direction: row;
  gap: var(--spacing-xl);
  width: 100%;
  align-items: stretch;
}

.left-component {
  flex: 1;
  min-width: 0; /* Для корректного сжатия */
  background: var(--color-bg-elevated);
  border: 1px solid var(--color-border);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-sm);
  padding: var(--spacing-xl);
  transition: all var(--transition-normal);
  display: flex;
  flex-direction: column;
}

.left-component:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}

/* Правая колонка */
.right-column {
  max-width: 600px;
  justify-self: start;
}

.right-column > * {
  background: var(--color-bg-elevated);
  border: 1px solid var(--color-border);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-sm);
  transition: all var(--transition-normal);
  min-height: 600px;
  padding: var(--spacing-xl);
}

.right-column > *:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}

/* Стили для заглушки тестов */
.tests-placeholder {
  border: 2px dashed var(--color-border) !important;
  background: var(--color-bg-subtle) !important;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  min-height: 600px;
  padding: var(--spacing-2xl) !important;
}

.placeholder-content {
  max-width: 400px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-lg);
}

.placeholder-icon {
  font-size: 4rem;
  opacity: 0.7;
  margin-bottom: var(--spacing-md);
}

.placeholder-title {
  color: var(--color-text);
  font-size: 1.5rem;
  font-weight: var(--font-weight-bold);
  text-transform: uppercase;
  letter-spacing: 1px;
  margin: 0;
  line-height: 1.3;
}

.placeholder-description {
  color: var(--color-text-muted);
  font-size: 1rem;
  line-height: 1.5;
  margin: 0;
  opacity: 0.8;
}

.placeholder-features {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
  margin-top: var(--spacing-lg);
  width: 100%;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-sm);
  background: var(--color-bg-elevated);
  border-radius: var(--border-radius-md);
  border: 1px solid var(--color-border);
}

.feature-icon {
  font-size: 1.2rem;
  flex-shrink: 0;
}

.feature-text {
  color: var(--color-text);
  font-size: 0.9rem;
  font-weight: var(--font-weight-medium);
}

/* Анимация для заглушки */
.tests-placeholder {
  animation: pulse-glow 3s ease-in-out infinite;
}

@keyframes pulse-glow {
  0%,
  100% {
    border-color: var(--color-border);
    box-shadow: var(--shadow-sm);
  }
  50% {
    border-color: var(--color-primary);
    box-shadow: 0 0 20px rgba(var(--color-primary-rgb), 0.1);
  }
}

/* Декоративная линия разделения */
.two-column-layout::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 1px;
  height: 80%;
  background: var(--color-border);
  opacity: 0.4;
}

/* Анимация появления */
.left-column {
  animation: slideInLeft 0.6s ease-out;
}

.right-column {
  animation: slideInRight 0.6s ease-out;
}

@keyframes slideInLeft {
  from {
    opacity: 0;
    transform: translateX(-30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

/* Адаптивность для планшетов */
@media (max-width: 1200px) {
  .two-column-layout {
    grid-template-columns: 1fr;
    gap: var(--spacing-xl);
    padding: var(--spacing-lg);
    min-height: auto;
  }

  .left-column,
  .right-column {
    max-width: 100%;
    justify-self: center;
  }

  .left-column-content {
    max-width: 800px;
    margin: 0 auto;
  }

  .two-column-layout::before {
    display: none;
  }

  .right-column > * {
    min-height: auto;
  }

  .tests-placeholder {
    min-height: 400px;
    padding: var(--spacing-xl) !important;
  }

  /* Изменяем анимацию для мобильных */
  .left-column,
  .right-column {
    animation: fadeInUp 0.6s ease-out;
  }

  .right-column {
    animation-delay: 0.1s;
  }
}

/* Адаптивность для мобильных устройств */
@media (max-width: 768px) {
  .two-column-layout {
    padding: var(--spacing-md);
    gap: var(--spacing-lg);
  }

  .left-column-content {
    flex-direction: column;
    gap: var(--spacing-lg);
  }

  .left-component {
    padding: var(--spacing-lg);
  }

  .right-column > * {
    padding: var(--spacing-lg);
  }

  .tests-placeholder {
    min-height: 350px;
    padding: var(--spacing-lg) !important;
  }

  .placeholder-icon {
    font-size: 3rem;
  }

  .placeholder-title {
    font-size: 1.3rem;
  }

  .placeholder-description {
    font-size: 0.9rem;
  }
}

/* Для очень маленьких экранов */
@media (max-width: 480px) {
  .two-column-layout {
    padding: var(--spacing-sm);
    gap: var(--spacing-md);
  }

  .left-component {
    padding: var(--spacing-md);
  }

  .right-column > * {
    padding: var(--spacing-md);
  }

  .tests-placeholder {
    min-height: 300px;
    padding: var(--spacing-md) !important;
  }

  .placeholder-content {
    gap: var(--spacing-md);
  }

  .placeholder-icon {
    font-size: 2.5rem;
    margin-bottom: var(--spacing-sm);
  }

  .placeholder-title {
    font-size: 1.1rem;
  }

  .placeholder-description {
    font-size: 0.85rem;
  }

  .feature-item {
    padding: var(--spacing-xs);
  }

  .feature-text {
    font-size: 0.8rem;
  }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Дополнительные стили для лучшего визуального разделения */
.left-component:first-child {
  border-left: 3px solid var(--color-primary);
}

.left-component:last-child {
  border-left: 3px solid var(--color-accent);
}

/* Выравнивание контента внутри компонентов */
.left-component > * {
  flex: 1;
  display: flex;
  flex-direction: column;
}

/* Гарантируем одинаковую высоту компонентов в строке */
.left-column-content {
  align-items: stretch;
}
</style>
