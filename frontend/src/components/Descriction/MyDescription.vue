<template>
  <div class="algorithm-container">
    <!-- Фоновые элементы -->
    <div class="cosmic-bg">
      <div class="star-field">
        <div v-for="i in 30" :key="i" class="star" :style="getStarStyle(i)" />
      </div>
      <div class="orbits">
        <div v-for="(size, index) in [1, 1.3, 1.6, 1.9, 2.2]" :key="index" class="orbit" 
             :style="{ width: `${size * 60}px`, height: `${size * 60}px`, animationDelay: `${index * 0.5}s` }" />
      </div>
    </div>

    <!-- Основной контент -->
    <div class="algorithm-content">
      <!-- Заголовок -->
      <div class="algorithm-header">
        <div class="title-section">
          <div class="accent-planet" />
          <h1 class="main-title cyber-heading">Алгоритм получения случайной последовательности</h1>
        </div>
        <p class="subtitle futurism-elegant">
          Эта страница описывает пошаговый процесс генерации псевдослучайной последовательности 
          на основе Linear Feedback Shift Register (LFSR) с использованием внешних данных для seed
        </p>
      </div>

      <!-- Навигация и шаги -->
      <div class="steps-section">
        <div class="steps-navigation">
          <button class="nav-button prev-button" @click="prevStep" :disabled="currentStep === 0">
            <span class="arrow">←</span>
            Назад
          </button>
          
          <div class="steps-indicator">
            <div v-for="step in steps" :key="step.id" 
                 class="step-dot" 
                 :class="{ active: currentStep === step.id, completed: currentStep > step.id }"
                 @click="goToStep(step.id)">
              <span class="step-number cyber-mono">{{ step.id + 1 }}</span>
            </div>
          </div>

          <button class="nav-button next-button" @click="nextStep" :disabled="currentStep === steps.length - 1">
            Вперед
            <span class="arrow">→</span>
          </button>
        </div>

        <!-- Контейнер шагов -->
        <div class="steps-container">
          <transition-group name="step-transition" tag="div">
            <div v-for="step in visibleSteps" :key="step.id" class="step-card">
              <div class="step-header">
                <div class="step-icon">{{ step.icon }}</div>
                <h2 class="step-title cyber-heading">{{ step.title }}</h2>
                <div class="step-progress cyber-mono">Шаг {{ step.id + 1 }} из {{ steps.length }}</div>
              </div>

              <div class="step-content">
                <p class="step-description futurism-elegant">{{ step.description }}</p>
                
                <div class="step-details">
                  <div v-for="(detail, index) in step.details" :key="index" class="detail-item">
                    <div class="detail-check">✓</div>
                    <span class="detail-text cyber-dynamic">{{ detail }}</span>
                  </div>
                </div>

             

                <!-- Визуализация для шага LFSR -->
                <div v-if="step.id === 2" class="lfsr-visualization">
                  <div class="visualization-title cyber-dynamic">Визуализация LFSR:</div>
                  <div class="register-container">
                    <div v-for="(bit, index) in lfsrState" :key="index" 
                         class="register-bit" :class="{ active: bit === 1 }">
                      {{ bit }}
                    </div>
                  </div>
                  <div class="feedback-info cyber-mono">
                    Feedback: XOR(bit[127], bit[6], bit[1], bit[0])
                  </div>
                </div>
              </div>
            </div>
          </transition-group>
        </div>
      </div>

      <!-- Заключение с навигацией -->
      <div v-if="currentStep === steps.length - 1" class="conclusion-section">
        <div class="conclusion-navigation">
          <button class="nav-button prev-button" @click="prevStep" :disabled="currentStep === 0">
            <span class="arrow">←</span>
            Назад к шагам
          </button>
          
          <div class="conclusion-content">
            <h2 class="conclusion-title cyber-heading">Заключение</h2>
            <p class="conclusion-text futurism-elegant">
              Этот алгоритм сочетает внешнюю энтропию (солнечные данные), криптостойкий LFSR 
              и постобработку для создания высококачественных случайных последовательностей. 
            </p>
          </div>

          <button class="nav-button next-button" @click="restartJourney">
            Начать заново
            <span class="arrow">↺</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Клавиатурная подсказка -->
    <div class="keyboard-hint cyber-mono">
      Используйте ← → для навигации
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

