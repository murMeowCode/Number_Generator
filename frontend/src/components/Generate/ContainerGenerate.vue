<template>
  <div class="generator-container">
    <!-- Заголовок -->
    <div class="generator-header">
      <span class="text-primary">ГЕНЕРАТОР ПОСЛЕДОВАТЕЛЬНОСТЕЙ</span>
    </div>

    <!-- Основной контейнер -->
    <div class="generator-main">
      <!-- Панель управления -->
      <div class="control-panel">
        <!-- Переключатель режима -->
        <div class="mode-switcher">
          <div class="mode-buttons">
            <button
              class="mode-button"
              :class="{ active: generationMode === 'web' }"
              @click="switchMode('web')"
            >
              <span class="mode-icon">🎯</span>
              <span class="mode-text">Выигрышные числа</span>
            </button>
            <button
              class="mode-button"
              :class="{ active: generationMode === 'txt' }"
              @click="switchMode('txt')"
            >
              <span class="mode-icon">📄</span>
              <span class="mode-text">Случайная последовательность</span>
            </button>
          </div>
        </div>

        <!-- Параметры для WEB режима -->
        <div class="web-params" v-if="generationMode === 'web'">
          <div class="params-grid">
            <div class="param-group">
              <label class="param-label cyber-mono"> КОЛИЧЕСТВО ЧИСЕЛ </label>
              <input
                v-model="winNumbersCount"
                type="number"
                min="1"
                max="1000000"
                class="param-input cyber-mono"
              />
            </div>
            <div class="param-group">
              <label class="param-label cyber-mono"> ДИАПАЗОН ОТ </label>
              <input
                v-model="rangeFrom"
                type="number"
                min="1"
                max="1000"
                class="param-input cyber-mono"
                @input="validateRange"
              />
            </div>
            <div class="param-group">
              <label class="param-label cyber-mono"> ДИАПАЗОН ДО </label>
              <input
                v-model="rangeTo"
                type="number"
                min="1"
                max="1000"
                class="param-input cyber-mono"
                @input="validateRange"
              />
            </div>
          </div>
        </div>

        <!-- Параметры для TXT режима -->
        <div class="txt-params" v-if="generationMode === 'txt'">
          <div class="input-section">
            <label class="input-label cyber-mono"> ДЛИНА ПОСЛЕДОВАТЕЛЬНОСТИ </label>
            <div class="input-wrapper">
              <input
                v-model="sequenceLength"
                type="number"
                min="1"
                max="1000000"
                placeholder="Введите длину"
                class="length-input cyber-mono"
                @input="validateLength"
              />
              <span class="input-suffix">символов</span>
            </div>
            <div class="input-hint futurism-elegant">Введите число от 1 до 1 000 000</div>
          </div>
        </div>

        <!-- Кнопки генерации -->
        <div class="generation-buttons">
          <button
            class="cyber-button generate-button"
            @click="generateSequence"
            :disabled="!isValidParams || isGenerating"
            :class="{ disabled: !isValidParams || isGenerating }"
          >
            <span class="button-icon">{{ generationMode === 'web' ? '🎯' : '📄' }}</span>
            <span class="button-text">
              {{ generationMode === 'web' ? 'СГЕНЕРИРОВАТЬ ЧИСЛА' : 'СГЕНЕРИРОВАТЬ ФАЙЛ' }}
            </span>
          </button>
        </div>

        <!-- Статус генерации -->
        <div class="generation-status" v-if="generationStatus">
          <div class="status-indicator" :class="statusType">
            <span class="status-icon">{{ statusIcon }}</span>
            <span class="status-text cyber-mono">{{ generationStatus }}</span>
          </div>
        </div>

        <!-- Индикатор запуска тестов -->
        <div class="tests-start-indicator" v-if="isTestsStarting">
          <div class="indicator-content">
            <div class="indicator-icon">⚡</div>
            <div class="indicator-text">
              <h4 class="indicator-title">ЗАПУСК СТАТИСТИЧЕСКИХ ТЕСТОВ</h4>
              <p class="indicator-description">Проверка случайности последовательности...</p>
            </div>
            <div class="indicator-animation">
              <div class="pulse-dot"></div>
              <div class="pulse-dot"></div>
              <div class="pulse-dot"></div>
            </div>
          </div>
        </div>
      </div>

      <!-- Результаты генерации -->
      <div class="generation-results" v-if="generatedSequence || downloadedFile">
        <!-- Результат WEB генерации -->
        <div class="web-result" v-if="generatedSequence && !downloadedFile">
          <div class="result-header">
            <h3 class="cyber-heading">
              <span class="text-primary">ВЫИГРЫШНЫЕ ЧИСЛА</span>
            </h3>
          </div>

          <!-- Основная последовательность -->
          <div class="sequence-preview">
            <pre class="sequence-text cyber-mono">{{ generatedSequence }}</pre>
          </div>

          <!-- Отображение дополнительной информации -->
          <div class="additional-info" v-if="entropyData || initialFillData">
            <div class="info-grid">
              <!-- Энтропия от солнца -->
              <div class="info-item" v-if="entropyData">
                <label class="info-label cyber-mono">ЭНТРОПИЯ ОТ СОЛНЦА</label>
                <div class="info-value cyber-mono entropy-value">
                  {{ entropyData || 'Не доступно' }}
                </div>
                <div class="info-hint futurism-elegant">
                  Случайное значение, полученное от приёмника солнечного излучения
                </div>
              </div>

              <!-- Начальное заполнение -->
              <div class="info-item" v-if="initialFillData">
                <label class="info-label cyber-mono">НАЧАЛЬНОЕ ЗАПОЛНЕНИЕ В ДЕСЯТИЧНОМ ВИДЕ</label>
                <div class="info-value cyber-mono initial-fill-value">
                  {{ initialFillData || 'Не доступно' }}
                </div>
                <div class="info-hint futurism-elegant">
                  Исходное состояние генератора перед созданием последовательности
                </div>
              </div>
            </div>
          </div>

          <!-- Блок верификации энтропии -->
          <div class="verification-section">
            <div class="verification-header">
              <h3 class="cyber-heading">
                <span class="text-primary">ВЕРИФИКАЦИЯ ЛОТЕРЕИ</span>
              </h3>
            </div>

            <div class="verification-content">
              <!-- Поле ввода энтропии -->
              <div class="verification-input-group">
                <label class="verification-label cyber-mono">ВВЕДИТЕ ЗНАЧЕНИЕ ЭНТРОПИИ</label>
                <div class="entropy-input-wrapper">
                  <input
                    v-model="entropyValue"
                    type="text"
                    placeholder="Введите энтропию для верификации"
                    class="param-input cyber-mono entropy-input"
                    :class="{ verified: isEntropyVerified }"
                  />
                  <button
                    class="verify-button cyber-mono"
                    @click="verifyEntropy"
                    :disabled="!entropyValue || isVerifying"
                    :class="{
                      disabled: !entropyValue || isVerifying,
                      verified: isEntropyVerified,
                    }"
                  >
                    <span class="verify-icon">{{ isEntropyVerified ? '✅' : '🔍' }}</span>
                    <span class="verify-text">
                      {{ isEntropyVerified ? 'ВЕРИФИЦИРОВАНО' : 'ВЕРИФИЦИРОВАТЬ' }}
                    </span>
                  </button>
                </div>
                <div class="verification-hint futurism-elegant">
                  {{
                    isEntropyVerified
                      ? 'Энтропия успешно верифицирована'
                      : 'Введите значение энтропии для проверки'
                  }}
                </div>
              </div>

              <!-- Статус верификации -->
              <div class="verification-status" v-if="entropyValue">
                <div class="status-item">
                  <label class="status-label cyber-mono">СТАТУС ВЕРИФИКАЦИИ</label>
                  <div
                    class="status-value cyber-mono"
                    :class="isEntropyVerified ? 'verified' : 'not-verified'"
                  >
                    {{ isEntropyVerified ? '✅ ВЕРИФИЦИРОВАНО' : '❌ НЕ ВЕРИФИЦИРОВАНО' }}
                  </div>
                  <div class="status-details futurism-elegant" v-if="verificationResult">
                    {{ verificationResult }}
                  </div>
                </div>

                <!-- Отображение верифицированной последовательности -->
                <div class="verified-sequence" v-if="verifiedSequence && isEntropyVerified">
                  <div class="status-item">
                    <label class="status-label cyber-mono"
                      >ВЕРИФИЦИРОВАННАЯ ПОСЛЕДОВАТЕЛЬНОСТЬ</label
                    >
                    <div class="info-value cyber-mono verified-sequence-value">
                      {{ verifiedSequence }}
                    </div>
                    <div class="info-hint futurism-elegant">
                      Последовательность, полученная при верификации энтропии
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Информация о скачанном файле -->
        <div class="download-result" v-if="downloadedFile">
          <div class="result-header">
            <h3 class="cyber-heading">
              <span class="text-primary">ФАЙЛ УСПЕШНО СКАЧАН</span>
            </h3>
            <div class="file-info">
              <div class="file-icon">📄</div>
              <div class="file-details">
                <h4 class="file-name cyber-heading">{{ downloadedFile.name }}</h4>
                <p class="file-size cyber-mono">
                  {{ formatFileSize(downloadedFile.size) }}
                </p>
              </div>
            </div>
          </div>
          <div class="download-actions">
            <button class="cyber-button primary" @click="generateSequence">
              <span class="button-icon">🔄</span>
              <span class="button-text">СКАЧАТЬ СНОВА</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, inject, provide } from 'vue'
