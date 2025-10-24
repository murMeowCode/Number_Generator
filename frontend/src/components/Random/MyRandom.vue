<template>
  <div class="cosmic-description">
    <!-- Фоновые элементы -->
    <div class="cosmic-bg">
      <div class="star-field">
        <div
          v-for="i in 30"
          :key="i"
          class="star"
          :style="{
            left: `${Math.random() * 100}%`,
            top: `${Math.random() * 100}%`,
            animationDelay: `${Math.random() * 3}s`,
          }"
        />
      </div>

      <!-- Орбиты планет -->
      <div class="orbits">
        <div
          v-for="(size, index) in [1, 1.3, 1.6, 1.9, 2.2, 2.5]"
          :key="index"
          class="orbit"
          :style="{
            width: `${size * 40}px`,
            height: `${size * 40}px`,
            animationDelay: `${index * 0.5}s`,
          }"
        />
      </div>
    </div>

    <!-- Контент -->
    <div class="cosmic-content">
      <div class="title-section">
        <div
          class="accent-planet"
          :style="{
            backgroundColor: accentColor,
            boxShadow: `0 0 20px ${accentColor}80`,
          }"
        />
        <h1 class="cosmic-title">{{ title }}</h1>
      </div>

      <p class="cosmic-subtitle">{{ description }}</p>


      <!-- Декоративные планеты -->
      <div class="floating-planets">
        <div class="planet planet-1" :style="{ animationDelay: '0s' }" />
        <div class="planet planet-2" :style="{ animationDelay: '1.5s' }" />
        <div class="planet planet-3" :style="{ animationDelay: '3s' }" />
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CosmicDescription',
  props: {
    title: {
      type: String,
      default: 'Солнечная система',
    },
    description: {
      type: String,
      default: 'Наша космическая обитель в бескрайней Вселенной',
    },
    features: {
      type: Array,
      default: () => [
        '8 планет, вращающихся вокруг звезды',
        'Более 200 спутников',
        'Возраст: 4.6 млрд лет',
        'Диаметр: 287 млрд км',
      ],
    },
    accentColor: {
      type: String,
      default: '#6366f1',
    },
  },
  methods: {
    hoverFeature(index) {
      console.log(`Hovered feature ${index}`)
    },
    resetFeature() {
      // Сброс состояний при уходе курсора
    },
  },
}
</script>

<style scoped>
.cosmic-description {
  position: relative;
  background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
  color: #ffffff;
  padding: 1.5rem;
  border-radius: 16px;
  overflow: hidden;
  font-family: 'Segoe UI', system-ui, sans-serif;
  min-height: 320px;
  width: 100%;
  max-width: 620px;
  border: 1px solid #2a2a4a;
  box-shadow:
    0 0 30px rgba(99, 102, 241, 0.1),
    inset 0 0 60px rgba(99, 102, 241, 0.05);
  display: flex;
  flex-direction: column;
}

