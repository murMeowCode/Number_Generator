<template>
  <button
    class="stellar-button"
    :class="buttonClasses"
    :disabled="disabled || loading"
    @click="handleClick"
    @mousedown="createRipple"
    ref="buttonRef"
  >
    <!-- Космический фон с частицами -->
    <div class="cosmic-background">
      <!-- Планеты -->
      <div class="planet planet-1"></div>
      <div class="planet planet-2"></div>
      <div class="planet planet-3"></div>
      
      <!-- Звездное поле -->
      <div v-for="i in starCount" :key="i" class="star" :style="getStarStyle(i)" />
      
      <!-- Туманности -->
      <div class="nebula nebula-1"></div>
      <div class="nebula nebula-2"></div>
      
      <!-- Летающие астероиды -->
      <div v-for="n in 3" :key="'asteroid-' + n" class="asteroid" :style="getAsteroidStyle(n)" />
    </div>

    <!-- Энергетическое свечение -->
    <div class="energy-pulse" :style="{ background: energyPulseColor }"></div>
    
    <!-- Основное свечение -->
    <div class="main-glow" :style="{ background: mainGlowColor }"></div>

    <!-- Содержимое кнопки -->
    <div class="button-content-wrapper">
      <span class="button-content" :class="{ 'content-hidden': loading || isSuccess }">
        <span class="text-glow">
          <slot>
            {{ text }}
          </slot>
        </span>
      </span>

      <!-- Иконка запуска -->
      <div v-if="!loading && !isSuccess" class="launch-icon">
        <div class="rocket">
          <div class="rocket-body"></div>
          <div class="rocket-wings"></div>
          <div class="exhaust">
            <div class="exhaust-particle" v-for="n in 3" :key="n" :style="getExhaustStyle(n)"></div>
          </div>
        </div>
      </div>

      <!-- Success иконка -->
      <div v-if="isSuccess" class="success-icon">
        <div class="success-orb">
          <div class="success-check">
            <svg viewBox="0 0 24 24" class="checkmark">
              <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/>
            </svg>
          </div>
        </div>
        <span class="success-text">Успех!</span>
      </div>

      <!-- Лоадер -->
      <div v-if="loading && !isSuccess" class="stellar-loader">
        <div class="quantum-spinner">
          <div class="quantum-ring"></div>
          <div class="quantum-core"></div>
          <div v-for="n in 4" :key="n" class="quantum-particle" :style="getParticleStyle(n)"></div>
        </div>
        <span class="loading-text">Генерация...</span>
      </div>
    </div>

    <!-- Эффект взрыва звезд -->
    <div v-if="isSuccess" class="galaxy-burst">
      <div v-for="i in burstCount" :key="'burst-' + i" class="burst-star" :style="getBurstStarStyle(i)" />
    </div>

    <!-- Эффект риппла -->
    <div v-if="ripple.visible" class="ripple-effect" :style="rippleStyle" />

    <!-- Энергетическое поле -->
    <div class="energy-field" :style="{ borderColor: energyFieldColor }"></div>
  </button>
</template>

<script setup>
import { ref, computed, reactive } from 'vue'