import { useApiMutations } from '@/utils/api/useApiMutation'
import { api8000, api8001 } from '@/utils/apiUrl/urlApi'
import axios from 'axios'

const { usePost } = useApiMutations()

// Refs
const generationMode = ref('web') // 'web' или 'txt'
const sequenceLength = ref('')
const isGenerating = ref(false)
const generatedSequence = ref('')
const downloadedFile = ref(null)
const copySuccess = ref(false)
const generationStatus = ref('')
const isTestsStarting = ref(false) // Флаг запуска тестов

// Настройки для выигрышных чисел (WEB)
const winNumbersCount = ref(6) // Количество выигрышных чисел
const rangeFrom = ref(1) // Диапазон от
const rangeTo = ref(49) // Диапазон до

// Новые поля для энтропии
const entropyValue = ref('') // Введенное пользователем значение энтропии
const isEntropyVerified = ref(false) // Статус верификации
const isVerifying = ref(false) // Флаг процесса верификации
const entropyData = ref(null) // Данные энтропии от сервера
const initialFillData = ref(null) // Данные начального заполнения
const verificationResult = ref('') // Результат верификации
const verifiedSequence = ref('') // Последовательность, полученная при верификации

// Инъекция функций управления тестами из главного компонента
const { startTests, updateTestProgress, completeTest, completeAllTests, setTestResults,  } =
  inject('testControls')

// Вычисляемые свойства
const isValidParams = computed(() => {
  if (generationMode.value === 'web') {
    return (
      winNumbersCount.value > 0 &&
      rangeFrom.value > 0 &&
      rangeTo.value > 0 &&
      rangeFrom.value <= rangeTo.value &&
      winNumbersCount.value <= rangeTo.value - rangeFrom.value + 1
    )
  } else {
    const length = parseInt(sequenceLength.value)
    return length > 0 && length <= 1000000
  }
})

const statusType = computed(() => {
  if (isGenerating.value) return 'running'
  if (generatedSequence.value || downloadedFile.value) return 'success'
  return 'idle'
})

