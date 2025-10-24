<!-- MyLinerRegister.vue -->
<template>
  <div class="lfsr-container">
    <!-- Заголовок -->
    <div class="lfsr-header">
      <h2 class="cyber-heading">
        <span class="text-indigo-theme">16-БИТНЫЙ LFSR</span>
      </h2>
      <p class="lfsr-subtitle futurism-elegant">Линейный Регистр Сдвига с Обратной Связью</p>
    </div>

    <!-- Блок преобразования числа -->
    <div v-if="showConversion" class="conversion-section">
      <div class="conversion-container">
        <h3 class="conversion-title cyber-heading">ПРЕОБРАЗОВАНИЕ ЧИСЛА</h3>
        
        <div class="conversion-steps">
          <!-- Шаг 1: Исходное число -->
          <div class="conversion-step">
            <div class="step-label cyber-mono">ИСХОДНОЕ ЧИСЛО:</div>
    <div class="step-value cyber-mono" :class="{ 'blink-original': blinkOriginalNumber }">
      {{ originalNumber }}
    </div>
  </div>

          <!-- Шаг 2: Умножение на 10 -->
          <div class="conversion-step">
            <div class="step-label cyber-mono">× 10^18:</div>
            <div class="step-value cyber-mono">{{ multipliedNumber }}</div>
            <div class="step-animation" v-if="currentStep >= 1">
              <div class="animation-dot"></div>
              <div class="animation-dot"></div>
              <div class="animation-dot"></div>
            </div>
          </div>
        </div>

<!-- Измененная таблица преобразования -->
<div class="binary-table-section">
  <h4 class="table-title cyber-heading">ПРЕОБРАЗОВАНИЕ DECIMAL → BINARY</h4>
  
  <!-- Облачко с пояснением для таблицы -->
  <div v-if="showTableBubble" class="table-explanation-bubble">
    <div class="bubble-content">
      <span class="bubble-icon">💡</span>
      <span class="bubble-text">Для работы регистра сдвига преобразуем десятичные цифры в двоичную последовательность</span>
    </div>
  </div>
  
  <div class="binary-table">
    <div class="table-header">
      <div class="decimal-column cyber-mono">ДЕСЯТИЧНЫЕ ЦИФРЫ</div>
      <div class="arrow-column"></div>
      <div class="binary-column cyber-mono">ДВОИЧНЫЙ КОД (8 бит)</div>
    </div>
    <div class="table-body">
      <!-- Строки для каждой цифры -->
      <div 
        v-for="(digit, index) in decimalDigits" 
        :key="index"
        class="table-row" 
        :class="{ 'active': currentTableRow >= index }"
      >
        <div class="decimal-column cyber-mono">
          <span class="decimal-digit" :class="{ 'visible': currentTableRow >= index }">
            {{ digit }}
          </span>
        </div>
        <div class="arrow-column">
          <div class="arrow-animation" :class="{ 'active': currentTableRow === index }">
            →
          </div>
        </div>
        <div class="binary-column cyber-mono">
          <span class="binary-digit" :class="{ 
            'visible': binaryDigits[index] !== '',
            'animating': currentTableRow === index
          }">
            {{ binaryDigits[index] || '????????' }}
          </span>
        </div>
      </div>
      <!-- Третья строка - троеточие -->
      <div class="table-row dots-row">
        <div class="decimal-column cyber-mono">
          <span class="dots">...</span>
        </div>
        <div class="arrow-column">
          <div class="arrow-animation">→</div>
        </div>
        <div class="binary-column cyber-mono">
          <span class="dots">...</span>
        </div>
      </div>
    </div>
  </div>