const currentStep = ref(0)

const steps = [
  {
    id: 0,
    icon: '🌞',
    title: 'Получение начального seed из внешних данных',
    description: 'Seed генерируется на основе реальных астрономических данных — текущего коэффициента солнечных рентгеновских вспышек (x-ray flares).',
    details: [
      'Данные запрашиваются с официального API NOAA',
      'Из ответа берётся значение current_ratio',
      'Из дробной части извлекаются последние 16 цифр',
      'Каждая цифра преобразуется в 8 бит',
      'Результат — бинарный seed длиной 128 бит'
    ],
    code: `const getSolarSeed = async () => {
  const response = await fetch(
    'https://services.swpc.noaa.gov/json/goes/primary/xray-flares-latest.json'
  );
  const data = await response.json();
  const ratio = data.current_ratio;
  // ... обработка seed
};`
  },
  {
    id: 1,
    icon: '🔧',
    title: 'Обработка seed и инициализация LFSR',
    description: 'Полученный seed используется для инициализации состояния Linear Feedback Shift Register (LFSR).',
    details: [
      'Длина регистра: 128 бит',
      'Полином обратной связи: [128, 7, 2, 1]',
      'Максимальный период: 2^128 - 1 символов',
      'Примитивный полином для полного периода'
    ],
    code: `class LFSR {
  constructor(seed) {
    this.state = seed;
    this.polynomial = [128, 7, 2, 1];
  }
  
  nextBit() {
    // ... генерация следующего бита
  }
}`
  },
  {
    id: 2,
    icon: '🔄',
    title: 'Генерация битов с помощью LFSR',
    description: 'LFSR работает как сдвиговый регистр: каждый шаг генерирует новый бит, сдвигает состояние и вставляет бит обратной связи.',
    details: [
      'Выходной бит: младший бит текущего состояния',
      'Бит обратной связи: XOR позиций полинома',
      'Сдвиг состояния вправо на 1 бит',
      'Feedback_bit вставляется в старший бит',
      'Равномерное распределение 0 и 1'
    ]
  },
  {
    id: 3,
    icon: '📊',
    title: 'Коррекция битов методом фон Неймана',
    description: 'Чтобы улучшить случайность и устранить возможные корреляции, применяется метод фон Неймана.',
    details: [
      'Пары битов преобразуются в один бит',
      '(0,1) → выводим 0',
      '(1,0) → выводим 1',
      '(0,0) и (1,1) игнорируются',
      'Более равномерное распределение 50/50'
    ],
    code: `function vonNeumannDebiasing(bits) {
  const result = [];
  for (let i = 0; i < bits.length - 1; i += 2) {
    if (bits[i] === 0 && bits[i + 1] === 1) {
      result.push(0);
    } else if (bits[i] === 1 && bits[i + 1] === 0) {
      result.push(1);
    }
  }
  return result;
}`
  },
  {
    id: 4,
    icon: '🎯',
    title: 'Получение финальной случайной последовательности',
    description: 'После коррекции битов, последовательность обрезается до нужной длины и используется для извлечения уникальных чисел.',
    details: [
      'Биты группируются по 8 (байты)',
      'Преобразование в числа от 0 до 255',
      'Выбор уникальных чисел в заданном диапазоне',
      'Повтор процесса при недостатке уникальных чисел',
      'Сохранение в БД с метаданными для верификации'
    ]
  }
]

// Состояние для визуализации LFSR
const lfsrState = ref(Array(8).fill(0).map(() => Math.round(Math.random())))

const visibleSteps = computed(() => {
  return steps.filter(step => step.id === currentStep.value)
})

const nextStep = () => {
  if (currentStep.value < steps.length - 1) {
    currentStep.value++
  }
}

