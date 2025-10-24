<template>
  <div class="file-upload-container">
    <!-- Заголовок -->
    <div class="upload-header">
      <span class="text-primary">АНАЛИЗ ФАЙЛОВ</span>
    </div>

    <!-- Основной контейнер -->
    <div class="upload-main">
      <!-- Зона загрузки файла -->
      <div
        class="upload-zone"
        :class="{
          'drag-over': dragOver,
          'has-file': uploadedFile,
          uploading: isUploading,
        }"
        @drop="onDrop"
        @dragover="onDragOver"
        @dragleave="onDragLeave"
      >
        <!-- Контент загрузки - всегда видимый -->
        <div class="upload-content" v-if="!isUploading && !waitingForTests">
          <div class="upload-icon">📁</div>
          <h3 class="upload-title cyber-heading">ПЕРЕТАЩИТЕ ФАЙЛ СЮДА</h3>
          <p class="upload-description futurism-elegant">или нажмите для выбора файла</p>

          <!-- Единая красивая кнопка выбора файла -->
          <div class="file-select-wrapper">
            <input
              type="file"
              ref="fileInput"
              @change="onFileSelect"
              class="file-input"
              accept="*/*"
            />
            <button
              class="cyber-button file-select-button"
              @click="triggerFileInput"
              :class="{
                primary: !uploadedFile,
                accent: uploadedFile && !isAnalyzing,
                success: uploadedFile && analysisComplete,
              }"
            >
              <span class="button-icon">
                <span v-if="!uploadedFile">🔍</span>
                <span v-else-if="uploadedFile && !analysisComplete">📄</span>
                <span v-else>✅</span>
              </span>
              <span class="button-text">
                <span v-if="!uploadedFile">ВЫБРАТЬ ФАЙЛ</span>
                <span v-else-if="uploadedFile && !analysisComplete">{{ uploadedFile.name }}</span>
                <span v-else>ФАЙЛ ЗАГРУЖЕН</span>
              </span>
              <span class="file-size" v-if="uploadedFile">
                {{ formatFileSize(uploadedFile.size) }}
              </span>
            </button>
          </div>

          <!-- Кнопка начала анализа -->
          <button
            class="cyber-button start-analysis-button"
            @click="startAnalysis"
            :disabled="!uploadedFile || isAnalyzing"
            v-if="uploadedFile && !analysisComplete"
          >
            <span class="button-icon">⚡</span>
            <span class="button-text">НАЧАТЬ АНАЛИЗ</span>
          </button>

          <!-- Кнопка нового анализа -->
          <button
            class="cyber-button new-analysis-button"
            @click="resetUpload"
            v-if="analysisComplete"
          >
            <span class="button-icon">🔄</span>
            <span class="button-text">НОВЫЙ АНАЛИЗ</span>
          </button>
        </div>

        <!-- Прогресс загрузки на сервер -->
        <div class="upload-progress" v-if="isUploading">
          <div class="progress-icon">🔄</div>
          <h4 class="progress-title cyber-heading">ЗАГРУЗКА ФАЙЛА НА СЕРВЕР</h4>
          <h4 class="progress-title cyber-heading">ОЖИДАЙТЕ, ЗАНИМАЕТ НЕ БОЛЕЕ МИНУТЫ</h4>
          <div class="progress-bar">
            <div class="progress-fill" :style="{ width: uploadProgress + '%' }"></div>
          </div>
          <p class="progress-percent cyber-mono">{{ Math.round(uploadProgress) }}%</p>
        </div>

        <!-- Ожидание запуска тестов -->
        <div class="waiting-tests" v-if="waitingForTests">
          <div class="waiting-icon">⏳</div>
          <h4 class="waiting-title cyber-heading">ОЖИДАНИЕ ЗАПУСКА ТЕСТОВ</h4>
          <p class="waiting-description futurism-elegant">
            Файл загружен, запускаем тесты на сервере...
          </p>
          <div class="loading-dots">
            <span></span>
            <span></span>
            <span></span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { api8000 } from '@/utils/apiUrl/urlApi'
import { ref, inject } from 'vue'
import { useApiMutations } from '@/utils/api/useApiMutation'
import { useNotificationsStore } from '@/stores/useToastStore'
import axios from 'axios'

// Refs
const fileInput = ref(null)
const dragOver = ref(false)
const uploadedFile = ref(null)
const isUploading = ref(false)
const uploadProgress = ref(0)
const isAnalyzing = ref(false)
const analysisComplete = ref(false)
const waitingForTests = ref(false)
const { usePost } = useApiMutations()

// Инъекция функций управления тестами из главного компонента
const { startTests, updateTestProgress, completeTest, completeAllTests, setTestResults } =
  inject('testControls')
const notifications = useNotificationsStore()

// Мутация для загрузки файла
const serverFileMutation = usePost(`${api8000}/statistics/file`, {
  headers: {
    'Content-Type': 'multipart/form-data',
  },
  onSuccess: (data) => {
    console.log('✅ Файл успешно загружен:', data)
    isUploading.value = false
    waitingForTests.value = true
  },
  onError: (error) => {
    console.error('❌ Ошибка загрузки файла:', error)
    isUploading.value = false
    notifications.error('Ошибка при загрузке файла', 'Попробуйте еще раз')
  },
})

