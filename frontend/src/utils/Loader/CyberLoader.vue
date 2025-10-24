<template>
  <div class="cyber-loader" :class="[size, variant]">
    <div class="loader-core"></div>
    <div class="loader-orbit"></div>
    <div class="loader-particles">
      <div v-for="n in particleCount" :key="n" class="particle" :style="getParticleStyle(n)"></div>
    </div>
    <div class="loader-glow"></div>
    <div v-if="showText" class="loader-text cyber-mono">
      {{ text }}
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  size: {
    type: String,
    default: 'medium',
    validator: (value) => ['small', 'medium', 'large', 'xlarge'].includes(value),
  },
  variant: {
    type: String,
    default: 'primary',
    validator: (value) => ['primary', 'success', 'warning', 'error'].includes(value),
  },
  showText: {
    type: Boolean,
    default: false,
  },
  text: {
    type: String,
    default: 'Загрузка...',
  },
})

const particleCount = 8

const getParticleStyle = (index) => {
  const angle = (index / particleCount) * 360
  const delay = (index / particleCount) * 1.5
  return {
    '--particle-angle': `${angle}deg`,
    '--particle-delay': `${delay}s`,
  }
}
</script>

<style scoped>
.cyber-loader {
  position: relative;
  display: inline-flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

/* Размеры */
.cyber-loader.small {
  width: 30px;
  height: 30px;
}

.cyber-loader.medium {
  width: 50px;
  height: 50px;
}

.cyber-loader.large {
  width: 80px;
  height: 80px;
}

.cyber-loader.xlarge {
  width: 120px;
  height: 120px;
}

/* Варианты цветов */
.cyber-loader.primary {
  --loader-color: var(--color-primary);
}

.cyber-loader.success {
  --loader-color: var(--color-success);
}

.cyber-loader.warning {
  --loader-color: var(--color-warning);
}

.cyber-loader.error {
  --loader-color: var(--color-error);
}

/* Основные элементы лоадера */
.loader-core {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 20%;
  height: 20%;
  background: var(--loader-color);
  border-radius: 50%;
  transform: translate(-50%, -50%);
  animation: pulse-core 2s ease-in-out infinite;
  box-shadow:
    0 0 10px var(--loader-color),
    0 0 20px var(--loader-color);
  z-index: 3;
}

.loader-orbit {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 100%;
  height: 100%;
  border: 2px solid transparent;
  border-top: 2px solid var(--loader-color);
  border-radius: 50%;
  animation: spin-orbit 1.5s linear infinite;
  transform: translate(-50%, -50%) rotate(0deg);
}

.loader-particles {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 100%;
  height: 100%;
  transform: translate(-50%, -50%);
}

.particle {
  position: absolute;
  width: 12%;
  height: 12%;
  background: var(--loader-color);
  border-radius: 50%;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%) rotate(var(--particle-angle)) translateX(40px)
    rotate(calc(-1 * var(--particle-angle)));
  animation:
    particle-rotate 3s linear infinite var(--particle-delay),
    particle-pulse 1.5s ease-in-out infinite var(--particle-delay);
  box-shadow: 0 0 8px var(--loader-color);
}

.loader-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 120%;
  height: 120%;
  background: radial-gradient(circle, var(--loader-color) 0%, transparent 70%);
  opacity: 0.1;
  transform: translate(-50%, -50%);
  border-radius: 50%;
  animation: glow-pulse 2s ease-in-out infinite;
  z-index: 1;
}

.loader-text {
  margin-top: 20px;
  color: var(--loader-color);
  font-size: 0.9rem;
  text-align: center;
  text-shadow: 0 0 10px var(--loader-color);
  animation: text-flicker 2s ease-in-out infinite;
}

.cyber-loader.small .loader-text {
  margin-top: 8px;
  font-size: 0.7rem;
}

.cyber-loader.medium .loader-text {
  margin-top: 12px;
  font-size: 0.8rem;
}

