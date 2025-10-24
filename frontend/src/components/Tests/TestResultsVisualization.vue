<template>
  <div class="tests-visualization" v-if="isAnalyzing || analysisComplete">
    <div class="tests-header">
      <h3 class="cyber-heading">
        <span class="text-primary">ВЫПОЛНЕНИЕ ТЕСТОВ</span>
        <span class="completion-badge" v-if="analysisComplete"> ЗАВЕРШЕНО </span>
      </h3>
      <div class="tests-progress">
        <span class="progress-text cyber-mono"> {{ completedTests }}/{{ totalTests }} </span>
        <div class="progress-circle">
          <svg width="60" height="60" viewBox="0 0 60 60">
            <circle
              cx="30"
              cy="30"
              r="27"
              stroke="var(--color-border)"
              stroke-width="3"
              fill="none"
            />
            <circle
              cx="30"
              cy="30"
              r="27"
              stroke="var(--color-primary)"
              stroke-width="3"
              fill="none"
              stroke-linecap="round"
              :stroke-dasharray="circumference"
              :stroke-dashoffset="circumference - (testsProgress / 100) * circumference"
              transform="rotate(-90 30 30)"
            />
          </svg>
          <span class="circle-percent cyber-mono"> {{ Math.round(testsProgress) }}% </span>
        </div>
      </div>
    </div>

    <!-- Список тестов с прогресс-барами -->
    <div class="tests-list">
      <div v-for="test in tests" :key="test.id" class="test-item" :class="test.serverData.result">
        <div class="test-icon">
          <span v-if="test.status === 'pending'">⏳</span>
          <span v-else-if="test.serverData.result === 'running'">⚡</span>
          <span v-else-if="test.serverData.result === 'PASS'">✅</span>
          <span v-else-if="test.serverData.result === 'WARNING'">❌</span>
          <span v-else-if="test.serverData.result === 'FAIL'">❌</span>
          <span v-else-if="test.serverData.result === 'SKIP'">⏭️</span>
        </div>
        <div class="test-content">
          <div class="test-header">
            <span class="test-name cyber-mono">{{ test.name }}</span>
            <div class="test-status-info">
              <span class="test-duration cyber-mono" v-if="test.duration && test.status !== 'skip'">
                {{ test.duration }}мс
              </span>
              <span class="test-skip-badge" v-if="test.status === 'skip'"> ПРОПУЩЕНО </span>
            </div>
          </div>
          <p class="test-description futurism-elegant">
            {{ test.description }}
          </p>

          <!-- Причина пропуска -->
          <div class="skip-reason" v-if="test.status === 'skip' && test.skipReason">
            <span class="skip-reason-text cyber-mono"> 📝 {{ test.skipReason }} </span>
          </div>

          <!-- Прогресс-бар для каждого теста -->
          <div class="test-progress-container">
            <div
              class="test-progress-bar"
              v-if="test.status === 'running' || test.status === 'pending'"
            >
              <div
                class="test-progress-fill"
                :style="{ width: test.progress + '%' }"
                :class="{ animated: test.status === 'running' }"
              ></div>
            </div>

            <!-- Результат теста -->
            <div
              class="test-result"
              v-if="test.result && test.status !== 'skip'"
              :class="test.serverData.result"
            >
              <span class="result-text cyber-mono">{{ test.result }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

// Props
const props = defineProps({
  tests: {
    type: Array,
    required: true,
    default: () => [],
  },
  isAnalyzing: {
    type: Boolean,
    default: false,
  },
  analysisComplete: {
    type: Boolean,
    default: false,
  },
})

// Emits
const emit = defineEmits(['repeat-analysis'])

// Вычисляемые свойства
const totalTests = computed(() => props.tests.length)
const completedTests = computed(
  () =>
    props.tests.filter(
      (test) => test.status === 'success' || test.status === 'error' || test.status === 'skip',
    ).length,
)
const testsProgress = computed(() => (completedTests.value / totalTests.value) * 100)
const passedTests = computed(
  () => props.tests.filter((test) => test.serverData.result === 'PASS').length,
)
const failedTests = computed(
  () => props.tests.filter((test) => test.serverData.result === 'WARNING').length,
)
const skippedTests = computed(
  () => props.tests.filter((test) => test.serverData.result === 'SKIP').length,
) // ИСПРАВЛЕНО: было 'skipped'
console.log(props.tests)
const circumference = computed(() => 2 * Math.PI * 27)
</script>

<style scoped>
.tests-visualization {
  background: var(--color-bg-elevated);
  border-radius: var(--border-radius-lg);
  padding: var(--spacing-xl);
  border: 1px solid var(--color-border);
  box-shadow: var(--shadow-sm);
  height: auto;
  min-height: 500px;
  display: flex;
  flex-direction: column;
}

.tests-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-lg);
  border-bottom: 1px solid var(--color-border);
  padding-bottom: var(--spacing-md);
  flex-shrink: 0;
}