const statusIcon = computed(() => {
  switch (statusType.value) {
    case 'running':
      return '⚡'
    case 'success':
      return '✅'
    default:
      return '⏸'
  }
})

// Метод переключения режима
const switchMode = (mode) => {
  generationMode.value = mode
  
  // Очищаем все результаты и тесты при переключении режима
  setTestResults(null)

}

// Метод очистки результатов
const clearResults = () => {
  generatedSequence.value = ''
  downloadedFile.value = null
  generationStatus.value = ''
  isTestsStarting.value = false
  entropyValue.value = ''
  isEntropyVerified.value = false
  isVerifying.value = false
  entropyData.value = null
  initialFillData.value = null
  verificationResult.value = ''
  verifiedSequence.value = ''
}

// Методы
const validateLength = () => {
  const length = parseInt(sequenceLength.value)
  if (length > 1000000) {
    sequenceLength.value = '10000'
  } else if (length < 1 && sequenceLength.value !== '') {
    sequenceLength.value = '1'
  }
}

const validateRange = () => {
  // Гарантируем, что "от" не больше "до"
  if (parseInt(rangeFrom.value) > parseInt(rangeTo.value)) {
    rangeTo.value = rangeFrom.value
  }

  // Ограничиваем максимальные значения
  if (rangeFrom.value > 1000) rangeFrom.value = 1000
  if (rangeTo.value > 1000) rangeTo.value = 1000
  if (rangeFrom.value < 1) rangeFrom.value = 1
  if (rangeTo.value < 1) rangeTo.value = 1
}

// Функция для сравнения двух последовательностей чисел
const compareSequences = (seq1, seq2) => {
  if (!seq1 || !seq2) return false

  try {
    // Преобразуем обе последовательности в массивы чисел
    const numbers1 = seq1.split('|').map((num) => parseInt(num.trim()))
    const numbers2 = seq2.split('|').map((num) => parseInt(num.trim()))

    // Сортируем оба массива для сравнения
    const sorted1 = [...numbers1].sort((a, b) => a - b)
    const sorted2 = [...numbers2].sort((a, b) => a - b)

    // Сравниваем массивы
    if (sorted1.length !== sorted2.length) return false

    for (let i = 0; i < sorted1.length; i++) {
      if (sorted1[i] !== sorted2[i]) return false
    }

    return true
  } catch (error) {
    console.error('Ошибка сравнения последовательностей:', error)
    return false
  }
}

// Функция верификации энтропии
const verifyEntropy = async () => {
  if (!entropyValue.value) return

  isVerifying.value = true
  verificationResult.value = ''
  isEntropyVerified.value = false
  verifiedSequence.value = ''

  try {
    // Отправляем запрос на верификацию энтропии
    const response = await axios.post(`${api8001}/generate/generate-winners/verify`, {
      seed: entropyValue.value,
      count_of_winning_numbers: winNumbersCount.value,
      max_number: rangeTo.value,
    })

    console.log('🔍 Результат верификации энтропии:', response.data)

    // Получаем верифицированную последовательность
    const verifiedData = response.data
    let verifiedTickets = ''

    if (verifiedData.winning_tickets) {
      // Преобразуем строку "18,4,43,7,26,17" в форматированную строку "18 | 4 | 43 | 7 | 26 | 17"
      verifiedTickets = verifiedData.winning_tickets
        .split(',')
        .map((num) => num.trim())
        .join(' | ')
      verifiedSequence.value = verifiedTickets
    }

    // Сравниваем с текущей сгенерированной последовательностью
    const isMatch = compareSequences(generatedSequence.value, verifiedTickets)

    if (isMatch) {
      isEntropyVerified.value = true
      verificationResult.value = 'Энтропия успешно верифицирована - последовательности совпадают'
      generationStatus.value = 'Энтропия верифицирована'
    } else {
      isEntropyVerified.value = false
      verificationResult.value = 'Энтропия не прошла верификацию - последовательности не совпадают'
      generationStatus.value = 'Ошибка верификации энтропии'
    }
  } catch (error) {
    console.error('❌ Ошибка верификации энтропии:', error)
    isEntropyVerified.value = false
    verificationResult.value = 'Ошибка при верификации энтропии'
    generationStatus.value = 'Ошибка верификации'
  } finally {
    isVerifying.value = false
  }
}

// Генерация выигрышных чисел (для WEB)
const generateWinNumbers = (count, from, to) => {
  const numbers = []
  const rangeSize = to - from + 1
  const availableNumbers = Array.from({ length: rangeSize }, (_, i) => i + from)

  for (let i = 0; i < count; i++) {
    if (availableNumbers.length === 0) break

    const randomIndex = Math.floor(Math.random() * availableNumbers.length)
    const selectedNumber = availableNumbers.splice(randomIndex, 1)[0]
    numbers.push(selectedNumber)
  }

  // Сортируем числа по возрастанию
  numbers.sort((a, b) => a - b)

  return numbers.join(' | ')
}

// Генерация случайной последовательности (для TXT)
const generateRandomSequence = (length) => {
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
  let result = ''
  for (let i = 0; i < length; i++) {
    result += chars.charAt(Math.floor(Math.random() * chars.length))
  }
  return result
}

const generateSequence = async () => {
  if (!isValidParams.value) return

  isGenerating.value = true

  if (generationMode.value === 'web') {
    await generateWeb()
  } else {
    await generateTxt()
  }
}