</div>




        <!-- Кнопка запуска преобразования -->
          <div class="conversion-controls" v-if="!props.startSdvig">
            <button 
              class="cyber-button primary"
              @click="startConversion"
              :disabled="isConverting"
            >
              <span class="button-icon">{{ isConverting ? '⏳' : '🚀' }}</span>
              {{ isConverting ? 'ПРЕОБРАЗОВАНИЕ...' : 'НАЧАТЬ ПРЕОБРАЗОВАНИЕ' }}
            </button>
          </div>
      </div>
    </div>

    <!-- Основной контейнер -->
    <div class="lfsr-main">
      <!-- Визуализация регистра -->
      <div class="register-visualization">
        <!-- Облачко объяснения LFSR -->
        <!-- Облачко объяснения LFSR - ПЕРВОЕ ПОВЫШЕ, остальные нормально -->
        <div v-if="showLfsrBubble" class="lfsr-explanation-bubble" :class="bubbleType">
          <div class="bubble-content">
            <span class="bubble-icon">{{ bubbleIcon }}</span>
            <div class="bubble-text-content">
              <div class="bubble-title cyber-mono">{{ bubbleTitle }}</div>
              <div class="bubble-description futurism-elegant">{{ bubbleDescription }}</div>
              <div v-if="showXorCalculation" class="xor-calculation">
                <div class="xor-formula cyber-mono">
                  {{ xorFormula }}
                </div>
                <div class="xor-result cyber-mono">
                  = {{ xorResult }}
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="register-container">
          <div
            v-for="(bit, index) in bitsReversed"
            :key="index"
            class="register-bit"
            :class="{
              'bit-1': bit === 1,
              'bit-0': bit === 0,
              'active-tap': activeTaps.includes(15 - index),
              'new-bit': index === 0 && justUpdated,
              'xor-highlight': xorHighlightBits.includes(15 - index),
              'empty-bit': isShiftAnimation && index === 0,
              'blink-green-step3': currentAnimationStep === 3 && index === 0  // Добавляем класс для моргания при step 3
            }"
            :title="`Бит ${15 - index}${activeTaps.includes(15 - index) ? ' — тап' : ''}`"
          >
            <div class="bit-value cyber-mono">
              {{ isShiftAnimation && index === 0 ? '?' : bit }}
            </div>
            <div class="bit-index cyber-mono">{{ 15 - index }}</div>
            <div 
              v-if="activeTaps.includes(15 - index)"
              class="tap-connector"
              :class="{ 'xor-highlight': xorHighlightBits.includes(15 - index) }"
            ></div>
            
            <!-- Красные стрелки для XOR битов -->
            <div 
              v-if="xorHighlightBits.includes(15 - index)"
              class="xor-arrow"
              :style="{ 
                left: index < 8 ? '100%' : '-20px',
                transform: index < 8 ? 'none' : 'rotate(180deg)'
              }"
            >
              <div class="arrow-head"></div>
            </div>
          </div>
        </div>

        <!-- Информация о состоянии -->
        <div class="state-info">
          <div class="state-item">
            <span class="state-label cyber-mono">СОСТОЯНИЕ:</span>
            <span class="state-value cyber-mono">{{ stateToBinary }}</span>
          </div>
          <div class="state-item">
            <span class="state-label cyber-mono">HEX:</span>
            <span class="state-value cyber-mono">{{ stateToHex }}</span>
          </div>
          <div class="state-item" v-if="conversionComplete">
            <span class="state-label cyber-mono">ИСХОДНОЕ:</span>
            <span class="state-value cyber-mono">0x{{ finalHexValue }}</span>
          </div>
        </div>
      </div>

      <!-- Статус -->
      <div class="status-section">
        <div class="status-indicator" :class="{ active: isRunning }">
          <span class="status-icon">{{ isRunning ? '⚡' : '⏸' }}</span>
          <span class="status-text cyber-mono">
            {{ isRunning ? 'АВТОМАТИЧЕСКИЙ РЕЖИМ' : conversionComplete ? 'РЕЖИМ ОЖИДАНИЯ' : 'ТРЕБУЕТСЯ ПРЕОБРАЗОВАНИЕ' }}
          </span>
        </div>
        <p class="status-note futurism-elegant" v-if="isRunning">
          Обновление каждые 500 мс
        </p>
        <p class="status-note futurism-elegant" v-else-if="!conversionComplete">
          Нажмите "НАЧАТЬ ПРЕОБРАЗОВАНИЕ" для инициализации LFSR
        </p>
      </div>
    </div>

    <!-- Информационная панель -->
    <div class="info-panel">
      <div class="info-item">
        <h4 class="info-title cyber-heading">ПРИНЦИП РАБОТЫ LFSR</h4>
        <p class="info-text futurism-elegant">
          16-битный линейный регистр сдвига генерирует псевдослучайную последовательность через XOR
          выбранных битов (тапов). Максимальный период: 65535 тактов.
        </p>
      </div>
      <div class="info-item">
        <h4 class="info-title cyber-heading">ПРЕОБРАЗОВАНИЕ ЧИСЛА</h4>
        <p class="info-text futurism-elegant">
          Исходное число умножается на 10^18, преобразуется в шестнадцатеричный формат,
          из которого берутся первые 4 цифры для инициализации регистра.
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, defineProps, onMounted } from 'vue'

const props = defineProps({
  chislo: Number,
  startSdvig: Boolean,
})

// Предопределённые корректные тапы для 16-битного LFSR
const tapPresets = [
  { id: 'preset1', label: 'Минимум (2 тапа)', taps: [16, 14] },
  { id: 'preset2', label: 'Стандартный (3 тапа)', taps: [16, 15, 13, 4] },
  { id: 'preset3', label: 'Максимальная длина (4 тапа)', taps: [16, 14, 13, 11] },
]

const selectedPreset = ref('preset2')
const state = ref(0)
const isRunning = ref(false)
const justUpdated = ref(false)

// Переменные для преобразования числа
const showConversion = ref(true)
const isConverting = ref(false)
const currentStep = ref(0)
const conversionComplete = ref(false)
const originalNumber = ref('')
const multipliedNumber = ref('')
const hexString = ref('')
const finalHexValue = ref('')
const decimalDigits = ref(['?', '?', '?', '?'])

// Переменные для таблицы преобразования
const hexDigits = ref(['?', '?', '?', '?'])
const currentTableRow = ref(-1)
const binaryDigits = ref(['', '', '', ''])

// Переменные для облачков
const showTableBubble = ref(false)