const props = defineProps({
  text: {
    type: String,
    default: 'Космическая кнопка',
  },
  variant: {
    type: String,
    default: 'primary',
    validator: (value) => ['primary', 'secondary', 'ghost', 'success'].includes(value),
  },
  loading: {
    type: Boolean,
    default: false,
  },
  disabled: {
    type: Boolean,
    default: false,
  },
  color: {
    type: String,
    default: '#6366f1',
  },
  successColor: {
    type: String,
    default: '#10b981',
  },
  size: {
    type: String,
    default: 'medium',
    validator: (value) => ['small', 'medium', 'large'].includes(value),
  },
  success: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['click'])

const buttonRef = ref(null)
const starCount = 15
const burstCount = 16

const ripple = reactive({
  visible: false,
  x: 0,
  y: 0,
})

// Computed свойства
const isSuccess = computed(() => props.variant === 'success' || props.success)

const buttonClasses = computed(() => [
  `stellar-button--${props.variant}`,
  `stellar-button--${props.size}`,
  {
    'stellar-button--loading': props.loading,
    'stellar-button--disabled': props.disabled,
    'stellar-button--success': isSuccess.value,
    'stellar-button--interactive': !props.loading && !props.disabled,
  },
])

const energyPulseColor = computed(() => {
  if (isSuccess.value) {
    return `radial-gradient(circle, ${props.successColor}80 0%, transparent 70%)`
  }
  return `radial-gradient(circle, ${props.color}60 0%, transparent 70%)`
})

const mainGlowColor = computed(() => {
  if (isSuccess.value) {
    return `radial-gradient(ellipse at center, ${props.successColor}40 0%, transparent 80%)`
  }
  return `radial-gradient(ellipse at center, ${props.color}30 0%, transparent 80%)`
})

const energyFieldColor = computed(() => {
  if (isSuccess.value) {
    return `${props.successColor}60`
  }
  return `${props.color}50`
})

const rippleStyle = computed(() => ({
  left: `${ripple.x}px`,
  top: `${ripple.y}px`,
  background: isSuccess.value 
    ? `${props.successColor}80` 
    : props.variant === 'ghost' 
      ? 'rgba(255, 255, 255, 0.4)' 
      : `${props.color}60`,
}))

// Методы
const getStarStyle = (index) => {
  const angle = (index / starCount) * Math.PI * 2
  const distance = 25 + Math.random() * 40
  const size = 1 + Math.random() * 2
  const duration = 2 + Math.random() * 2
  
  return {
    left: `calc(50% + ${Math.cos(angle) * distance}px)`,
    top: `calc(50% + ${Math.sin(angle) * distance}px)`,
    width: `${size}px`,
    height: `${size}px`,
    animationDelay: `${index * 0.2}s`,
    animationDuration: `${duration}s`,
    opacity: 0.4 + Math.random() * 0.6,
  }
}

const getAsteroidStyle = (index) => {
  return {
    animationDelay: `${index * 1.5}s`,
    left: `${-10 + Math.random() * 120}%`,
    top: `${-10 + Math.random() * 120}%`,
    width: `${1 + Math.random() * 3}px`,
    height: `${1 + Math.random() * 3}px`,
  }
}

const getExhaustStyle = (index) => {
  return {
    animationDelay: `${index * 0.3}s`,
  }
}

const getParticleStyle = (index) => {
  const angle = (index / 4) * Math.PI * 2
  return {
    '--particle-angle': `${angle}rad`,
    animationDelay: `${index * 0.3}s`,
  }
}

const getBurstStarStyle = (index) => {
  const angle = (index / burstCount) * Math.PI * 2
  const distance = 50 + Math.random() * 80
  const size = 3 + Math.random() * 5
  const duration = 1 + Math.random() * 0.5
  
  return {
    left: '50%',
    top: '50%',
    width: `${size}px`,
    height: `${size}px`,
    '--burst-angle': `${angle}rad`,
    '--burst-distance': `${distance}px`,
    '--burst-duration': `${duration}s`,
    '--burst-delay': `${index * 0.08}s`,
  }
}

const handleClick = (event) => {
  if (!props.loading && !props.disabled) {
    emit('click', event)
  }
}

const createRipple = (event) => {
  if (props.loading || props.disabled) return

  const button = buttonRef.value
  const rect = button.getBoundingClientRect()

  ripple.x = event.clientX - rect.left
  ripple.y = event.clientY - rect.top
  ripple.visible = true

  setTimeout(() => {
    ripple.visible = false
  }, 800)
}
</script>

<style scoped>
.stellar-button {
  position: relative;
  border: none;
  border-radius: 16px;
  font-family: 'Segoe UI', system-ui, sans-serif;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  overflow: hidden;
  background: transparent;
  color: white;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(20px);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* Размеры */
.stellar-button--small {
  padding: 12px 24px;
  font-size: 0.9rem;
  min-height: 44px;
  min-width: 120px;
}

.stellar-button--medium {
  padding: 16px 32px;
  font-size: 1.1rem;
  min-height: 56px;
  min-width: 200px;
}

.stellar-button--large {
  padding: 20px 40px;
  font-size: 1.3rem;
  min-height: 68px;
  min-width: 240px;
}

/* Варианты */
.stellar-button--primary {
  background: linear-gradient(135deg, 
    v-bind('props.color') 0%, 
    color-mix(in srgb, v-bind('props.color') 70%, black) 50%,
    v-bind('props.color') 100%);
  box-shadow:
    0 8px 40px v-bind('props.color + "60"'),
    0 4px 20px v-bind('props.color + "40"'),
    0 0 0 2px rgba(255, 255, 255, 0.3),
    inset 0 2px 0 rgba(255, 255, 255, 0.4),
    inset 0 -2px 0 rgba(0, 0, 0, 0.2);
}

.stellar-button--success {
  background: linear-gradient(135deg, 
    v-bind('props.successColor') 0%, 
    color-mix(in srgb, v-bind('props.successColor') 70%, black) 50%,
    v-bind('props.successColor') 100%);
  box-shadow:
    0 8px 50px v-bind('props.successColor + "80"'),
    0 4px 25px v-bind('props.successColor + "60"'),
    0 0 0 2px rgba(255, 255, 255, 0.4),
    inset 0 2px 0 rgba(255, 255, 255, 0.5),
    inset 0 -2px 0 rgba(0, 0, 0, 0.2);
  animation: cosmic-success 3s infinite ease-in-out;
}

.stellar-button--secondary {
  background: linear-gradient(135deg, 
    rgba(99, 102, 241, 0.9) 0%,
    rgba(79, 70, 229, 0.8) 100%);
  box-shadow:
    0 8px 40px rgba(99, 102, 241, 0.5),
    0 4px 20px rgba(99, 102, 241, 0.3),
    0 0 0 2px rgba(255, 255, 255, 0.2),
    inset 0 2px 0 rgba(255, 255, 255, 0.3),
    inset 0 -2px 0 rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.stellar-button--ghost {
  background: rgba(255, 255, 255, 0.15);
  color: v-bind('props.color');
  border: 2px solid v-bind('props.color + "60"');
  box-shadow:
    0 4px 20px rgba(0, 0, 0, 0.3),
    0 0 0 1px rgba(255, 255, 255, 0.1);
}

/* Состояния */
.stellar-button--interactive:hover {
  transform: translateY(-4px) scale(1.02);
  box-shadow:
    0 16px 50px v-bind('isSuccess ? props.successColor + "90" : props.color + "80"'),
    0 8px 30px v-bind('isSuccess ? props.successColor + "70" : props.color + "60"'),
    0 0 0 3px rgba(255, 255, 255, 0.4),
    inset 0 3px 0 rgba(255, 255, 255, 0.5);
}

.stellar-button--interactive:active {
  transform: translateY(-1px) scale(1.01);
  transition-duration: 0.1s;
}

.stellar-button--disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none !important;
  filter: grayscale(0.5);
}

.stellar-button--loading {
  cursor: wait;
}

/* Анимации */
@keyframes cosmic-success {
  0%, 100% {
    box-shadow:
      0 8px 50px v-bind('props.successColor + "80"'),
      0 4px 25px v-bind('props.successColor + "60"'),
      0 0 0 2px rgba(255, 255, 255, 0.4),
      inset 0 2px 0 rgba(255, 255, 255, 0.5);
  }
  50% {
    box-shadow:
      0 12px 60px v-bind('props.successColor + "A0"'),
      0 6px 35px v-bind('props.successColor + "80"'),
      0 0 0 3px rgba(255, 255, 255, 0.6),
      inset 0 3px 0 rgba(255, 255, 255, 0.7);
  }
}

/* Космический фон */
.cosmic-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  overflow: hidden;
}

/* Планеты */
.planet {
  position: absolute;
  border-radius: 50%;
  animation: float 8s infinite ease-in-out;
}

.planet-1 {
  width: 6px;
  height: 6px;
  background: linear-gradient(45deg, #ff6b6b, #ffa726);
  top: 20%;
  left: 15%;
  animation-delay: 0s;
}

.planet-2 {
  width: 4px;
  height: 4px;
  background: linear-gradient(45deg, #4ecdc4, #45b7d1);
  top: 70%;
  left: 80%;
  animation-delay: 2s;
}

.planet-3 {
  width: 5px;
  height: 5px;
  background: linear-gradient(45deg, #a166ab, #5073b8);
  top: 40%;
  left: 85%;
  animation-delay: 4s;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px) scale(1);
  }
  50% {
    transform: translateY(-10px) scale(1.1);
  }
}

/* Звезды */
.star {
  position: absolute;
  background: white;
  border-radius: 50%;
  animation: twinkle 4s infinite ease-in-out;
  transform: translate(-50%, -50%);
}

@keyframes twinkle {
  0%, 100% {
    opacity: 0.3;
    transform: translate(-50%, -50%) scale(0.8);
  }
  50% {
    opacity: 1;
    transform: translate(-50%, -50%) scale(1.5);
    box-shadow: 0 0 8px white;
  }
}

/* Астероиды */
.asteroid {
  position: absolute;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 1px;
  animation: fly 6s infinite linear;
}

@keyframes fly {
  0% {
    transform: translateX(-20px) translateY(-20px) rotate(0deg);
    opacity: 0;
  }
  10% {
    opacity: 1;
  }
  90% {
    opacity: 1;
  }
  100% {
    transform: translateX(120px) translateY(120px) rotate(360deg);
    opacity: 0;
  }
}

/* Энергетические эффекты */
.energy-pulse {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 120%;
  height: 120%;
  transform: translate(-50%, -50%);
  opacity: 0;
  animation: energy-pulse 3s infinite ease-in-out;
  pointer-events: none;
}

.main-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 100%;
  height: 100%;
  transform: translate(-50%, -50%);
  opacity: 0.6;
  pointer-events: none;
}

.energy-field {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border: 2px solid;
  border-radius: 16px;
  opacity: 0;
  animation: energy-field-pulse 2s infinite ease-in-out;
  pointer-events: none;
}

@keyframes energy-pulse {
  0%, 100% {
    opacity: 0;
    transform: translate(-50%, -50%) scale(0.8);
  }
  50% {
    opacity: 0.4;
    transform: translate(-50%, -50%) scale(1.1);
  }
}

@keyframes energy-field-pulse {
  0%, 100% {
    opacity: 0.3;
    transform: scale(1);
  }
  50% {
    opacity: 0.7;
    transform: scale(1.05);
  }
}

/* Контент */
.button-content-wrapper {
  position: relative;
  z-index: 10;
  display: flex;
  align-items: center;
  gap: 12px;
}

.button-content {
  position: relative;
  transition: all 0.3s ease;
}

.text-glow {
  text-shadow: 
    0 0 20px rgba(255, 255, 255, 0.8),
    0 0 40px currentColor,
    0 2px 8px rgba(0, 0, 0, 0.3);
}

.content-hidden {
  opacity: 0;
  transform: scale(0.8);
}

/* Иконка запуска */
.launch-icon {
  display: flex;
  align-items: center;
  animation: launch-hover 2s infinite ease-in-out;
}

.rocket {
  position: relative;
  width: 20px;
  height: 20px;
  animation: rocket-tremble 0.3s infinite ease-in-out;
}

.rocket-body {
  width: 12px;
  height: 16px;
  background: white;
  border-radius: 50% 50% 40% 40%;
  position: absolute;
  top: 2px;
  left: 4px;
}

.rocket-wings {
  position: absolute;
  bottom: 0;
  width: 20px;
  height: 6px;
  background: rgba(255, 255, 255, 0.8);
  clip-path: polygon(0% 100%, 50% 0%, 100% 100%);
}

.exhaust {
  position: absolute;
  bottom: -8px;
  left: 6px;
}

.exhaust-particle {
  width: 4px;
  height: 8px;
  background: linear-gradient(to bottom, #ff6b6b, transparent);
  border-radius: 50%;
  margin-top: 2px;
  animation: exhaust-blast 0.6s infinite ease-out;
}

@keyframes launch-hover {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-3px);
  }
}

