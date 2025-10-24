<template>
  <div class="error-page">
    <div class="error-background">
      <div class="error-glow error-glow-1"></div>
      <div class="error-glow error-glow-2"></div>
      <div class="error-glow error-glow-3"></div>
    </div>

    <div class="error-container">
      <div class="error-content">
        <div class="error-header">
          <div class="error-number">
            <span class="number-digit">4</span>
            <div class="error-orb">
              <svg
                class="face"
                viewBox="0 0 320 380"
                width="120"
                height="142"
                aria-label="Анимированное лицо 404"
              >
                <g
                  fill="none"
                  :stroke="currentColor"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="25"
                >
                  <g class="face__eyes" transform="translate(0, 112.5)">
                    <g transform="translate(15, 0)">
                      <polyline class="face__eye-lid" points="37,0 0,120 75,120" />
                      <polyline
                        class="face__pupil"
                        points="55,120 55,155"
                        stroke-dasharray="35 35"
                      />
                    </g>
                    <g transform="translate(230, 0)">
                      <polyline class="face__eye-lid" points="37,0 0,120 75,120" />
                      <polyline
                        class="face__pupil"
                        points="55,120 55,155"
                        stroke-dasharray="35 35"
                      />
                    </g>
                  </g>
                  <rect
                    class="face__nose"
                    rx="4"
                    ry="4"
                    x="132.5"
                    y="112.5"
                    width="55"
                    height="155"
                  />
                  <g stroke-dasharray="102 102" transform="translate(65, 334)">
                    <path
                      class="face__mouth-left"
                      d="M 0 30 C 0 30 40 0 95 0"
                      stroke-dashoffset="-102"
                    />
                    <path
                      class="face__mouth-right"
                      d="M 95 0 C 150 0 190 30 190 30"
                      stroke-dashoffset="102"
                    />
                  </g>
                </g>
              </svg>
            </div>
            <span class="number-digit">4</span>
          </div>
        </div>

        <div class="error-text">
          <h1 class="error-title">Страница не найдена</h1>
          <p class="error-description">
            Кажется, мы не можем найти то, что вы ищете. Возможно, страница была перемещена или
            удалена.
          </p>
        </div>

        <div class="error-actions">
          <button @click="goBack" class="btn btn-ghost">
            <span class="btn-icon">←</span>
            Вернуться назад
          </button>
          <button @click="goHome" class="btn btn-primary">
            <span class="btn-icon">🏠</span>
            На главную страницу
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Error404',
  computed: {
    currentColor() {
      return (
        getComputedStyle(document.documentElement).getPropertyValue('--color-primary').trim() ||
        '#3b82f6'
      )
    },
  },
  methods: {
    goBack() {
      if (window.history.length > 2) {
        this.$router.go(-1)
      } else {
        this.goHome()
      }
    },
    goHome() {
      this.$router.push('/')
    },
  },
}
</script>

<style scoped>
.error-page {
  min-height: 70vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-bg);
  position: relative;
  overflow: hidden;
  padding: var(--spacing-xl);
}

.error-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.error-glow {
  position: absolute;
  border-radius: 50%;
  filter: blur(60px);
  opacity: 0.1;
  animation: float 6s ease-in-out infinite;
}

.error-glow-1 {
  width: 300px;
  height: 300px;
  background: var(--color-primary);
  top: 10%;
  left: 10%;
  animation-delay: 0s;
}

.error-glow-2 {
  width: 200px;
  height: 200px;
  background: var(--color-secondary);
  top: 60%;
  right: 10%;
  animation-delay: 2s;
}

.error-glow-3 {
  width: 150px;
  height: 150px;
  background: var(--color-accent);
  bottom: 20%;
  left: 20%;
  animation-delay: 4s;
}

.error-container {
  max-width: 600px;
  width: 100%;
  text-align: center;
  position: relative;
  z-index: 1;
}

.error-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-2xl);
}

.error-header {
  margin-bottom: var(--spacing-lg);
}

.error-number {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-xl);
}

.number-digit {
  font-size: 8rem;
  font-weight: var(--font-weight-bold);
  background: var(--color-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: var(--shadow-lg);
  line-height: 1;
}

.error-orb {
  width: 140px;
  height: 140px;
  background: var(--color-bg-subtle);
  border-radius: var(--border-radius-full);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow:
    var(--shadow-xl),
    inset 0 2px 4px rgba(255, 255, 255, 0.1);
  border: 1px solid var(--color-border);
  position: relative;
  overflow: hidden;
}

.error-orb::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: rgba(255, 255, 255, 0.3);
}

.face {
  color: var(--color-primary);
  filter: drop-shadow(0 4px 8px rgba(59, 130, 246, 0.3));
}

.error-text {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.error-title {
  font-size: 2.5rem;
  font-weight: var(--font-weight-bold);
  color: var(--color-text);
  margin: 0;
  line-height: 1.2;
  background: var(--color-text);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.error-description {
  font-size: 1.25rem;
  color: var(--color-text-muted);
  margin: 0;
  line-height: 1.6;
  max-width: 400px;
}

.error-actions {
  display: flex;
  gap: var(--spacing-md);
  flex-wrap: wrap;
  justify-content: center;
}

.btn {
  padding: var(--spacing-md) var(--spacing-xl);
  border-radius: var(--border-radius-xl);
  font-weight: var(--font-weight-medium);
  font-size: 1rem;
  text-decoration: none;
  border: 2px solid transparent;
  cursor: pointer;
  transition: all var(--transition-normal);
  display: inline-flex;
  align-items: center;
  gap: var(--spacing-sm);
  position: relative;
  overflow: hidden;
}

.btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.2);
  transition: left var(--transition-slow);
}