// Новые переменные для анимации LFSR с облачками
const showLfsrBubble = ref(false)
const bubbleType = ref('info')
const bubbleIcon = ref('💡')
const bubbleTitle = ref('')
const bubbleDescription = ref('')
const showXorCalculation = ref(false)
const xorFormula = ref('')
const xorResult = ref('')
const xorHighlightBits = ref([])
const isShiftAnimation = ref(false)
const currentAnimationStep = ref(0)
// Добавляем новые переменные для анимации моргания
const blinkOriginalNumber = ref(false)
const blinkFirstBit = ref(false)


// Инициализация при получении props
onMounted(() => {
  if (props.chislo) {
    originalNumber.value = props.chislo.toFixed(17)
  }
})

// Watch для отслеживания изменения startSdvig
watch(() => props.startSdvig, (newValue) => {
  if (newValue && !conversionComplete.value && !isConverting.value) {
    console.log('startSdvig стал true, автоматически запускаем преобразование')
    isRunning.value = true
    startConversion() // Автоматически запускаем преобразование
  } else if (newValue && conversionComplete.value) {
    console.log('startSdvig стал true, запускаем LFSR')
    isRunning.value = true
    start()
  }
})

// Watch для отслеживания изменения числа
watch(() => props.chislo, (newValue) => {
  if (newValue) {
    originalNumber.value = newValue.toFixed(17)
    if (conversionComplete.value) {
      conversionComplete.value = false
      currentStep.value = 0
      state.value = 0
      currentTableRow.value = -1
      binaryDigits.value = ['', '', '', '']
      hexDigits.value = ['?', '?', '?', '?']
    }
  }
})

// Функция для преобразования десятичной цифры в двоичный код (8 бит)
const decimalToBinary = (decimalDigit) => {
  const decimal = parseInt(decimalDigit, 10)
  return decimal.toString(2).padStart(8, '0')
}



// Функция для точного умножения числа на 10^17
const multiplyByPowerOfTen = (numStr, power) => {
  const [integerPart, decimalPart = ''] = numStr.split('.')
  const fullNumber = integerPart + decimalPart
  const zerosToAdd = power - decimalPart.length
  let result = fullNumber
  
  if (zerosToAdd > 0) {
    result = result.padEnd(result.length + zerosToAdd, '0')
  }
  
  result = result.replace(/^0+/, '') || '0'
  return result
}


const animateBinaryConversion = async () => {
  // Анимируем каждую цифру по отдельности
  for (let i = 0; i < decimalDigits.value.length; i++) {
    currentTableRow.value = i
    await new Promise(resolve => setTimeout(resolve, 600))
    
    binaryDigits.value[i] = decimalToBinary(decimalDigits.value[i])
    await new Promise(resolve => setTimeout(resolve, 800))
  }
  
  currentTableRow.value = -1
  await new Promise(resolve => setTimeout(resolve, 500))
}



// Преобразование числа
// Преобразование числа
const startConversion = async () => {
  if (isConverting.value) return
  
  window.scrollTo({
    top: 900,
    behavior: 'smooth'
  })

  isConverting.value = true
  currentStep.value = 0
  conversionComplete.value = false
  currentTableRow.value = -1
  binaryDigits.value = ['', '', '', '']
  decimalDigits.value = ['?', '?', '?', '?']
  showTableBubble.value = false

  try {
    // Запускаем моргание исходного числа на 3 секунды
    blinkOriginalNumber.value = true
    await new Promise(resolve => setTimeout(resolve, 3000))
    blinkOriginalNumber.value = false
    
    await new Promise(resolve => setTimeout(resolve, 800))
    multipliedNumber.value = multiplyByPowerOfTen(originalNumber.value, 18)
    currentStep.value = 1
    
    await new Promise(resolve => setTimeout(resolve, 800))
    const bigIntValue = BigInt(multipliedNumber.value)
    hexString.value = bigIntValue.toString(16).toUpperCase()
    currentStep.value = 2
    
    await new Promise(resolve => setTimeout(resolve, 800))
    finalHexValue.value = hexString.value.substring(0, 4).padStart(4, '0')
    currentStep.value = 3
    
    // ИСПРАВЛЕНИЕ: Берем первые 4 цифры из десятичного числа multipliedNumber
    const decimalString = multipliedNumber.value.toString().substring(0, 4).padStart(4, '0')
    decimalDigits.value = decimalString.split('') // ['9', '8', '7', '4']
    
    // Показываем облачко для таблицы преобразования
    showTableBubble.value = true
    await new Promise(resolve => setTimeout(resolve, 1500))
    
    await animateBinaryConversion()
    
    showTableBubble.value = false
    
    state.value = parseInt(finalHexValue.value, 16)
    conversionComplete.value = true
    
    // АВТОМАТИЧЕСКИ ЗАПУСКАЕМ LFSR ПОСЛЕ ПРЕОБРАЗОВАНИЯ
    await new Promise(resolve => setTimeout(resolve, 1500))
    start()
    
  } catch (error) {
    console.error('Ошибка при преобразовании числа:', error)
  } finally {
    isConverting.value = false
  }
}

// Получаем активные тапы
const activeTaps = computed(() => {
  const preset = tapPresets.find((p) => p.id === selectedPreset.value)
  if (!preset) return []
  return preset.taps.map(t => t - 1).filter(bit => bit >= 0 && bit < 16)
})

// Биты регистра
const bits = computed(() => {
  return Array.from({ length: 16 }, (_, i) => (state.value >> (15 - i)) & 1)
})