.tests-progress {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}
.test-item.FAIL {
  border-color: var(--color-error);
  background: var(--color-error-soft);
}
.progress-text {
  color: var(--color-text-muted);
  font-size: 0.9rem;
}

.progress-circle {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.circle-percent {
  position: absolute;
  color: var(--color-primary);
  font-weight: var(--font-weight-bold);
  font-size: 0.8rem;
}

.completion-badge {
  background: var(--color-success);
  color: var(--color-text-inverted);
  padding: var(--spacing-xs) var(--spacing-sm);
  border-radius: var(--border-radius-sm);
  font-size: 0.8rem;
  margin-left: var(--spacing-md);
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%,
  100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.8;
    transform: scale(1.05);
  }
}

.tests-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
  flex: 1;
  overflow: visible;
  padding-right: 0;
}

.test-item {
  display: flex;
  gap: var(--spacing-md);
  padding: var(--spacing-md);
  border: 1px solid var(--color-border);
  border-radius: var(--border-radius-md);
  background: var(--color-bg-subtle);
  transition: all var(--transition-normal);
}

.test-item:hover {
  border-color: var(--color-primary);
  transform: translateY(-1px);
  box-shadow: var(--shadow-sm);
}

.test-item.running {
  border-color: var(--color-warning);
  background: var(--color-warning-soft);
}

.test-item.success {
  border-color: var(--color-success);
  background: var(--color-success-soft);
}

.test-item.error {
  border-color: var(--color-error);
  background: var(--color-error-soft);
}

.test-item.SKIP {
  border-color: var(--color-skip);
  background: var(--color-skip-soft);
}

.test-icon {
  font-size: 1.2rem;
  display: flex;
  align-items: flex-start;
  min-width: 24px;
}

.test-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.test-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: var(--spacing-sm);
}

.test-name {
  color: var(--color-text);
  font-weight: var(--font-weight-bold);
  font-size: 0.9rem;
  line-height: 1.2;
}

.test-status-info {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: var(--spacing-xs);
}

.test-duration {
  color: var(--color-text-muted);
  font-size: 0.7rem;
  white-space: nowrap;
}

.test-skip-badge {
  background: var(--color-skip);
  color: var(--color-text-inverted);
  padding: 4px 8px;
  border-radius: var(--border-radius-sm);
  font-size: 0.7rem;
  font-weight: var(--font-weight-bold);
  white-space: nowrap;
}

.test-description {
  color: var(--color-text-light);
  margin: 0;
  font-size: 0.8rem;
  line-height: 1.3;
}

.skip-reason {
  margin-top: 4px;
  padding: 6px 10px;
  background: rgba(var(--color-skip-rgb), 0.1);
  border-radius: var(--border-radius-sm);
  border-left: 3px solid var(--color-skip);
}

.skip-reason-text {
  color: var(--color-skip);
  font-size: 0.75rem;
  line-height: 1.2;
}

.test-progress-container {
  margin-top: var(--spacing-xs);
}

.test-progress-bar {
  width: 100%;
  height: 4px;
  background: var(--color-border);
  border-radius: var(--border-radius-full);
  overflow: hidden;
  margin-bottom: var(--spacing-xs);
}

.test-progress-fill {
  height: 100%;
  background: var(--color-warning);
  border-radius: var(--border-radius-full);
  transition: width var(--transition-slow);
  position: relative;
}

.test-progress-fill.animated {
  background: var(--color-warning);
}

.test-progress-fill.animated::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.6), transparent);
  animation: shimmer 1.5s infinite;
}

@keyframes shimmer {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(100%);
  }
}

.test-result {
  padding: var(--spacing-xs) var(--spacing-sm);
  border-radius: var(--border-radius-sm);
  font-size: 0.7rem;
  text-align: center;
}