// Методы
const triggerFileInput = () => {
  fileInput.value?.click()
}

const onFileSelect = (event) => {
  const file = event.target.files[0]
  if (file) {
    handleFile(file)
  }
}

const onDragOver = (event) => {
  event.preventDefault()
  dragOver.value = true
}

const onDragLeave = () => {
  dragOver.value = false
}

const onDrop = (event) => {
  event.preventDefault()
  dragOver.value = false

  const file = event.dataTransfer.files[0]
  if (file) {
    handleFile(file)
  }
}

const handleFile = (file) => {
  uploadedFile.value = file
  if (!analysisComplete.value) {
    resetAnalysis()
  }
}

const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

const startAnalysis = async () => {
  if (!uploadedFile.value) return

  // 1. Загрузка файла на сервер
  isUploading.value = true
  const serverData = await uploadFileToServer()

  // 2. Ожидание запуска тестов на бэкенде
  waitingForTests.value = true

  // 3. ПЕРЕДАЕМ ДАННЫЕ ТЕСТОВ В РОДИТЕЛЬСКИЙ КОМПОНЕНТ
  if (serverData.tests_results && setTestResults) {
    isUploading.value = false
    setTestResults(serverData.tests_results)
  }

  // 4. Запуск визуализации тестов с реальными данными
  waitingForTests.value = false
  isAnalyzing.value = true

  // Запуск тестов с реальными данными
  await runFileTests(serverData.tests_results)
}

const uploadFileToServer = async () => {
  if (!uploadedFile.value) return

  try {
    const formData = new FormData()
    formData.append('file', uploadedFile.value)

    // Прогресс загрузки
    const progressInterval = setInterval(() => {
      if (uploadProgress.value < 90) {
        uploadProgress.value += 10
      }
    }, 200)

    // Отправка файла
    const response = await axios.post(`${api8000}/statistics/file`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })

    clearInterval(progressInterval)
    uploadProgress.value = 100

    console.log('Данные с сервера:', response.data)

    return response.data
  } catch (error) {
    console.error('❌ Ошибка загрузки файла:', error)
    isUploading.value = false
    throw error
  }
}

const runFileTests = async (testsResults) => {
  // Запускаем тесты через инъекцию из главного компонента
  startTests()

  // Список тестов с русскими названиями и задержками
  const tests = [
    { key: 'frequency', name: 'Частотный тест', delay: 80 },
    { key: 'runs', name: 'Тест серий', delay: 90 },
    { key: 'poker', name: 'Покер-тест', delay: 70 },
    { key: 'serial', name: 'Последовательный тест', delay: 85 },
    { key: 'longest_runs', name: 'Тест самых длинных серий', delay: 75 },
    { key: 'cumulative_sums', name: 'Тест кумулятивных сумм', delay: 80 },
    { key: 'autocorrelation', name: 'Тест автокорреляции', delay: 90 },
    { key: 'matrix_rank', name: 'Тест ранга матрицы', delay: 70 },
  ]

  // Запускаем каждый тест
  for (let i = 0; i < tests.length; i++) {
    const { key, name, delay } = tests[i]
    const testData = testsResults?.[key]

    // Прогресс для текущего теста
    for (let j = 0; j <= 100; j += 10) {
      await new Promise((resolve) => setTimeout(resolve, delay))
      updateTestProgress(i + 1, j)
    }

    // Формируем сообщение на основе данных теста
    let message = name
    let success = false

    if (testData) {
      message += `: ${testData.result}`
      if (testData.p_value !== null && testData.p_value !== undefined) {
        message += ` (p-value: ${testData.p_value})`
      }

      // Определяем успешность теста
      success = testData.result === 'PASS' || testData.result === 'SKIP'
    } else {
      message += ': Данные недоступны'
    }

    completeTest(i + 1, message, success)
  }

  // Завершаем все тесты
  completeAllTests()
  analysisComplete.value = true
  isAnalyzing.value = false
}

const resetAnalysis = () => {
  analysisComplete.value = false
  isAnalyzing.value = false
  waitingForTests.value = false
  uploadProgress.value = 0
}

const resetUpload = () => {
  uploadedFile.value = null
  resetAnalysis()
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}
</script>

<style scoped>
/* Стили остаются без изменений */
.file-upload-container {
  width: 100%;
  margin: 0 auto;
}

.upload-header {
  text-align: center;
  margin-bottom: var(--spacing-xl);
  border-bottom: 2px solid var(--color-border);
  padding-bottom: var(--spacing-md);
}

.main-title {
  font-size: 1.6rem;
  margin-bottom: var(--spacing-xs);
}

.upload-subtitle {
  color: var(--color-text-muted);
  font-size: 0.9rem;
}