const bitsReversed = computed(() => {
  return bits.value
})

// Вспомогательные представления
const stateToBinary = computed(() =>
  state.value.toString(2).padStart(16, '0')
)

const stateToHex = computed(() =>
  '0x' + state.value.toString(16).toUpperCase().padStart(4, '0')
)

// Вычисление нового бита (XOR выбранных тапов)
function computeFeedback() {
  let feedback = 0
  for (const tap of activeTaps.value) {
    feedback ^= (state.value >> tap) & 1
  }
  return feedback
}

// Один шаг LFSR
function lfsrStep() {
  const newBit = computeFeedback()
  state.value = ((state.value >> 1) | (newBit << 15)) & 0xFFFF
  justUpdated.value = true
  setTimeout(() => (justUpdated.value = false), 300)
}

// Функция для показа облачка объяснения LFSR - с разной высотой для первого шага
const showExplanationBubble = async (step) => {
  currentAnimationStep.value = step
  
  switch (step) {
    case 1:
      // Шаг 1: Вычисление обратной связи - ПЕРВОЕ ОБЛАЧКО ВЫШЕ
      showLfsrBubble.value = true
      bubbleType.value = 'calculation'
      bubbleIcon.value = '🧮'
      bubbleTitle.value = 'ШАГ 1: ВЫЧИСЛЕНИЕ ОБРАТНОЙ СВЯЗИ'
      bubbleDescription.value = 'Выполняем операцию XOR между битами на позициях тапов:'
      showXorCalculation.value = true
      
      // Подсвечиваем биты для XOR
      xorHighlightBits.value = [...activeTaps.value]
      
      // Формируем формулу XOR
      const tapValues = activeTaps.value.map(tap => {
        const bitValue = (state.value >> tap) & 1
        return `бит${15 - tap}(${bitValue})`
      })
      xorFormula.value = tapValues.join(' ⊕ ')
      xorResult.value = computeFeedback()
      
      break
      
    case 2:
      // Шаг 2: Сдвиг вправо - нормальная высота
      showLfsrBubble.value = true
      bubbleType.value = 'shift'
      bubbleIcon.value = '➡️'
      bubbleTitle.value = 'ШАГ 2: СДВИГ ВПРАВО'
      bubbleDescription.value = 'Все биты сдвигаются на одну позицию вправо. Младший бит теряется.'
      showXorCalculation.value = false
      xorHighlightBits.value = []
      
      // Включаем анимацию сдвига
      isShiftAnimation.value = true
      
      break
      
    case 3:
      // Шаг 3: Вставка нового бита - нормальная высота
      showLfsrBubble.value = true
      bubbleType.value = 'insert'
      bubbleIcon.value = '⭐'
      bubbleTitle.value = 'ШАГ 3: ВСТАВКА НОВОГО БИТА'
      bubbleDescription.value = `Новый бит обратной связи (${computeFeedback()}) вставляется в старший разряд`
      showXorCalculation.value = false
      isShiftAnimation.value = false
      
      break
      
    case 4:
      // Шаг 4: Завершение объяснения - нормальная высота
      showLfsrBubble.value = true
      bubbleType.value = 'info'
      bubbleIcon.value = '✅'
      bubbleTitle.value = 'АЛГОРИТМ РАБОТЫ LFSR'
      bubbleDescription.value = 'Так работает линейный регистр сдвига с обратной связью! Теперь процесс будет продолжаться автоматически.'
      showXorCalculation.value = false
      
      break
      
    default:
      showLfsrBubble.value = false
  }
}

// Обновленная функция start с анимацией
async function start() {
  if (conversionComplete.value) {

          window.scrollTo({
          top: 1500,
          behavior: 'smooth'})

    
    isRunning.value = true
    
    // Первые 4 шага с анимацией объяснения
    for (let step = 1; step <= 4; step++) {
      if (!isRunning.value) break
      
      await showExplanationBubble(step)
      await new Promise(resolve => setTimeout(resolve, 7000))
      
      // Выполняем соответствующие действия для каждого шага
      if (step === 1) {
        // На шаге 1 только показываем вычисление, не выполняем сдвиг
        continue
      } else if (step === 2) {
        // На шаге 2 выполняем сдвиг (но не вставляем новый бит еще)
        state.value = (state.value >> 1) & 0xFFFF
      } else if (step === 3) {

        // На шаге 3 вставляем новый бит
        const newBit = computeFeedback()
        state.value = (state.value | (newBit << 15)) & 0xFFFF
        justUpdated.value = true
        setTimeout(() => justUpdated.value = false, 300)
      }
      
      await new Promise(resolve => setTimeout(resolve, 1000))
    }
    
    // Скрываем облачко после завершения анимации
    showLfsrBubble.value = false
    isShiftAnimation.value = false
    xorHighlightBits.value = []
    
    // Переход к нормальной работе
    const interval = setInterval(() => {
      if (!isRunning.value) {
        clearInterval(interval)
        return
      }
      lfsrStep()
    }, 500)
    window.lfsrInterval = interval
  }
}

function stop() {
  isRunning.value = false
  if (window.lfsrInterval) {
    clearInterval(window.lfsrInterval)
    delete window.lfsrInterval
  }
  showLfsrBubble.value = false
  isShiftAnimation.value = false
  xorHighlightBits.value = []
}