.test-result.PASS {
  background: var(--color-success);
  color: var(--color-text-inverted);
}
.test-result.SKIP {
  border-color: var(--color-skip);
  background: var(--color-skip-soft);

  color: var(--color-text);
}
.test-result.WARNING {
  background: var(--color-error);
  color: var(--color-text-inverted);
}
.test-result.FAIL {
  background: var(--color-error);
  color: var(--color-text-inverted);
}

.analysis-results {
  margin-top: var(--spacing-lg);
  padding-top: var(--spacing-lg);
  border-top: 1px solid var(--color-border);
  flex-shrink: 0;
}

.results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-lg);
  gap: var(--spacing-md);
}

.results-summary {
  display: flex;
  gap: var(--spacing-md);
  flex-wrap: wrap;
}

.summary-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-xs);
  padding: var(--spacing-sm);
  border-radius: var(--border-radius-md);
  background: var(--color-bg-subtle);
  border: 1px solid var(--color-border);
  min-width: 70px;
}

.summary-item.success {
  border-color: var(--color-success);
  background: var(--color-success-soft);
}

.summary-item.error {
  border-color: var(--color-error);
  background: var(--color-error-soft);
}

.summary-item.skip {
  border-color: var(--color-skip);
  background: var(--color-skip-soft);
}

.summary-item.total {
  border-color: var(--color-border);
  background: var(--color-bg-elevated);
}

.summary-count {
  font-size: 1.2rem;
  font-weight: var(--font-weight-bold);
  color: var(--color-primary);
}

.summary-item.success .summary-count {
  color: var(--color-success);
}

.summary-item.error .summary-count {
  color: var(--color-error);
}

.summary-item.skip .summary-count {
  color: var(--color-skip);
}

.summary-item.total .summary-count {
  color: var(--color-text);
}

.summary-label {
  color: var(--color-text-muted);
  font-size: 0.7rem;
  text-align: center;
}

.skip-info {
  display: flex;
  align-items: flex-start;
  gap: var(--spacing-md);
  padding: var(--spacing-md);
  background: var(--color-info-soft);
  border: 1px solid var(--color-info);
  border-radius: var(--border-radius-md);
  margin-bottom: var(--spacing-lg);
}

.skip-info-icon {
  font-size: 1.2rem;
  flex-shrink: 0;
}

.skip-info-content {
  flex: 1;
}

.skip-info-text {
  color: var(--color-info);
  font-size: 0.8rem;
  margin: 0;
  line-height: 1.4;
}

.results-actions {
  display: flex;
  justify-content: center;
  margin-top: var(--spacing-lg);
}

.repeat-button {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-md) var(--spacing-lg);
  border: 2px solid var(--color-primary);
  background: var(--color-bg-elevated);
  color: var(--color-primary);
  border-radius: var(--border-radius-md);
  font-weight: var(--font-weight-bold);
  transition: all var(--transition-normal);
  position: relative;
  overflow: hidden;
}

.repeat-button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: var(--color-primary);
  transition: left var(--transition-slow);
  z-index: 1;
}

.repeat-button:hover::before {
  left: 0;
}

.repeat-button:hover {
  color: var(--color-text-inverted);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(var(--color-primary-rgb), 0.2);
}

.repeat-button .button-icon,
.repeat-button .button-text {
  position: relative;
  z-index: 2;
}

/* Адаптивность */
@media (max-width: 768px) {
  .tests-visualization {
    padding: var(--spacing-lg);
    min-height: 450px;
  }

  .tests-header {
    flex-direction: column;
    gap: var(--spacing-md);
    text-align: center;
  }

  .results-header {
    flex-direction: column;
    gap: var(--spacing-md);
    text-align: center;
  }

  .results-summary {
    justify-content: center;
  }

  .test-header {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--spacing-xs);
  }

  .test-status-info {
    align-items: flex-start;
  }
}

@media (max-width: 480px) {
  .tests-visualization {
    padding: var(--spacing-md);
    min-height: 400px;
  }

  .results-summary {
    flex-direction: column;
    gap: var(--spacing-sm);
    width: 100%;
  }

  .summary-item {
    flex-direction: row;
    justify-content: space-between;
    min-width: auto;
  }

  .test-item {
    padding: var(--spacing-sm);
    gap: var(--spacing-sm);
  }

  .test-icon {
    font-size: 1rem;
    min-width: 20px;
  }

  .repeat-button {
    padding: var(--spacing-sm) var(--spacing-md);
    font-size: 0.9rem;
  }

  .skip-info {
    flex-direction: column;
    text-align: center;
    gap: var(--spacing-sm);
  }
}
</style>