.btn:hover::before {
  left: 100%;
}

.btn-primary {
  background: var(--color-primary);
  color: var(--color-text-inverted);
  border: none;
  box-shadow: var(--shadow-lg);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-xl);
}

.btn-ghost {
  background: transparent;
  color: var(--color-text);
  border: 2px solid var(--color-border);
  backdrop-filter: var(--backdrop-blur);
}

.btn-ghost:hover {
  background: var(--color-bg-muted);
  border-color: var(--color-border-hover);
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.btn-icon {
  font-size: 1.2em;
}

.error-suggestions {
  background: var(--color-bg-subtle);
  padding: var(--spacing-xl);
  border-radius: var(--border-radius-xl);
  border: 1px solid var(--color-border);
  backdrop-filter: var(--backdrop-blur);
  box-shadow: var(--shadow-md);
  max-width: 400px;
}

.suggestions-title {
  font-size: 1rem;
  font-weight: var(--font-weight-semibold);
  color: var(--color-text);
  margin: 0 0 var(--spacing-md) 0;
}

.suggestions-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.suggestion-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  font-size: 0.9rem;
  color: var(--color-text-muted);
  padding: var(--spacing-sm);
  border-radius: var(--border-radius-md);
  transition: all var(--transition-fast);
}

.suggestion-item:hover {
  background: var(--color-bg-muted);
  color: var(--color-text);
}

.suggestion-icon {
  font-size: 1.1em;
}

/* Animations */
@keyframes float {
  0%,
  100% {
    transform: translateY(0px) scale(1);
  }
  50% {
    transform: translateY(-20px) scale(1.05);
  }
}

.face__eyes,
.face__eye-lid,
.face__mouth-left,
.face__mouth-right,
.face__nose,
.face__pupil {
  animation: eyes 1s 0.3s cubic-bezier(0.65, 0, 0.35, 1) forwards;
}

.face__eye-lid,
.face__pupil {
  animation-duration: 4s;
  animation-delay: 1.3s;
  animation-iteration-count: infinite;
}

.face__eye-lid {
  animation-name: eye-lid;
}

.face__mouth-left,
.face__mouth-right {
  animation-timing-function: cubic-bezier(0.33, 1, 0.68, 1);
}

.face__mouth-left {
  animation-name: mouth-left;
}

.face__mouth-right {
  animation-name: mouth-right;
}

.face__nose {
  animation-name: nose;
}

.face__pupil {
  animation-name: pupil;
}

/* Keyframes */
@keyframes eye-lid {
  from,
  40%,
  45%,
  to {
    transform: translateY(0);
  }
  42.5% {
    transform: translateY(17.5px);
  }
}

@keyframes eyes {
  from {
    transform: translateY(112.5px);
  }
  to {
    transform: translateY(15px);
  }
}

@keyframes pupil {
  from,
  37.5%,
  40%,
  45%,
  87.5%,
  to {
    stroke-dashoffset: 0;
    transform: translate(0, 0);
  }
  12.5%,
  25%,
  62.5%,
  75% {
    stroke-dashoffset: 0;
    transform: translate(-35px, 0);
  }
  42.5% {
    stroke-dashoffset: 35;
    transform: translate(0, 17.5px);
  }
}

@keyframes mouth-left {
  from,
  50% {
    stroke-dashoffset: -102;
  }
  to {
    stroke-dashoffset: 0;
  }
}

@keyframes mouth-right {
  from,
  50% {
    stroke-dashoffset: 102;
  }
  to {
    stroke-dashoffset: 0;
  }
}

@keyframes nose {
  from {
    transform: translate(0, 0);
  }
  to {
    transform: translate(0, 22.5px);
  }
}

/* Responsive */
@media (max-width: 768px) {
  .error-number {
    gap: var(--spacing-sm);
  }

  .number-digit {
    font-size: 6rem;
  }

  .error-orb {
    width: 120px;
    height: 120px;
  }

  .error-title {
    font-size: 2rem;
  }

  .error-description {
    font-size: 1.125rem;
  }

  .error-actions {
    flex-direction: column;
    align-items: center;
  }

  .btn {
    width: 220px;
    justify-content: center;
  }

  .face {
    width: 100px;
    height: 118px;
  }
}

@media (max-width: 480px) {
  .error-page {
    padding: var(--spacing-md);
  }

  .number-digit {
    font-size: 4rem;
  }

  .error-orb {
    width: 100px;
    height: 100px;
  }

  .error-title {
    font-size: 1.75rem;
  }

  .error-description {
    font-size: 1rem;
  }

  .error-suggestions {
    padding: var(--spacing-lg);
  }

  .face {
    width: 80px;
    height: 95px;
  }
}

/* Dark theme enhancements */
[data-theme='dark'] .error-orb {
  background: var(--color-bg-elevated);
  box-shadow:
    var(--shadow-xl),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
}

[data-theme='dark'] .error-suggestions {
  background: var(--color-bg-elevated);
  border-color: var(--color-border);
}

[data-theme='dark'] .btn-ghost:hover {
  background: var(--color-bg-muted);
}
</style>