function reset() {
  stop()
  state.value = 0
  conversionComplete.value = false
  currentStep.value = 0
  multipliedNumber.value = ''
  hexString.value = ''
  finalHexValue.value = ''
  currentTableRow.value = -1
  binaryDigits.value = ['', '', '', '']
  hexDigits.value = ['?', '?', '?', '?']
  showTableBubble.value = false
  showLfsrBubble.value = false
  isShiftAnimation.value = false
  xorHighlightBits.value = []
}

</script>

<style scoped>
.blink-original {
  animation: blink-original-pulse 0.5s ease-in-out infinite !important;
  border: 2px solid var(--color-primary) !important;
  background: var(--color-primary-soft) !important;
  color: var(--color-primary) !important;
  box-shadow: 0 0 12px var(--color-primary) !important;
  border-radius: var(--border-radius-md);
  padding: var(--spacing-sm) var(--spacing-md);
}

@keyframes blink-original-pulse {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
    box-shadow: 0 0 8px var(--color-primary);
  }
  50% {
    opacity: 0.7;
    transform: scale(1.02);
    box-shadow: 0 0 16px var(--color-primary);
  }
}

.blink-green-step3 .bit-value {
  animation: blink-green-step3-pulse 0.6s ease-in-out infinite !important;
  border-color: var(--color-success) !important;
  background: var(--color-success-soft) !important;
  color: var(--color-success) !important;
  box-shadow: 0 0 12px var(--color-success) !important;
}

@keyframes blink-green-step3-pulse {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
    box-shadow: 0 0 8px var(--color-success);
  }
  50% {
    opacity: 0.8;
    transform: scale(1.05);
    box-shadow: 0 0 16px var(--color-success);
  }
}
.decimal-column {
  flex: 1;
}

.arrow-column {
  width: 80px;
  flex: none;
}

.binary-column {
  flex: 2;
}

.decimal-digit, .binary-digit {
  transition: all var(--transition-normal);
  opacity: 0.3;
}

.decimal-digit.visible {
  opacity: 1;
  font-weight: var(--font-weight-bold);
  color: var(--color-primary);
  animation: digit-appear 0.5s ease-out;
}

.binary-digit {
  font-family: 'Courier New', monospace;
  letter-spacing: 1px;
  font-size: 0.9rem;
}

.binary-digit.visible {
  opacity: 1;
  font-weight: var(--font-weight-bold);
  color: var(--color-accent);
}

/* Стили для облачка таблицы преобразования - ПОНИЖЕ */
.table-explanation-bubble {
  position: absolute;
  left: 50%;
  top: -70px; /* Уменьшил высоту позиционирования */
  transform: translateX(-50%);
  background: var(--color-accent-soft);
  border: 2px solid var(--color-accent);
  border-radius: 20px;
  padding: var(--spacing-lg);
  max-width: 350px;
  z-index: 1000;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  animation: table-bubble-slide-down 0.6s ease-out;
}

.table-explanation-bubble::before {
  content: '';
  position: absolute;
  left: 50%;
  bottom: -20px;
  transform: translateX(-50%);
  width: 0;
  height: 0;
  border: 15px solid transparent;
  border-top-color: var(--color-accent);
  border-bottom: 0;
}

.binary-table-section {
  position: relative;
  margin-top: var(--spacing-xl);
  padding-top: var(--spacing-lg);
  border-top: 1px solid var(--color-border);
}

@keyframes table-bubble-slide-down {
  0% {
    opacity: 0;
    transform: translateX(-50%) translateY(-10px);
  }
  100% {
    opacity: 1;
    transform: translateX(-50%) translateY(0);
  }
}

/* Стили для облачка объяснения LFSR - ПОВЫШЕ */
.lfsr-explanation-bubble {
  position: absolute;
  left: 50%;
  top: -180px; /* Увеличил высоту позиционирования */
  transform: translateX(-50%);
  background: var(--color-bg-elevated);
  border: 2px solid;
  border-radius: 20px;
  padding: var(--spacing-lg);
  max-width: 400px;
  z-index: 1000;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
  animation: bubble-slide-down 0.6s ease-out;
}

.lfsr-explanation-bubble.info {
  border-color: var(--color-primary);
}

.lfsr-explanation-bubble.calculation {
  border-color: var(--color-error);
}

.lfsr-explanation-bubble.shift {
  border-color: var(--color-warning);
}

.lfsr-explanation-bubble.insert {
  border-color: var(--color-success);
}

.lfsr-explanation-bubble::before {
  content: '';
  position: absolute;
  left: 50%;
  bottom: -20px;
  transform: translateX(-50%);
  width: 0;
  height: 0;
  border: 15px solid transparent;
  border-top-color: inherit;
  border-bottom: 0;
}

.bubble-content {
  display: flex;
  align-items: flex-start;
  gap: var(--spacing-md);
}

.bubble-icon {
  font-size: 1.8rem;
  flex-shrink: 0;
  margin-top: 2px;
}

.bubble-text-content {
  flex: 1;
}