.cyber-loader.large .loader-text {
  margin-top: 16px;
  font-size: 0.9rem;
}

.cyber-loader.xlarge .loader-text {
  margin-top: 20px;
  font-size: 1rem;
}

/* Анимации */
@keyframes spin-orbit {
  0% {
    transform: translate(-50%, -50%) rotate(0deg);
    border-top-color: var(--loader-color);
    border-right-color: transparent;
    border-bottom-color: transparent;
    border-left-color: transparent;
  }
  25% {
    border-top-color: transparent;
    border-right-color: var(--loader-color);
    border-bottom-color: transparent;
    border-left-color: transparent;
  }
  50% {
    border-top-color: transparent;
    border-right-color: transparent;
    border-bottom-color: var(--loader-color);
    border-left-color: transparent;
  }
  75% {
    border-top-color: transparent;
    border-right-color: transparent;
    border-bottom-color: transparent;
    border-left-color: var(--loader-color);
  }
  100% {
    transform: translate(-50%, -50%) rotate(360deg);
    border-top-color: var(--loader-color);
    border-right-color: transparent;
    border-bottom-color: transparent;
    border-left-color: transparent;
  }
}

@keyframes pulse-core {
  0%,
  100% {
    transform: translate(-50%, -50%) scale(1);
    box-shadow:
      0 0 10px var(--loader-color),
      0 0 20px var(--loader-color);
  }
  50% {
    transform: translate(-50%, -50%) scale(1.3);
    box-shadow:
      0 0 20px var(--loader-color),
      0 0 40px var(--loader-color),
      0 0 60px var(--loader-color);
  }
}

@keyframes particle-rotate {
  0% {
    transform: translate(-50%, -50%) rotate(var(--particle-angle)) translateX(40px)
      rotate(calc(-1 * var(--particle-angle)));
  }
  100% {
    transform: translate(-50%, -50%) rotate(calc(var(--particle-angle) + 360deg)) translateX(40px)
      rotate(calc(-1 * var(--particle-angle) - 360deg));
  }
}

@keyframes particle-pulse {
  0%,
  100% {
    opacity: 0.7;
    transform: translate(-50%, -50%) rotate(var(--particle-angle)) translateX(40px)
      rotate(calc(-1 * var(--particle-angle))) scale(1);
  }
  50% {
    opacity: 1;
    transform: translate(-50%, -50%) rotate(var(--particle-angle)) translateX(40px)
      rotate(calc(-1 * var(--particle-angle))) scale(1.2);
  }
}

@keyframes glow-pulse {
  0%,
  100% {
    opacity: 0.1;
    transform: translate(-50%, -50%) scale(1);
  }
  50% {
    opacity: 0.2;
    transform: translate(-50%, -50%) scale(1.1);
  }
}

@keyframes text-flicker {
  0%,
  100% {
    opacity: 1;
    text-shadow: 0 0 10px var(--loader-color);
  }
  50% {
    opacity: 0.8;
    text-shadow: 0 0 5px var(--loader-color);
  }
}

/* Адаптивность для разных размеров */
.cyber-loader.small .particle {
  transform: translate(-50%, -50%) rotate(var(--particle-angle)) translateX(12px)
    rotate(calc(-1 * var(--particle-angle)));
}

.cyber-loader.medium .particle {
  transform: translate(-50%, -50%) rotate(var(--particle-angle)) translateX(20px)
    rotate(calc(-1 * var(--particle-angle)));
}

.cyber-loader.large .particle {
  transform: translate(-50%, -50%) rotate(var(--particle-angle)) translateX(32px)
    rotate(calc(-1 * var(--particle-angle)));
}

.cyber-loader.xlarge .particle {
  transform: translate(-50%, -50%) rotate(var(--particle-angle)) translateX(48px)
    rotate(calc(-1 * var(--particle-angle)));
}
</style>