@keyframes rocket-tremble {
  0%, 100% {
    transform: rotate(-2deg);
  }
  50% {
    transform: rotate(2deg);
  }
}

@keyframes exhaust-blast {
  0% {
    opacity: 0;
    transform: scale(0.5);
  }
  50% {
    opacity: 1;
    transform: scale(1.2);
  }
  100% {
    opacity: 0;
    transform: scale(0.8);
  }
}

/* Success иконка */
.success-icon {
  display: flex;
  align-items: center;
  gap: 10px;
  animation: success-arrival 0.8s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.success-orb {
  width: 24px;
  height: 24px;
  background: radial-gradient(circle, white 30%, transparent 70%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 0 20px white;
}

.success-check {
  width: 16px;
  height: 16px;
}

.checkmark {
  width: 100%;
  height: 100%;
  fill: v-bind('props.successColor');
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.3));
}

.success-text {
  font-weight: 800;
  font-size: 1.2em;
  text-shadow: 
    0 0 20px v-bind('props.successColor'),
    0 2px 8px rgba(0, 0, 0, 0.4);
}

@keyframes success-arrival {
  0% {
    opacity: 0;
    transform: scale(0.5) rotate(-180deg);
  }
  70% {
    transform: scale(1.1) rotate(10deg);
  }
  100% {
    opacity: 1;
    transform: scale(1) rotate(0deg);
  }
}