/* Фоновые звезды */
.star-field {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.star {
  position: absolute;
  width: 1.5px;
  height: 1.5px;
  background: #ffffff;
  border-radius: 50%;
  animation: twinkle 3s infinite ease-in-out;
}

@keyframes twinkle {
  0%,
  100% {
    opacity: 0.3;
    transform: scale(0.8);
  }
  50% {
    opacity: 1;
    transform: scale(1.2);
  }
}

/* Орбиты */
.orbits {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  pointer-events: none;
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
  from {
    transform: translate(-50%, -50%) rotate(0deg);
  }
  to {
    transform: translate(-50%, -50%) rotate(360deg);
  }
}

/* Контент */
.cosmic-content {
  position: relative;
  z-index: 2;
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0; /* Важно для правильного скролла */
}

.title-section {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  margin-bottom: 1rem;
  flex-shrink: 0;
}

.accent-planet {
  width: 14px;
  height: 14px;
  border-radius: 50%;
  animation: pulse 2s infinite ease-in-out;
  flex-shrink: 0;
}

@keyframes pulse {
  0%,
  100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
}

.cosmic-title {
  font-size: 1.5rem;
  font-weight: 700;
  background: linear-gradient(135deg, #ffffff 0%, #c7d2fe 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0;
  line-height: 1.2;
  word-wrap: break-word;
  overflow-wrap: break-word;
}

.cosmic-subtitle {
  font-size: 1.2rem;
  color: #c7d2fe;
  margin-bottom: 1rem;
  line-height: 1.4;
  flex-shrink: 0;
  word-wrap: break-word;
  overflow-wrap: break-word;
}

/* Контейнер для списка особенностей */
.features-container {
  flex: 1;
  min-height: 0;
  overflow: hidden;
  position: relative;
}

.features-grid {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
  max-height: 100%;
  overflow-y: auto;
  padding-right: 4px;
  scrollbar-width: thin;
  scrollbar-color: rgba(99, 102, 241, 0.3) transparent;
}

/* Стилизация скроллбара для Webkit браузеров */
.features-grid::-webkit-scrollbar {
  width: 4px;
}

.features-grid::-webkit-scrollbar-track {
  background: transparent;
  border-radius: 2px;
}

.features-grid::-webkit-scrollbar-thumb {
  background: rgba(99, 102, 241, 0.3);
  border-radius: 2px;
}

.features-grid::-webkit-scrollbar-thumb:hover {
  background: rgba(99, 102, 241, 0.5);
}

.feature-item {
  display: flex;
  align-items: flex-start;
  gap: 0.7rem;
  padding: 0.5rem 0.7rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(8px);
  transition: all 0.3s ease;
  cursor: pointer;
  flex-shrink: 0;
}

.feature-item:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: translateX(3px);
}

.feature-dot {
  width: 5px;
  height: 5px;
  border-radius: 50%;
  flex-shrink: 0;
  margin-top: 0.35rem;
}

.feature-text {
  font-size: 0.85rem;
  line-height: 1.3;
  color: #e2e8f0;
  word-wrap: break-word;
  overflow-wrap: break-word;
  flex: 1;
}

/* Плавающие планеты */
.floating-planets {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  width: 50px;
  pointer-events: none;
  z-index: 1;
}

.planet {
  position: absolute;
  border-radius: 50%;
  animation: float 6s infinite ease-in-out;
}

.planet-1 {
  width: 10px;
  height: 10px;
  background: linear-gradient(135deg, #f59e0b, #fbbf24);
  top: 20%;
  right: 15%;
}

.planet-2 {
  width: 8px;
  height: 8px;
  background: linear-gradient(135deg, #10b981, #34d399);
  top: 60%;
  right: 25%;
}

.planet-3 {
  width: 12px;
  height: 12px;
  background: linear-gradient(135deg, #8b5cf6, #a78bfa);
  top: 40%;
  right: 10%;
}

@keyframes float {
  0%,
  100% {
    transform: translateY(0px) scale(1);
  }
  50% {
    transform: translateY(-12px) scale(1.05);
  }
}

/* Адаптивность */
@media (max-width: 480px) {
  .cosmic-description {
    padding: 1.2rem;
    min-height: 300px;
    max-width: 100%;
  }

  .cosmic-title {
    font-size: 1.3rem;
  }

  .cosmic-subtitle {
    font-size: 0.85rem;
  }

  .feature-item {
    padding: 0.4rem 0.6rem;
    gap: 0.6rem;
  }

  .feature-text {
    font-size: 0.8rem;
  }

  .floating-planets {
    width: 35px;
  }

  .orbits {
    transform: translate(-50%, -50%) scale(0.6);
  }

  .title-section {
    gap: 0.6rem;
    margin-bottom: 0.8rem;
  }

  .accent-planet {
    width: 12px;
    height: 12px;
  }
}

/* Для очень маленьких экранов */
@media (max-width: 360px) {
  .cosmic-description {
    padding: 1rem;
    min-height: 280px;
  }

  .cosmic-title {
    font-size: 1.2rem;
  }

  .features-grid {
    gap: 0.5rem;
  }

  .feature-item {
    padding: 0.35rem 0.5rem;
  }

  .floating-planets {
    display: none; /* Скрываем планеты на очень маленьких экранах */
  }
}

/* Обеспечиваем правильное отображение длинного текста */
.cosmic-title,
.cosmic-subtitle,
.feature-text {
  hyphens: auto;
  -webkit-hyphens: auto;
  -ms-hyphens: auto;
}

/* Улучшаем читаемость при переполнении */
.features-grid {
  mask-image: linear-gradient(to bottom, transparent 0%, black 10%, black 90%, transparent 100%);
}
</style>