.upload-main {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.upload-zone {
  border: 3px dashed var(--color-border);
  border-radius: var(--border-radius-lg);
  padding: var(--spacing-xl);
  text-align: center;
  transition: all var(--transition-normal);
  background: var(--color-bg-elevated);
  position: relative;
  min-height: 180px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.upload-zone.drag-over {
  border-color: var(--color-primary);
  background: var(--color-primary-soft);
  transform: scale(1.02);
}

.upload-zone.has-file {
  border-color: var(--color-success);
  background: var(--color-success-soft);
}

.upload-zone.uploading {
  border-color: var(--color-warning);
  background: var(--color-warning-soft);
}

.file-select-wrapper {
  position: relative;
  margin: var(--spacing-md) 0;
}

.file-input {
  display: none;
}

.file-select-button {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-xs);
  padding: var(--spacing-md) var(--spacing-lg);
  min-width: 240px;
  transition: all var(--transition-normal);
  border: 2px solid;
  border-radius: var(--border-radius-md);
  background: var(--color-bg-elevated);
  position: relative;
  overflow: hidden;
}

.file-select-button.primary {
  border-color: var(--color-primary);
  color: var(--color-primary);
}

.file-select-button.accent {
  border-color: var(--color-accent);
  color: var(--color-accent);
}

.file-select-button.success {
  border-color: var(--color-success);
  color: var(--color-success);
}

.file-select-button:not(.disabled):hover {
  background: var(--color-primary);
  border-color: var(--color-primary);
  color: var(--color-text-inverted);
  transform: translateY(-1px);
}

.file-select-button .button-text {
  font-weight: var(--font-weight-bold);
  font-size: 0.9rem;
  text-align: center;
}

.file-select-button .file-size {
  font-size: 0.7rem;
  opacity: 0.8;
  font-family: var(--font-mono);
}

.start-analysis-button,
.new-analysis-button {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-sm) var(--spacing-md);
  margin-top: var(--spacing-md);
  font-weight: var(--font-weight-bold);
  font-size: 0.8rem;
}

.start-analysis-button {
  background: var(--color-warning);
  border-color: var(--color-warning);
  color: var(--color-text-inverted);
}

.start-analysis-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none !important;
}

.start-analysis-button:not(:disabled):hover {
  background: var(--color-warning-dark);
  border-color: var(--color-warning-dark);
}

.new-analysis-button {
  background: var(--color-info);
  border-color: var(--color-info);
  color: var(--color-text-inverted);
}

.new-analysis-button:hover {
  background: var(--color-info-dark);
  border-color: var(--color-info-dark);
}

.upload-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-md);
  width: 100%;
}

.upload-icon {
  font-size: 2rem;
  opacity: 0.7;
}

.upload-title {
  color: var(--color-text);
  margin: 0;
  font-size: 1.1rem;
}

.upload-description {
  color: var(--color-text-muted);
  margin: 0;
  font-size: 0.8rem;
}

.waiting-tests {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-sm);
  width: 100%;
}

.waiting-icon {
  font-size: 2rem;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%,
  100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.7;
    transform: scale(1.1);
  }
}

.waiting-title {
  color: var(--color-text);
  margin: 0;
  font-size: 1rem;
}

.waiting-description {
  color: var(--color-text-muted);
  margin: 0;
  font-size: 0.8rem;
}

.loading-dots {
  display: flex;
  gap: 4px;
}

.loading-dots span {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--color-primary);
  animation: bounce 1.4s infinite ease-in-out;
}

.loading-dots span:nth-child(1) {
  animation-delay: -0.32s;
}
.loading-dots span:nth-child(2) {
  animation-delay: -0.16s;
}

@keyframes bounce {
  0%,
  80%,
  100% {
    transform: scale(0.8);
    opacity: 0.5;
  }
  40% {
    transform: scale(1);
    opacity: 1;
  }
}

.upload-progress {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-sm);
  width: 100%;
}

.progress-icon {
  font-size: 1.5rem;
  animation: spin 2s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.progress-title {
  color: var(--color-text);
  margin: 0;
  font-size: 0.9rem;
}

.progress-bar {
  width: 100%;
  height: 6px;
  background: var(--color-bg-subtle);
  border-radius: var(--border-radius-full);
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: var(--color-warning);
  border-radius: var(--border-radius-full);
  transition: width var(--transition-normal);
}

.progress-percent {
  color: var(--color-warning);
  font-weight: var(--font-weight-bold);
  font-size: 0.8rem;
}

/* Адаптивность */
@media (max-width: 768px) {
  .upload-zone {
    padding: var(--spacing-lg);
    min-height: 160px;
  }

  .file-select-button {
    min-width: 200px;
    padding: var(--spacing-sm) var(--spacing-md);
  }

  .file-select-button .button-text {
    font-size: 0.8rem;
  }
}

@media (max-width: 480px) {
  .upload-zone {
    padding: var(--spacing-md);
    min-height: 140px;
  }

  .file-select-button {
    min-width: 180px;
  }

  .upload-icon {
    font-size: 1.5rem;
  }

  .upload-title {
    font-size: 1rem;
  }
}
</style>