/* Лоадер */
.stellar-loader {
  display: flex;
  align-items: center;
  gap: 12px;
}

.quantum-spinner {
  position: relative;
  width: 24px;
  height: 24px;
}

.quantum-ring {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  animation: quantum-rotate 2s infinite linear;
}

.quantum-core {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 8px;
  height: 8px;
  background: white;
  border-radius: 50%;
  transform: translate(-50%, -50%);
  box-shadow: 0 0 12px white;
}

.quantum-particle {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 4px;
  height: 4px;
  background: white;
  border-radius: 50%;
  transform: translate(-50%, -50%);
  animation: quantum-orbit 1.5s infinite ease-in-out;
}

.loading-text {
  font-weight: 600;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

@keyframes quantum-rotate {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

@keyframes quantum-orbit {
  0% {
    transform: 
      translate(-50%, -50%) 
      rotate(var(--particle-angle)) 
      translateX(12px) 
      scale(0.8);
    opacity: 0.5;
  }
  50% {
    transform: 
      translate(-50%, -50%) 
      rotate(calc(var(--particle-angle) + 180deg)) 
      translateX(16px) 
      scale(1.2);
    opacity: 1;
  }
  100% {
    transform: 
      translate(-50%, -50%) 
      rotate(calc(var(--particle-angle) + 360deg)) 
      translateX(12px) 
      scale(0.8);
    opacity: 0.5;
  }
}

/* Взрыв галактики */
.galaxy-burst {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.burst-star {
  position: absolute;
  background: radial-gradient(circle, white 30%, transparent 70%);
  border-radius: 50%;
  opacity: 0;
  animation: galaxy-burst-animation var(--burst-duration) ease-out var(--burst-delay) both;
}

@keyframes galaxy-burst-animation {
  0% {
    opacity: 0;
    transform: translate(-50%, -50%) scale(0);
  }
  20% {
    opacity: 1;
  }
  100% {
    opacity: 0;
    transform: 
      translate(
        calc(-50% + cos(var(--burst-angle)) * var(--burst-distance)),
        calc(-50% + sin(var(--burst-angle)) * var(--burst-distance))
      ) scale(2);
  }
}

/* Эффект риппла */
.ripple-effect {
  position: absolute;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  transform: translate(-50%, -50%) scale(0);
  animation: cosmic-ripple 0.8s ease-out;
  pointer-events: none;
}

@keyframes cosmic-ripple {
  to {
    transform: translate(-50%, -50%) scale(15);
    opacity: 0;
  }
}

/* Пульсация для интерактивных кнопок */
.stellar-button--interactive {
  animation: gentle-cosmic-pulse 4s infinite ease-in-out;
}

@keyframes gentle-cosmic-pulse {
  0%, 100% {
    box-shadow:
      0 8px 40px v-bind('isSuccess ? props.successColor + "60" : props.color + "60"'),
      0 4px 20px v-bind('isSuccess ? props.successColor + "40" : props.color + "40"'),
      0 0 0 2px rgba(255, 255, 255, 0.3);
  }
  50% {
    box-shadow:
      0 12px 50px v-bind('isSuccess ? props.successColor + "80" : props.color + "80"'),
      0 6px 30px v-bind('isSuccess ? props.successColor + "60" : props.color + "60"'),
      0 0 0 3px rgba(255, 255, 255, 0.4);
  }
}
</style>