const prevStep = () => {
  if (currentStep.value > 0) {
    currentStep.value--
  }
}

const goToStep = (stepId) => {
  currentStep.value = stepId
}

const restartJourney = () => {
  currentStep.value = 0
}

const getStarStyle = (index) => {
  return {
    left: `${Math.random() * 100}%`,
    top: `${Math.random() * 100}%`,
    animationDelay: `${Math.random() * 3}s`,
    opacity: 0.3 + Math.random() * 0.7
  }
}

const copyCode = async (code) => {
  try {
    await navigator.clipboard.writeText(code)
    // Можно добавить уведомление об успешном копировании
    console.log('Код скопирован в буфер обмена')
  } catch (err) {
    console.error('Ошибка копирования: ', err)
  }
}

// Обработка клавиатуры
const handleKeydown = (event) => {
  if (event.key === 'ArrowLeft') {
    prevStep()
  } else if (event.key === 'ArrowRight') {
    nextStep()
  }
}

onMounted(() => {
  window.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeydown)
})
</script>

<style scoped>
/* Подключение шрифтов */
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700;900&family=Rajdhani:wght@300;400;500;600;700&family=Exo+2:wght@100;200;300;400;500;600;700;800;900&family=Share+Tech+Mono&display=swap');

/* CSS переменные с вашими цветами */
:root {
  /* Основные цвета */
  --color-midnight: #212842;
  --color-vanilla: #f0e7d5;
  --color-midnight-light: #2d3a5a;
  --color-midnight-medium: #3a4a7a;
  --color-vanilla-light: #f8f2e8;
  --color-vanilla-dark: #d8cfc0;

  /* Фоны */
  --color-bg: var(--color-midnight);
  --color-bg-muted: var(--color-midnight-light);
  --color-bg-subtle: #1a2036;
  --color-bg-elevated: var(--color-midnight-light);

  /* Текст */
  --color-text: var(--color-vanilla);
  --color-text-muted: #d8cfc0;
  --color-text-inverted: var(--color-midnight);
  --color-text-light: #a0a8c0;

  /* Акценты */
  --color-primary: var(--color-vanilla);
  --color-primary-hover: #f8f2e8;
  --color-accent: var(--color-vanilla);
  --color-accent-hover: #f8f2e8;

  /* Градиенты */
  --gradient-primary: linear-gradient(135deg, var(--color-vanilla) 0%, #a0a8c0 100%);
  --gradient-midnight: linear-gradient(135deg, var(--color-midnight) 0%, var(--color-midnight-light) 50%, var(--color-midnight-medium) 100%);
  --gradient-accent: linear-gradient(135deg, var(--color-vanilla) 0%, var(--color-midnight) 100%);

  /* Тени */
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.6), 0 2px 4px -1px rgba(0, 0, 0, 0.5);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.7), 0 4px 6px -2px rgba(0, 0, 0, 0.6);
  --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.8), 0 10px 10px -5px rgba(0, 0, 0, 0.7);

  /* Transition */
  --transition-normal: 250ms cubic-bezier(0.4, 0, 0.2, 1);
}

.algorithm-container {
  position: relative;
  min-height: 100vh;
  background: var(--gradient-midnight);
  color: var(--color-text);
  font-family: 'Exo 2', 'Rajdhani', 'Space Grotesk', sans-serif;
  overflow-x: hidden;
}

/* Космический фон */
.cosmic-bg {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 0;
}