.bubble-title {
  color: var(--color-text);
  font-weight: var(--font-weight-bold);
  margin-bottom: var(--spacing-xs);
  font-size: 1rem;
  text-transform: uppercase;
}

.bubble-description {
  color: var(--color-text);
  font-size: 0.95rem;
  line-height: 1.4;
  margin-bottom: var(--spacing-sm);
}

.xor-calculation {
  background: var(--color-bg-subtle);
  padding: var(--spacing-md);
  border-radius: var(--border-radius-md);
  border: 1px solid var(--color-border);
  margin-top: var(--spacing-sm);
}

.xor-formula {
  color: var(--color-error);
  font-weight: var(--font-weight-bold);
  font-size: 0.9rem;
  margin-bottom: var(--spacing-xs);
}

.xor-result {
  color: var(--color-success);
  font-weight: var(--font-weight-bold);
  font-size: 1rem;
}

@keyframes bubble-slide-down {
  0% {
    opacity: 0;
    transform: translateX(-50%) translateY(-30px);
  }
  100% {
    opacity: 1;
    transform: translateX(-50%) translateY(0);
  }
}

/* Стили для подсветки XOR битов */
.xor-highlight .bit-value {
  border-color: var(--color-error) !important;
  background: var(--color-error-soft) !important;
  color: var(--color-error) !important;
  box-shadow: 0 0 12px var(--color-error) !important;
  animation: xor-pulse 1s ease-in-out infinite;
}

@keyframes xor-pulse {
  0%, 100% {
    box-shadow: 0 0 8px var(--color-error);
  }
  50% {
    box-shadow: 0 0 20px var(--color-error);
  }
}

/* Стили для стрелок XOR */
.xor-arrow {
  position: absolute;
  top: -25px;
  display: flex;
  align-items: center;
  animation: arrow-float 1.5s ease-in-out infinite;
}

.arrow-head {
  width: 0;
  height: 0;
  border: 8px solid transparent;
  border-left-color: var(--color-error);
  border-right: 0;
  position: absolute;
  right: -8px;
  top: -6px;
}

.xor-arrow:nth-child(even) .arrow-head {
  border-left-color: transparent;
  border-right-color: var(--color-error);
  border-left: 0;
  right: auto;
  left: 0px;
}

@keyframes arrow-float {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-5px);
  }
}

.empty-bit .bit-value {
  background: var(--color-bg-subtle) !important;
  border-color: var(--color-border) !important;
  color: var(--color-text-muted) !important;
  animation: empty-pulse 1s ease-in-out infinite;
}

@keyframes empty-pulse {
  0%, 100% {
    opacity: 0.7;
  }
  50% {
    opacity: 1;
  }
}

/* Обновленные стили для таблицы */
.dots-row {
  opacity: 0.6;
  font-style: italic;
}

.dots {
  color: var(--color-text-muted);
  font-size: 1.1rem;
}

.binary-digit {
  font-family: 'Courier New', monospace;
  letter-spacing: 1px;
  font-size: 0.9rem;
}

/* Остальные стили остаются без изменений */
.lfsr-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: var(--spacing-xl);
  background: var(--color-bg-subtle);
  border-radius: var(--border-radius-xl);
  box-shadow: var(--shadow-lg);
}

.lfsr-header {
  text-align: center;
  margin-bottom: var(--spacing-2xl);
  border-bottom: 2px solid var(--color-border);
  padding-bottom: var(--spacing-lg);
}

/* Стили для секции преобразования */
.conversion-section {
  background: var(--color-bg-elevated);
  padding: var(--spacing-xl);
  border-radius: var(--border-radius-lg);
  border: 1px solid var(--color-border);
  margin-bottom: var(--spacing-xl);
  box-shadow: var(--shadow-indigo);
  position: relative;
}

.conversion-title {
  text-align: center;
  color: var(--color-primary);
  margin-bottom: var(--spacing-lg);
  font-size: 1.2rem;
}

.conversion-steps {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-lg);
}

.conversion-step {
  height: 70px;
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  padding: var(--spacing-md);
  background: var(--color-bg-subtle);
  border: 1px solid var(--color-border);
  border-radius: var(--border-radius-md);
  position: relative;
  transition: all var(--transition-normal);
}

.conversion-step.final {
  background: var(--color-primary-soft);
  border-color: var(--color-primary);
}

.step-label {
  color: var(--color-text-muted);
  font-size: 0.9rem;
  min-width: 180px;
  text-transform: uppercase;
}

.step-value {
  color: var(--color-text);
  font-weight: var(--font-weight-bold);
  font-size: 0.95rem;
  flex: 1;
  word-break: break-all;
  transition: all var(--transition-normal);
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--border-radius-md);
  border: 1px solid transparent;
}

.step-value.final-value {
  color: var(--color-primary);
  font-size: 1.1rem;
}

.step-animation {
  display: flex;
  gap: 4px;
  margin-left: auto;
}

.animation-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--color-primary);
  animation: pulse-dot 1.4s ease-in-out infinite both;
}

.animation-dot:nth-child(2) {
  animation-delay: 0.2s;
}

.animation-dot:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes pulse-dot {
  0%, 80%, 100% {
    transform: scale(0.8);
    opacity: 0.5;
  }
  40% {
    transform: scale(1.2);
    opacity: 1;
  }
}