const generateWeb = async () => {
  generationStatus.value = 'Генерация выигрышных чисел...'

  try {
    // Подготавливаем данные для запроса
    const requestData = {
      count_of_winning_numbers: winNumbersCount.value,
      max_number: rangeTo.value,
    }

    // Добавляем энтропию, если она верифицирована
    if (isEntropyVerified.value && entropyValue.value) {
      requestData.entropy = entropyValue.value
    }

    // Отправляем запрос на сервер с параметрами
    const response = await axios.post(`${api8001}/generate/generate-winners`, requestData)

    console.log('🎯 Ответ сервера для выигрышных чисел:', response.data)

    // Получаем данные из ответа сервера
    const responseData = response.data

    // Сохраняем данные энтропии и начального заполнения
    if (responseData.seed) {
      entropyData.value = responseData.seed
      console.log(entropyData.value, 'ENTROPY')
    }
    if (responseData.initial_fill) {
      initialFillData.value = responseData.initial_fill
      console.log(initialFillData.value, 'INITIAL')
    }

    // Извлекаем сгенерированные числа из ответа
    let winNumbers = ''

    if (typeof responseData === 'object' && responseData !== null) {
      // Если сервер возвращает объект с winning_tickets
      if (responseData.winning_tickets) {
        // Преобразуем строку "3,11,38" в форматированную строку "3 | 11 | 38"
        winNumbers = responseData.winning_tickets
          .split(',')
          .map((num) => num.trim())
          .join(' | ')
      }
      // Если сервер возвращает массив numbers
      else if (responseData.numbers && Array.isArray(responseData.numbers)) {
        winNumbers = responseData.numbers.join(' | ')
      }
      // Если сервер возвращает последовательность
      else if (responseData.sequence) {
        winNumbers = responseData.sequence
      } else {
        // Если структура ответа неизвестна, генерируем локально
        console.warn('⚠️ Неизвестная структура ответа сервера, генерируем локально')
        winNumbers = generateWinNumbers(winNumbersCount.value, rangeFrom.value, rangeTo.value)
      }
    } else if (typeof responseData === 'string') {
      // Если сервер возвращает строку
      winNumbers = responseData
    } else {
      // Fallback на локальную генерацию
      console.warn('⚠️ Неподдерживаемый формат ответа, генерируем локально')
      winNumbers = generateWinNumbers(winNumbersCount.value, rangeFrom.value, rangeTo.value)
    }

    generatedSequence.value = winNumbers
    downloadedFile.value = null
    generationStatus.value = 'Выигрышные числа сгенерированы'

    // Если сервер возвращает ID последовательности, можно отправить на тестирование
    if (responseData.id || responseData.sequence_id) {
      const sequenceId = responseData.id || responseData.sequence_id
      console.log('🆔 ID последовательности для тестов:', sequenceId)

      // Создаем бинарную последовательность для тестов из выигрышных чисел
      let binarySequence = ''
      if (responseData.winning_tickets) {
        // Преобразуем выигрышные числа в бинарную последовательность
        const numbers = responseData.winning_tickets.split(',').map((num) => parseInt(num.trim()))
        binarySequence = numbers.map((num) => num.toString(2)).join('')
      } else {
        // Fallback - используем числа как есть
        binarySequence = winNumbers.replace(/\s*\|\s*/g, '')
      }

      // Показываем индикатор запуска тестов
      isTestsStarting.value = true
      generationStatus.value =
        'Запуск статистических тестов..., проверка осуществляется со скоростью 25 000 символов в секунду, ожидайте тестирование занимает не более минуты'

      // Отправляем на тестирование, если нужно
      try {
        const testResponse = await axios.post(`${api8000}/statistics/sequence`, {
          sequence_id: responseData.id || responseData.sequence_id,
          sequence: binarySequence,
        })

        console.log('📊 Результаты тестов для выигрышных чисел:', testResponse.data.tests_results)

        // Передаем результаты тестов в родительский компонент
        if (setTestResults && testResponse.data.tests_results) {
          setTestResults(testResponse.data.tests_results)
        }

        // Скрываем индикатор после получения результатов
        setTimeout(() => {
          isTestsStarting.value = false
        }, 1000)

        // Запускаем тесты с полученными результатами
        await runTests(testResponse.data.tests_results)
      } catch (testError) {
        console.warn('⚠️ Не удалось получить результаты тестов:', testError)
        // Скрываем индикатор при ошибке
        isTestsStarting.value = false
        // Продолжаем без тестов
        generationStatus.value = 'Числа сгенерированы (тесты недоступны)'
      }
    } else {
      // Если нет ID, просто показываем числа без тестов
      console.log('ℹ️ ID последовательности не получен, тесты не запускаются')
      generationStatus.value = 'Выигрышные числа сгенерированы'
    }
  } catch (error) {
    console.error('❌ Ошибка генерации выигрышных чисел:', error)
    // Скрываем индикатор при ошибке
    isTestsStarting.value = false

    // Fallback на локальную генерацию при ошибке
    try {
      console.log('🔄 Используем локальную генерацию...')
      const winNumbers = generateWinNumbers(winNumbersCount.value, rangeFrom.value, rangeTo.value)
      generatedSequence.value = winNumbers
      downloadedFile.value = null
      generationStatus.value = 'Числа сгенерированы локально (сервер недоступен)'
    } catch (fallbackError) {
      console.error('❌ Ошибка локальной генерации:', fallbackError)
      generationStatus.value = 'Ошибка генерации'
    }
  } finally {
    isGenerating.value = false
  }
}