.star-field {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.star {
  position: absolute;
  width: 1.5px;
  height: 1.5px;
  background: var(--color-vanilla);
  border-radius: 50%;
  animation: twinkle 3s infinite ease-in-out;
}

@keyframes twinkle {
  0%, 100% { opacity: 0.3; transform: scale(0.8); }
  50% { opacity: 1; transform: scale(1.2); }
}

.orbits {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.orbit {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  border: 1px solid rgba(99, 102, 241, 0.15);
  border-radius: 50%;
  animation: rotate 25s infinite linear;
}

@keyframes rotate {
  from { transform: translate(-50%, -50%) rotate(0deg); }
  to { transform: translate(-50%, -50%) rotate(360deg); }
}

/* Основной контент */
.algorithm-content {
  position: relative;
  z-index: 2;
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
}

/* Заголовок */
.algorithm-header {
  text-align: center;
  margin-bottom: 60px;
}

.title-section {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
  margin-bottom: 20px;
}

.accent-planet {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: var(--gradient-primary);
  animation: pulse 2s infinite ease-in-out;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}

.main-title {
  font-size: 2.5rem;
  font-weight: 700;
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0;
}

.subtitle {
  font-size: 1.2rem;
  color: var(--color-text-muted);
  max-width: 800px;
  margin: 0 auto;
  line-height: 1.6;
}

/* Навигация */
.steps-navigation {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 40px;
  gap: 20px;
}

.nav-button {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: rgba(240, 231, 213, 0.1);
  border: 1px solid rgba(240, 231, 213, 0.2);
  border-radius: 10px;
  color: var(--color-text);
  font-family: inherit;
  font-weight: 600;
  cursor: pointer;
  transition: all var(--transition-normal);
  backdrop-filter: blur(10px);
}

.nav-button:hover:not(:disabled) {
  background: rgba(240, 231, 213, 0.15);
  transform: translateY(-2px);
  box-shadow: 0 4px 20px rgba(240, 231, 213, 0.3);
  border-color: var(--color-vanilla);
}

.nav-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

.arrow {
  font-size: 1.2em;
}

.steps-indicator {
  display: flex;
  gap: 10px;
}

.step-dot {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(240, 231, 213, 0.1);
  border: 2px solid rgba(240, 231, 213, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all var(--transition-normal);
  position: relative;
}

.step-dot.active {
  background: var(--gradient-primary);
  border-color: var(--color-vanilla);
  box-shadow: 0 0 20px rgba(240, 231, 213, 0.5);
}

.step-dot.completed {
  background: linear-gradient(135deg, #10b981, #34d399);
  border-color: #10b981;
}

.step-number {
  font-weight: 600;
  font-size: 0.9rem;
  color: var(--color-text);
}

/* Карточки шагов */
.steps-container {
  min-height: 500px;
  position: relative;
}

.step-card {
  background: rgba(240, 231, 213, 0.1);
  border-radius: 20px;
  padding: 40px;
  backdrop-filter: blur(20px);
  border: 1px solid rgba(240, 231, 213, 0.2);
  box-shadow: var(--shadow-xl);
  margin-bottom: 30px;
}

.step-header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid rgba(240, 231, 213, 0.1);
}

.step-icon {
  font-size: 2.5rem;
}

.step-title {
  font-size: 1.8rem;
  font-weight: 600;
  color: var(--color-text);
  margin: 0;
  flex: 1;
}

.step-progress {
  background: rgba(240, 231, 213, 0.2);
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--color-text-muted);
}

.step-content {
  color: var(--color-text);
}

.step-description {
  font-size: 1.1rem;
  line-height: 1.6;
  margin-bottom: 25px;
  color: var(--color-text-muted);
}

.step-details {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 30px;
}

.detail-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.detail-check {
  color: #10b981;
  font-weight: bold;
  font-size: 1.1rem;
  flex-shrink: 0;
  margin-top: 2px;
}

.detail-text {
  line-height: 1.5;
  color: var(--color-text);
}

/* Блоки кода */
.code-block {
  background: rgba(33, 40, 66, 0.4);
  border-radius: 12px;
  overflow: hidden;
  margin: 25px 0;
  border: 1px solid rgba(240, 231, 213, 0.1);
}

.code-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 20px;
  background: rgba(33, 40, 66, 0.6);
  border-bottom: 1px solid rgba(240, 231, 213, 0.1);
}

.code-language {
  color: var(--color-text-light);
  font-weight: 600;
  font-size: 0.9rem;
}

.copy-button {
  background: rgba(240, 231, 213, 0.3);
  border: none;
  padding: 6px 12px;
  border-radius: 6px;
  color: var(--color-text);
  font-family: inherit;
  font-size: 0.8rem;
  cursor: pointer;
  transition: background var(--transition-normal);
}

.copy-button:hover {
  background: rgba(240, 231, 213, 0.5);
}

.code-content {
  padding: 20px;
  margin: 0;
  overflow-x: auto;
  color: var(--color-text);
  line-height: 1.5;
}

/* Визуализация LFSR */
.lfsr-visualization {
  background: rgba(33, 40, 66, 0.3);
  border-radius: 12px;
  padding: 20px;
  margin-top: 25px;
  border: 1px solid rgba(240, 231, 213, 0.3);
}

.visualization-title {
  font-weight: 600;
  margin-bottom: 15px;
  color: var(--color-text-muted);
}

.register-container {
  display: flex;
  gap: 4px;
  margin-bottom: 15px;
  flex-wrap: wrap;
  justify-content: center;
}

.register-bit {
  width: 30px;
  height: 30px;
  border: 2px solid rgba(240, 231, 213, 0.5);
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  background: rgba(33, 40, 66, 0.5);
  transition: all var(--transition-normal);
  color: var(--color-text);
}

.register-bit.active {
  background: var(--gradient-primary);
  border-color: var(--color-vanilla);
  box-shadow: 0 0 10px rgba(240, 231, 213, 0.5);
  color: var(--color-midnight);
}

.feedback-info {
  text-align: center;
  color: var(--color-text-light);
  font-size: 0.9rem;
}

/* Заключение с навигацией */
.conclusion-section {
  margin-top: 60px;
}

.conclusion-navigation {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 30px;
  background: linear-gradient(135deg, rgba(240, 231, 213, 0.1), rgba(139, 92, 246, 0.1));
  border-radius: 20px;
  padding: 40px;
  border: 1px solid rgba(240, 231, 213, 0.1);
}

.conclusion-content {
  flex: 1;
  text-align: center;
}

.conclusion-title {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 20px;
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.conclusion-text {
  font-size: 1.1rem;
  line-height: 1.6;
  color: var(--color-text-muted);
  max-width: 800px;
  margin: 0 auto;
}

/* Клавиатурная подсказка */
.keyboard-hint {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background: rgba(33, 40, 66, 0.7);
  padding: 10px 16px;
  border-radius: 20px;
  font-size: 0.8rem;
  color: var(--color-text-light);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(240, 231, 213, 0.1);
}

/* Анимации переходов */
.step-transition-enter-active,
.step-transition-leave-active {
  transition: all 0.5s ease;
}

.step-transition-enter-from {
  opacity: 0;
  transform: translateX(50px);
}

.step-transition-leave-to {
  opacity: 0;
  transform: translateX(-50px);
}

/* Адаптивность */
@media (max-width: 768px) {
  .algorithm-content {
    padding: 20px 15px;
  }

  .main-title {
    font-size: 2rem;
  }

  .title-section {
    flex-direction: column;
    gap: 10px;
  }

  .steps-navigation {
    flex-direction: column;
    gap: 15px;
  }

  .step-card {
    padding: 25px;
  }

  .step-header {
    flex-direction: column;
    text-align: center;
    gap: 15px;
  }

  .step-title {
    font-size: 1.5rem;
  }

  .register-container {
    gap: 2px;
  }

  .register-bit {
    width: 25px;
    height: 25px;
    font-size: 0.8rem;
  }

  .conclusion-navigation {
    flex-direction: column;
    gap: 20px;
    text-align: center;
  }

  .conclusion-content {
    order: -1;
  }
}

@media (max-width: 480px) {
  .main-title {
    font-size: 1.6rem;
  }

  .step-card {
    padding: 20px;
  }

  .steps-indicator {
    gap: 5px;
  }

  .step-dot {
    width: 35px;
    height: 35px;
  }

  .conclusion-navigation {
    padding: 25px;
  }
}
</style>