/* Стили для таблицы преобразования */
.binary-table {
  background: var(--color-bg-subtle);
  border: 1px solid var(--color-border);
  border-radius: var(--border-radius-md);
  overflow: hidden;
  box-shadow: var(--shadow-sm);
}

.table-header {
  display: flex;
  background: var(--color-primary-soft);
  border-bottom: 1px solid var(--color-border);
}

.table-header > div {
  padding: var(--spacing-md);
  font-weight: var(--font-weight-bold);
  color: var(--color-primary);
  text-align: center;
}

.hex-column {
  flex: 1;
}

.arrow-column {
  width: 80px;
  flex: none;
}

.binary-column {
  flex: 2;
}

.table-body {
  display: flex;
  flex-direction: column;
}

.table-row {
  display: flex;
  border-bottom: 1px solid var(--color-border);
  transition: all var(--transition-normal);
  min-height: 60px;
}

.table-row:last-child {
  border-bottom: none;
}

.table-row.active {
  background: var(--color-accent-soft);
}

.table-row.completed {
  background: var(--color-success-soft);
}

.table-row > div {
  padding: var(--spacing-md);
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
}

.hex-digit, .binary-digit {
  transition: all var(--transition-normal);
  opacity: 0.3;
}

.hex-digit.visible {
  opacity: 1;
  font-weight: var(--font-weight-bold);
  color: var(--color-primary);
  animation: digit-appear 0.5s ease-out;
}

.binary-digit {
  font-family: 'Courier New', monospace;
  letter-spacing: 2px;
}

.binary-digit.visible {
  opacity: 1;
  font-weight: var(--font-weight-bold);
  color: var(--color-accent);
}

.binary-digit.animating {
  animation: binary-pulse 0.6s ease-in-out;
}

@keyframes digit-appear {
  0% {
    opacity: 0;
    transform: scale(0.8);
  }
  70% {
    transform: scale(1.1);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes binary-pulse {
  0%, 100% {
    transform: scale(1);
    color: var(--color-accent);
  }
  50% {
    transform: scale(1.1);
    color: var(--color-primary);
    text-shadow: 0 0 8px var(--color-primary);
  }
}

.arrow-animation {
  font-size: 1.2rem;
  font-weight: var(--font-weight-bold);
  color: var(--color-text-muted);
  transition: all var(--transition-normal);
  opacity: 0.3;
}

.arrow-animation.active {
  color: var(--color-accent);
  opacity: 1;
  animation: arrow-pulse 0.6s ease-in-out infinite;
}

@keyframes arrow-pulse {
  0%, 100% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.3);
    opacity: 0.7;
  }
}

.conversion-controls {
  text-align: center;
  margin-top: var(--spacing-lg);
}

/* Адаптивность для таблицы */
@media (max-width: 768px) {
  .binary-table {
    font-size: 0.9rem;
  }
  
  .table-header > div,
  .table-row > div {
    padding: var(--spacing-sm);
  }
  
  .arrow-column {
    width: 60px;
  }
  
  .table-row {
    min-height: 50px;
  }
}

/* Остальные стили остаются без изменений */
.lfsr-subtitle {
  color: var(--color-text-muted);
  font-size: 1.1rem;
  margin-top: var(--spacing-sm);
}

.lfsr-main {
  display: grid;
  gap: var(--spacing-xl);
  margin-bottom: var(--spacing-2xl);
}

.control-panel {
  background: var(--color-bg-elevated);
  padding: var(--spacing-lg);
  border-radius: var(--border-radius-lg);
  border: 1px solid var(--color-border);
  box-shadow: var(--shadow-indigo);
}

.control-group {
  margin-bottom: var(--spacing-lg);
}

.control-label {
  display: block;
  margin-bottom: var(--spacing-sm);
  color: var(--color-text-muted);
  font-size: 0.9rem;
  text-transform: uppercase;
}

.cyber-select {
  width: 100%;
  padding: var(--spacing-md);
  border: 2px solid var(--color-border);
  border-radius: var(--border-radius-md);
  background: var(--color-bg-subtle);
  color: var(--color-text);
  font-family: 'Rajdhani', sans-serif;
  font-size: 1rem;
  transition: all var(--transition-normal);
}

.cyber-select:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px var(--color-primary-soft);
}

.cyber-select:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.control-buttons {
  display: flex;
  gap: var(--spacing-md);
  justify-content: center;
  flex-wrap: wrap;
}

.cyber-button {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-md) var(--spacing-lg);
  border: 2px solid;
  border-radius: var(--border-radius-md);
  font-family: 'Rajdhani', sans-serif;
  font-weight: var(--font-weight-semibold);
  text-transform: uppercase;
  cursor: pointer;
  transition: all var(--transition-normal);
  background: transparent;
}

.cyber-button.primary {
  border-color: var(--color-primary);
  color: var(--color-primary);
}