const generateTxt = async () => {
  generationStatus.value =
    'Генерация и скачивание файла..., скорость генерации не менее 50 000 символов в секунду, ожидайте'

  try {
    // Имитация запроса к бэкенду для TXT генерации
    await new Promise((resolve) => setTimeout(resolve, 1000))

    // Генерация случайной последовательности
    const length = parseInt(sequenceLength.value)
    console.log(sequenceLength.value, 'ДЛИНА')
    const response = await axios.post(`${api8001}/generate/generate-file`, {
      length: sequenceLength.value,
    })
    console.log(response.data, 'RESPONSE')

    // Получаем данные из ответа сервера
    const responseData = response.data

    // Ищем поля Sequence и ID в ответе
    let sequence = ''
    let sequenceId = ''

    // Если responseData - это объект, ищем поля Sequence и ID
    if (typeof responseData === 'object' && responseData !== null) {
      sequence = responseData.Sequence || ''
      sequenceId = responseData.ID || responseData.id || responseData.uuid || ''
      console.log('📊 ID из объекта:', sequenceId)
      console.log('📊 Sequence из объекта:', sequence)
    }
    // Если responseData - это строка (текст файла), ищем в тексте
    else if (typeof responseData === 'string') {
      console.log('📄 Ответ в виде текста, ищем Sequence и ID...')

      // Пытаемся найти строку с ID в тексте
      const idMatch = responseData.match(/ID:\s*([a-fA-F0-9-]+)/)
      if (idMatch) {
        sequenceId = idMatch[1]
        console.log('✅ ID найден в тексте:', sequenceId)
      }

      // Пытаемся найти строку с Sequence в тексте
      const sequenceMatch = responseData.match(/Sequence:\s*([01]+)/)
      if (sequenceMatch) {
        sequence = sequenceMatch[1]
        console.log('✅ Sequence найден в тексте:', sequence)
      } else {
        // Если не нашли по шаблону, возможно весь текст и есть последовательность
        sequence = responseData.trim()
        console.log('ℹ️ Sequence не найден, используем весь текст:', sequence)
      }
    }

    // Если sequence пустой, используем fallback
    if (!sequence) {
      console.warn('⚠️ Sequence не найден, генерируем локально')
      sequence = generateRandomSequence(length)
    }

    console.log('🎯 Финальная последовательность для тестов:', sequence)
    console.log('🆔 ID последовательности:', sequenceId)

    // Создание и скачивание файла
    const blob = new Blob([sequence], { type: 'text/plain' })
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `sequence_${sequenceLength.value}.txt`
    document.body.appendChild(a)
    a.click()
    window.URL.revokeObjectURL(url)
    document.body.removeChild(a)

    downloadedFile.value = {
      name: `sequence_${sequenceLength.value}.txt`,
      size: blob.size,
    }
    generatedSequence.value = ''
    generationStatus.value = 'Файл успешно скачан'

    // Показываем индикатор запуска тестов
    isTestsStarting.value = true
    generationStatus.value = 'Запуск статистических тестов...'

    // Отправляем ID и sequence на сервер для получения результатов тестов
    const responseID = await axios.post(`${api8000}/statistics/sequence`, {
      sequence_id: sequenceId,
      sequence: sequence,
    })

    console.log('📊 Результаты тестов с сервера:', responseID.data.tests_results)

    // ПЕРЕДАЕМ РЕЗУЛЬТАТЫ ТЕСТОВ В РОДИТЕЛЬСКИЙ КОМПОНЕНТ ЧЕРЕЗ INJECT
    if (setTestResults && responseID.data.tests_results) {
      setTestResults(responseID.data.tests_results)
    }

    // Скрываем индикатор после получения результатов
    setTimeout(() => {
      isTestsStarting.value = false
    }, 1000)

    // Запускаем тесты с полученными результатами
    await runTests(responseID.data.tests_results)
  } catch (error) {
    console.error('Ошибка генерации:', error)
    // Скрываем индикатор при ошибке
    isTestsStarting.value = false
    generationStatus.value = 'Ошибка генерации файла'
  } finally {
    isGenerating.value = false
  }
}

// Функция запуска тестов
const runTests = async (testsResults) => {
  // Запускаем тесты через инъекцию из главного компонента
  startTests()

  console.log('📊 Получены данные тестов с сервера:', testsResults)

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
      await new Promise((resolve) => setTimeout(resolve, delay / 10))
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
}

const copyToClipboard = async () => {
  try {
    await navigator.clipboard.writeText(generatedSequence.value)
    copySuccess.value = true
    setTimeout(() => {
      copySuccess.value = false
    }, 2000)
  } catch (error) {
    console.error('Ошибка копирования:', error)
  }
}

const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}
</script>

<style scoped>
/* Стили остаются без изменений */
.generator-container {
  width: 100%;
  margin: 0 auto;
  max-width: 100%;
  overflow: hidden;
}

.generator-header {
  text-align: center;
  margin-bottom: var(--spacing-2xl);
  border-bottom: 2px solid var(--color-border);
  padding-bottom: var(--spacing-lg);
  font-size: 3rem;
}

.main-title {
  font-size: clamp(1.4rem, 4vw, 1.8rem);
  margin-bottom: var(--spacing-sm);
  word-break: break-word;
}

.generator-main {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xl);
  width: 100%;
}

.control-panel {
  background: var(--color-bg-elevated);
  border-radius: var(--border-radius-lg);
  padding: var(--spacing-lg);
  border: 1px solid var(--color-border);
  box-shadow: var(--shadow-sm);
  width: 100%;
  box-sizing: border-box;
}

/* Переключатель режимов */
.mode-switcher {
  margin-bottom: var(--spacing-lg);
}

.mode-buttons {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-sm);
  border: 2px solid var(--color-border);
  border-radius: var(--border-radius-md);
  padding: var(--spacing-sm);
  background: var(--color-bg-subtle);
  width: 100%;
  font-size: 1rem;
}

.mode-button {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-xs);
  padding: var(--spacing-sm);
  border: none;
  border-radius: var(--border-radius-sm);
  background: transparent;
  color: var(--color-text);
  transition: all var(--transition-normal);
  cursor: pointer;
  box-sizing: border-box;
  min-height: 60px;
  width: 100%;
}

.mode-button.active {
  background: var(--color-primary);
  color: var(--color-text-inverted);
  transform: translateY(-1px);
  box-shadow: var(--shadow-sm);
}