.cyber-button.primary:hover:not(:disabled) {
  background: var(--color-primary);
  color: var(--color-text-inverted);
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.cyber-button.secondary {
  border-color: var(--color-accent);
  color: var(--color-accent);
}

.cyber-button.secondary:hover:not(:disabled) {
  background: var(--color-accent);
  color: var(--color-text-inverted);
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.cyber-button.accent {
  border-color: var(--color-warning);
  color: var(--color-warning);
}

.cyber-button.accent:hover {
  background: var(--color-warning);
  color: var(--color-text-inverted);
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.cyber-button.warning {
  border-color: var(--color-error);
  color: var(--color-error);
}

.cyber-button.warning:hover {
  background: var(--color-error);
  color: var(--color-text-inverted);
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.cyber-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none !important;
}

.button-icon {
  font-size: 1.1rem;
}

.register-visualization {
  background: var(--color-bg-elevated);
  padding: var(--spacing-xl);
  border-radius: var(--border-radius-lg);
  border: 1px solid var(--color-border);
  box-shadow: var(--shadow-indigo);
  position: relative;
}

.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: var(--spacing-sm);
  margin-bottom: var(--spacing-lg);
  flex-wrap: wrap;
}

.register-bit {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-xs);
  position: relative;
}

.bit-value {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid var(--color-border);
  border-radius: var(--border-radius-md);
  font-size: 1rem;
  font-weight: var(--font-weight-bold);
  transition: all var(--transition-normal);
}

.bit-1 .bit-value {
  background: var(--color-primary);
  color: var(--color-text-inverted);
  border-color: var(--color-primary);
  box-shadow: 0 0 8px var(--color-primary);
}

.bit-0 .bit-value {
  background: var(--color-bg-subtle);
  color: var(--color-text);
}

.active-tap .bit-value {
  border-color: var(--color-accent);
  background: var(--color-accent-soft);
}

.new-bit .bit-value {
  animation: pulse 0.6s ease-in-out;
  background: var(--color-success);
  color: var(--color-text-inverted);
  border-color: var(--color-success);
}

@keyframes pulse {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
  100% {
    transform: scale(1);
  }
}

.bit-index {
  font-size: 0.7rem;
  color: var(--color-text-light);
}

.tap-connector {
  position: absolute;
  top: -15px;
  width: 2px;
  height: 15px;
  background: var(--color-accent);
}

.state-info {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: var(--spacing-md);
  margin-top: var(--spacing-lg);
}

.state-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-md);
  background: var(--color-bg-subtle);
  border-radius: var(--border-radius-md);
  border: 1px solid var(--color-border);
}

.state-label {
  color: var(--color-text-muted);
  font-size: 0.9rem;
}

.state-value {
  color: var(--color-primary);
  font-weight: var(--font-weight-bold);
  font-size: 1rem;
}

.status-section {
  background: var(--color-bg-elevated);
  padding: var(--spacing-lg);
  border-radius: var(--border-radius-lg);
  border: 1px solid var(--color-border);
  box-shadow: var(--shadow-indigo);
  text-align: center;
}

.status-indicator {
  display: inline-flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-md) var(--spacing-lg);
  border-radius: var(--border-radius-full);
  background: var(--color-bg-subtle);
  border: 2px solid var(--color-border);
  transition: all var(--transition-normal);
}

.status-indicator.active {
  border-color: var(--color-success);
  background: var(--color-success-soft);
}

.status-icon {
  font-size: 1.2rem;
}

.status-text {
  color: var(--color-text);
  font-weight: var(--font-weight-medium);
}

.status-note {
  color: var(--color-text-muted);
  font-size: 0.9rem;
  margin-top: var(--spacing-sm);
  margin-bottom: 0;
}

.info-panel {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: var(--spacing-lg);
}

.info-item {
  background: var(--color-bg-elevated);
  padding: var(--spacing-lg);
  border-radius: var(--border-radius-lg);
  border: 1px solid var(--color-border);
  box-shadow: var(--shadow-sm);
}

.info-title {
  color: var(--color-primary);
  font-size: 1rem;
  margin-bottom: var(--spacing-sm);
  border-bottom: 1px solid var(--color-border);
  padding-bottom: var(--spacing-xs);
}

.info-text {
  color: var(--color-text);
  line-height: 1.6;
  margin: 0;
}

/* Стили для облачка объяснения LFSR - ПЕРВОЕ ПОВЫШЕ, остальные нормально */
.lfsr-explanation-bubble {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  background: var(--color-bg-elevated);
  border: 2px solid;
  border-radius: 20px;
  padding: var(--spacing-lg);
  max-width: 400px;
  z-index: 1000;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
  animation: bubble-slide-down 0.6s ease-out;
}

/* Первое облачко (шаг 1) - ВЫШЕ */
.lfsr-explanation-bubble.calculation {
  border-color: var(--color-error);
  top: -220px; /* Увеличил высоту для первого облачка */
}

/* Остальные облачка - нормальная высота */
.lfsr-explanation-bubble.shift {
  border-color: var(--color-warning);
  top: -180px;
}

.lfsr-explanation-bubble.insert {
  border-color: var(--color-success);
  top: -180px;
}

.lfsr-explanation-bubble.info {
  border-color: var(--color-primary);
  top: -180px;
}

.lfsr-explanation-bubble::before {
  content: '';
  position: absolute;
  left: 50%;
  bottom: -20px;
  transform: translateX(-50%);
  width: 0;
  height: 0;
  border: 15px solid transparent;
  border-top-color: inherit;
  border-bottom: 0;
}
</style>