.mode-button:hover:not(.active) {
  background: var(--color-bg-elevated);
}

.mode-icon {
  font-size: 1.2rem;
  flex-shrink: 0;
}

.mode-text {
  font-size: clamp(0.7rem, 2vw, 0.8rem);
  font-weight: var(--font-weight-medium);
  text-align: center;
  line-height: 1.2;
  word-break: break-word;
  overflow-wrap: break-word;
}

/* Параметры для WEB режима */
.web-params {
  margin-bottom: var(--spacing-lg);
}

.params-grid {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
  font-size: 2.5rem;
  width: 100%;
}

.param-group {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
  width: 100%;
}

.param-label {
  font-size: 1.5rem;
  color: var(--color-text);
  font-weight: var(--font-weight-bold);
  text-transform: uppercase;
  word-break: break-word;
}

.param-input {
  padding: var(--spacing-sm);
  border: 2px solid var(--color-border);
  border-radius: var(--border-radius-md);
  background: var(--color-bg-subtle);
  color: var(--color-text);
  font-family: var(--font-mono);
  transition: all var(--transition-normal);
  box-sizing: border-box;
  width: 100%;
  font-size: clamp(0.8rem, 2vw, 0.9rem);
}

.param-input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px var(--color-primary-soft);
}

/* Параметры для TXT режима */
.txt-params {
  margin-bottom: var(--spacing-lg);
}

.input-section {
  margin-bottom: 0;
  width: 100%;
}

.input-label {
  display: block;
  margin-bottom: var(--spacing-sm);
  color: var(--color-text);
  font-weight: var(--font-weight-bold);
  font-size: 1.5rem;
  text-transform: uppercase;
  word-break: break-word;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  width: 100%;
}

.length-input {
  flex: 1;
  padding: var(--spacing-md);
  border: 2px solid var(--color-border);
  border-radius: var(--border-radius-md);
  background: var(--color-bg-subtle);
  color: var(--color-text);
  font-size: clamp(0.9rem, 2vw, 1rem);
  font-family: var(--font-mono);
  transition: all var(--transition-normal);
  box-sizing: border-box;
  width: 100%;
}

.length-input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px var(--color-primary-soft);
}

.length-input::placeholder {
  color: var(--color-text-muted);
}

.input-suffix {
  position: absolute;
  right: var(--spacing-md);
  color: var(--color-text-muted);
  font-size: clamp(0.8rem, 2vw, 0.9rem);
  pointer-events: none;
  white-space: nowrap;
}

.input-hint {
  margin-top: var(--spacing-xs);
  color: var(--color-text-light);
  font-size: clamp(0.7rem, 2vw, 0.8rem);
  word-break: break-word;
}

/* Кнопка генерации */
.generation-buttons {
  margin-bottom: var(--spacing-lg);
  display: flex;
  justify-content: center;
  width: 100%;
}

.generate-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-md);
  border: 2px solid var(--color-primary);
  border-radius: var(--border-radius-lg);
  background: var(--color-primary);
  color: var(--color-text-inverted);
  font-weight: var(--font-weight-bold);
  font-size: clamp(0.8rem, 2vw, 0.9rem);
  transition: all var(--transition-normal);
  width: 100%;
  max-width: 300px;
  box-sizing: border-box;
  flex-wrap: wrap;
}

.generate-button:hover:not(.disabled) {
  background: var(--color-primary-dark);
  border-color: var(--color-primary-dark);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(var(--color-primary-rgb), 0.3);
}

.generate-button.disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none !important;
}

.button-icon {
  font-size: 1.2rem;
  flex-shrink: 0;
}

.button-text {
  text-align: center;
  line-height: 1.2;
  word-break: break-word;
  overflow-wrap: break-word;
}

/* Статус генерации */
.generation-status {
  display: flex;
  justify-content: center;
  width: 100%;
}

.status-indicator {
  display: inline-flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-sm);
  border-radius: var(--border-radius-full);
  background: var(--color-bg-subtle);
  border: 2px solid var(--color-border);
  transition: all var(--transition-normal);
  box-sizing: border-box;
  max-width: 100%;
}

.status-indicator.running {
  border-color: var(--color-warning);
  background: var(--color-warning-soft);
}

.status-indicator.success {
  border-color: var(--color-success);
  background: var(--color-success-soft);
}

.status-icon {
  font-size: 1rem;
  flex-shrink: 0;
}

.status-text {
  color: var(--color-text);
  font-weight: var(--font-weight-medium);
  font-size: clamp(0.8rem, 2vw, 0.9rem);
  word-break: break-word;
}

/* Индикатор запуска тестов */
.tests-start-indicator {
  margin-top: var(--spacing-lg);
  padding: var(--spacing-lg);
  background: linear-gradient(135deg, #fff9db 0%, #fff3bf 100%);
  border: 2px solid #ffd43b;
  border-radius: var(--border-radius-lg);
  box-shadow: 0 4px 15px rgba(255, 212, 59, 0.3);
  animation: pulse-glow 2s ease-in-out infinite;
}

.indicator-content {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  text-align: left;
}

.indicator-icon {
  font-size: 2.5rem;
  flex-shrink: 0;
  animation: bounce 1s ease-in-out infinite;
}

.indicator-text {
  flex: 1;
}

.indicator-title {
  color: #e67700;
  font-size: 1.2rem;
  font-weight: var(--font-weight-bold);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin: 0 0 var(--spacing-xs) 0;
}

.indicator-description {
  color: #b35c00;
  font-size: 0.9rem;
  margin: 0;
  opacity: 0.9;
}

.indicator-animation {
  display: flex;
  gap: 6px;
  align-items: center;
}

.pulse-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #e67700;
  animation: pulse-dots 1.4s ease-in-out infinite both;
}

.pulse-dot:nth-child(2) {
  animation-delay: 0.2s;
}

.pulse-dot:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes pulse-glow {
  0%,
  100% {
    box-shadow: 0 4px 15px rgba(255, 212, 59, 0.3);
  }
  50% {
    box-shadow: 0 4px 25px rgba(255, 212, 59, 0.6);
  }
}

@keyframes bounce {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-5px);
  }
}

@keyframes pulse-dots {
  0%,
  80%,
  100% {
    transform: scale(0.8);
    opacity: 0.5;
  }
  40% {
    transform: scale(1.2);
    opacity: 1;
  }
}

/* Результаты генерации */
.generation-results {
  background: var(--color-bg-elevated);
  border-radius: var(--border-radius-lg);
  padding: var(--spacing-lg);
  border: 1px solid var(--color-border);
  box-shadow: var(--shadow-sm);
  box-sizing: border-box;
  width: 100%;
}

.result-header {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
  border-bottom: 1px solid var(--color-border);
  padding-bottom: var(--spacing-md);
  width: 100%;
}

.copy-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-sm);
  background: var(--color-bg-subtle);
  border: 1px solid var(--color-border);
  color: var(--color-text);
  font-size: clamp(0.7rem, 2vw, 0.8rem);
  border-radius: var(--border-radius-md);
  min-width: auto;
  width: 100%;
  max-width: 140px;
  box-sizing: border-box;
  white-space: nowrap;
}

.copy-button:hover {
  background: var(--color-primary);
  border-color: var(--color-primary);
  color: var(--color-text-inverted);
}

.copy-button.success {
  background: var(--color-success);
  border-color: var(--color-success);
  color: var(--color-text-inverted);
}

/* Дополнительная информация */
.additional-info {
  margin-bottom: var(--spacing-lg);
  padding: var(--spacing-md);
  background: var(--color-bg-subtle);
  border: 1px solid var(--color-border);
  border-radius: var(--border-radius-md);
}

.info-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--spacing-md);
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
  padding: var(--spacing-sm);
  background: var(--color-bg-elevated);
  border-radius: var(--border-radius-sm);
  border: 1px solid var(--color-border);
}

.info-label {
  font-size: 1.5rem;
  color: var(--color-text-muted);
  font-family: var(--font-mono);
  text-transform: uppercase;
  word-break: break-word;
}
.label {
  font-size: 3rem;
}
.info-value {
  font-size: clamp(0.8rem, 2vw, 0.9rem);
  color: var(--color-primary);
  font-weight: var(--font-weight-bold);
  font-family: var(--font-mono);
  word-break: break-all;
  padding: var(--spacing-xs);
  background: var(--color-bg-subtle);
  border-radius: var(--border-radius-sm);
  border: 1px solid var(--color-border);
  line-height: 1.4;
}

.decimal-value {
  color: var(--color-success);
  font-weight: var(--font-weight-normal);
  font-size: 0.9em;
  margin-left: var(--spacing-xs);
}

.info-value.verified {
  color: var(--color-success);
  border-color: var(--color-success);
}

.info-value.not-verified {
  color: var(--color-danger);
  border-color: var(--color-danger);
}

.entropy-value,
.initial-fill-value {
  word-break: break-all;
  overflow-wrap: break-word;
}

.info-hint {
  color: var(--color-text-light);
  font-size: clamp(0.6rem, 2vw, 0.7rem);
  font-style: italic;
}

.sequence-preview {
  background: var(--color-bg-subtle);
  border: 1px solid var(--color-border);
  border-radius: var(--border-radius-md);
  padding: var(--spacing-md);
  margin-bottom: var(--spacing-md);
  max-height: 150px;
  overflow-y: auto;
  box-sizing: border-box;
  width: 100%;
}

.sequence-text {
  margin: 0;
  color: var(--color-text);
  font-size:2rem;
  line-height: 1.4;
  word-break: break-all;
  white-space: pre-wrap;
  text-align: center;
  font-weight: var(--font-weight-bold);
  overflow-wrap: break-word;
}

/* Секция верификации */
.verification-section {
  margin-top: var(--spacing-lg);
  padding: var(--spacing-md);
  background: var(--color-bg-subtle);
  border: 1px solid var(--color-border);
  border-radius: var(--border-radius-md);
}

.verification-header {
  margin-bottom: var(--spacing-md);
  border-bottom: 1px solid var(--color-border);
  padding-bottom: var(--spacing-sm);
}

.verification-content {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.verification-input-group {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.verification-label {
  font-size: 1.5rem;
  color: var(--color-text);
  font-weight: var(--font-weight-bold);
  text-transform: uppercase;
  word-break: break-word;
}

/* Стили для поля ввода энтропии и кнопки верификации */
.entropy-input-wrapper {
  display: flex;
  gap: var(--spacing-sm);
  width: 100%;
}

.entropy-input {
  flex: 1;
}

.entropy-input.verified {
  border-color: var(--color-success);
  background: var(--color-success-soft);
}

.verify-button {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  padding: var(--spacing-sm);
  border: 2px solid var(--color-border);
  border-radius: var(--border-radius-md);
  background: var(--color-bg-subtle);
  color: var(--color-text);
  font-size: clamp(0.7rem, 2vw, 0.8rem);
  cursor: pointer;
  transition: all var(--transition-normal);
  white-space: nowrap;
  min-width: 140px;
  justify-content: center;
}

.verify-button:hover:not(.disabled) {
  background: var(--color-primary);
  border-color: var(--color-primary);
  color: var(--color-text-inverted);
}

.verify-button.verified {
  background: var(--color-success);
  border-color: var(--color-success);
  color: var(--color-text-inverted);
}

.verify-button.disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.verify-icon {
  font-size: 0.9rem;
}

.verify-text {
  font-weight: var(--font-weight-medium);
}

.verification-hint {
  color: var(--color-text-light);
  font-size: clamp(0.7rem, 2vw, 0.8rem);
  word-break: break-word;
}

.verification-status {
  margin-top: var(--spacing-sm);
}

.status-item {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
  padding: var(--spacing-sm);
  background: var(--color-bg-elevated);
  border-radius: var(--border-radius-sm);
  border: 1px solid var(--color-border);
}

.status-label {
  font-size: clamp(0.65rem, 2vw, 0.7rem);
  color: var(--color-text-muted);
  font-family: var(--font-mono);
  text-transform: uppercase;
  word-break: break-word;
}

.status-value {
  font-size: clamp(0.8rem, 2vw, 0.9rem);
  font-weight: var(--font-weight-bold);
  font-family: var(--font-mono);
  padding: var(--spacing-xs);
  border-radius: var(--border-radius-sm);
  border: 1px solid var(--color-border);
}

.status-value.verified {
  color: var(--color-success);
  border-color: var(--color-success);
  background: var(--color-success-soft);
}

.status-value.not-verified {
  color: var(--color-danger);
  border-color: var(--color-danger);
  background: var(--color-danger-soft);
}

.status-details {
  color: var(--color-text-light);
  font-size: clamp(0.6rem, 2vw, 0.7rem);
  font-style: italic;
}

/* Стили для верифицированной последовательности */
.verified-sequence {
  margin-top: var(--spacing-md);
}

.verified-sequence-value {
  color: var(--color-success);
  border-color: var(--color-success);
  background: var(--color-success-soft);
}

.sequence-info {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
  margin-top: var(--spacing-md);
  padding: var(--spacing-sm);
  background: var(--color-bg-subtle);
  border-radius: var(--border-radius-md);
  border: 1px solid var(--color-border);
  box-sizing: border-box;
  width: 100%;
}

.file-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-sm);
  text-align: center;
  width: 100%;
}

.file-icon {
  font-size: 2rem;
}

.file-details {
  text-align: center;
  width: 100%;
}

.file-name {
  color: var(--color-text);
  margin: 0 0 var(--spacing-xs) 0;
  font-size: clamp(0.9rem, 2vw, 1rem);
  word-break: break-word;
}

.file-size {
  color: var(--color-text-muted);
  margin: 0;
  font-size: clamp(0.7rem, 2vw, 0.8rem);
}

.download-actions {
  display: flex;
  justify-content: center;
  margin-top: var(--spacing-md);
  width: 100%;
}

/* Основные кнопки в результатах */
.primary {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-sm);
  background: var(--color-primary);
  border: 2px solid var(--color-primary);
  color: var(--color-text-inverted);
  font-size: clamp(0.7rem, 2vw, 0.8rem);
  padding: var(--spacing-sm);
  border-radius: var(--border-radius-md);
  width: 100%;
  max-width: 200px;
  box-sizing: border-box;
}

.primary:hover {
  background: var(--color-primary-dark);
  border-color: var(--color-primary-dark);
}

/* Адаптивность */
@media (max-width: 768px) {
  .mode-buttons {
    grid-template-columns: 1fr;
    gap: var(--spacing-xs);
  }

  .params-grid {
    gap: var(--spacing-sm);
  }

  .entropy-input-wrapper {
    flex-direction: column;
  }

  .verify-button {
    min-width: 100%;
  }

  .result-header {
    flex-direction: column;
    gap: var(--spacing-sm);
    align-items: center;
    text-align: center;
  }

  .info-grid {
    grid-template-columns: 1fr;
  }

  .sequence-info {
    flex-direction: column;
    gap: var(--spacing-sm);
  }

  .file-info {
    flex-direction: column;
    text-align: center;
    gap: var(--spacing-sm);
  }

  .file-details {
    text-align: center;
  }

  .generate-button {
    max-width: 100%;
    padding: var(--spacing-sm);
    font-size: 0.8rem;
  }

  .mode-button {
    padding: var(--spacing-xs);
    min-height: 50px;
  }

  .control-panel {
    padding: var(--spacing-md);
  }

  .verification-section {
    padding: var(--spacing-sm);
  }

  .tests-start-indicator {
    padding: var(--spacing-md);
  }

  .indicator-content {
    flex-direction: column;
    text-align: center;
    gap: var(--spacing-sm);
  }

  .indicator-icon {
    font-size: 2rem;
  }

  .indicator-title {
    font-size: 1rem;
  }

  .indicator-description {
    font-size: 0.8rem;
  }
}

@media (max-width: 480px) {
  .control-panel {
    padding: var(--spacing-sm);
  }

  .generate-button {
    padding: var(--spacing-sm);
    font-size: 0.75rem;
    gap: var(--spacing-xs);
  }

  .button-icon {
    font-size: 1rem;
  }

  .mode-button {
    padding: var(--spacing-xs);
    min-height: 45px;
  }

  .mode-icon {
    font-size: 1rem;
  }

  .mode-text {
    font-size: 0.7rem;
  }

  .params-grid {
    gap: var(--spacing-sm);
  }

  .param-input,
  .length-input {
    padding: var(--spacing-sm);
    font-size: 0.8rem;
  }

  .generation-results {
    padding: var(--spacing-md);
  }

  .additional-info {
    padding: var(--spacing-sm);
  }

  .info-item {
    padding: var(--spacing-xs);
  }

  .decimal-value {
    display: block;
    margin-left: 0;
    margin-top: var(--spacing-xs);
  }
}

/* Дополнительные исправления для очень маленьких экранов */
@media (max-width: 360px) {
  .mode-text {
    font-size: 0.65rem;
  }

  .generate-button .button-text {
    font-size: 0.7rem;
  }

  .param-label,
  .input-label {
    font-size: 0.7rem;
  }

  .verify-text {
    font-size: 0.65rem;
  }
}
</style>