<template>
  <header class="header">
    <div class="container">
      <!-- Логотип -->
      <div class="logo">
        <img :src="svg" alt="">
      </div>

      <!-- Правая часть: навигация + переключатель темы -->
      <div class="header-right">
        <nav class="nav">
          <!-- Для авторизованных пользователей - все пункты кроме "Войти" -->
          <template v-if="isAuthenticated">
            <RouterLink
              v-for="item in navItems"
              :key="item.route"
              :to="{ name: item.route }"
              class="nav-link"
              active-class="nav-link--active"
            >
              <i :class="item.icon" class="nav-icon"></i>
              <span class="nav-label">{{ item.label }}</span>
            </RouterLink>
            
            <!-- Кнопка выхода для авторизованных -->
            <button
              class="nav-link logout-link"
              @click="handleLogout"
              aria-label="Выйти из системы"
            >
              <i class="pi pi-sign-out nav-icon"></i>
              <span class="nav-label">Выйти</span>
            </button>
          </template>

          <!-- Для неавторизованных пользователей - только "one" и "Войти" -->
          <template v-else>
            <RouterLink
              :to="{ name: 'one' }"
              class="nav-link"
              active-class="nav-link--active"
            >
              <i class="pi pi-calendar nav-icon"></i>
              <span class="nav-label">ДЕМОНСТРАЦИЯ</span>
            </RouterLink>

            <!-- Кнопка входа для неавторизованных -->
            <RouterLink
              :to="{ name: 'login' }"
              class="nav-link login-link"
              active-class="nav-link--active"
            >
              <i class="pi pi-sign-in nav-icon"></i>
              <span class="nav-label">Войти</span>
            </RouterLink>
          </template>
        </nav>
        <ThemeToggle class="theme-toggle theme-toggle--desktop" />
      </div>

      <!-- Переключатель темы для мобильных -->
      <ThemeToggle class="theme-toggle--mobile" />

      <!-- Бургер-меню (только на мобильных) -->
      <button
        class="burger"
        @click="toggleMobileMenu"
        aria-label="Меню"
        :aria-expanded="isMobileMenuOpen"
      >
        <span class="burger-line"></span>
        <span class="burger-line"></span>
        <span class="burger-line"></span>
      </button>

      <!-- Мобильное меню -->
      <nav v-if="isMobileMenuOpen" class="nav-mobile" data-aos="flip-right">
        <!-- Для авторизованных пользователей - все пункты кроме "Войти" -->
        <template v-if="isAuthenticated">
          <RouterLink
            v-for="item in navItems"
            :key="item.route"
            :to="{ name: item.route }"
            class="nav-link"
            active-class="nav-link--active"
            @click="closeMobileMenu"
          >
            <i :class="item.icon" class="nav-icon"></i>
            <span class="nav-label">{{ item.label }}</span>
          </RouterLink>
          
          <!-- Кнопка выхода для авторизованных (мобильная версия) -->
          <button
            class="nav-link logout-link"
            @click="handleLogoutMobile"
            aria-label="Выйти из системы"
          >
            <i class="pi pi-sign-out nav-icon"></i>
            <span class="nav-label">Выйти</span>
          </button>
        </template>

        <!-- Для неавторизованных пользователей - только "one" и "Войти" -->
        <template v-else>
          <RouterLink
            :to="{ name: 'one' }"
            class="nav-link"
            active-class="nav-link--active"
            @click="closeMobileMenu"
          >
            <i class="pi pi-calendar nav-icon"></i>
            <span class="nav-label">ДЕМОНСТРАЦИЯ</span>
          </RouterLink>

          <!-- Кнопка входа для неавторизованных -->
          <RouterLink
            :to="{ name: 'login' }"
            class="nav-link login-link"
            active-class="nav-link--active"
            @click="closeMobileMenu"
          >
            <i class="pi pi-sign-in nav-icon"></i>
            <span class="nav-label">Войти</span>
          </RouterLink>
        </template>
      </nav>
    </div>
  </header>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { RouterLink } from 'vue-router'
import ThemeToggle from '../Theme/ThemeToggle.vue'
import { useUserStore } from '@/stores/useUserStore'
import { storeToRefs } from 'pinia'
import svg from '@/assets/2.png'
import { useRouter } from 'vue-router'
// Состояние авторизации
const { getAuth: isAuthenticated } = storeToRefs(useUserStore())
const useUser = useUserStore()
const router = useRouter()
// Навигационные пункты (для авторизованных пользователей)
const navItems = [
  {
    label: 'ДЕМОНСТРАЦИЯ',
    icon: 'pi pi-desktop', // Более подходящая для демонстрации
    route: 'one',
  },
  {
    label: 'ДАШБОРД',
    icon: 'pi pi-chart-bar', // Классическая для дашбордов
    route: 'two',
  },
  {
    label: 'ГЕНЕРАТОР',
    icon: 'pi pi-bolt', // Или pi pi-cog, pi pi-wrench
    route: 'three',
  },
   {
    label: 'АУДИТ',
    icon: 'pi pi-shield', // Или pi pi-check-circle, pi pi-verified
    route: 'file',
  },
  {
  label: 'СРАВНЕНИЕ',
  icon: 'pi pi-equals', // Сортировка/сравнение
  route: 'comparation',
}
]

const isMobileMenuOpen = ref(false)

const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
}

const closeMobileMenu = () => {
  isMobileMenuOpen.value = false
}

// Метод выхода (пустой - вы заполните его)
const handleLogout = () => {
  // TODO: Добавьте логику выхода
  console.log('Выход из системы')
  useUser.removeUser()
  router.push({name:'login'})
}

// Метод выхода для мобильной версии
const handleLogoutMobile = () => {
  handleLogout()
  closeMobileMenu()
}

// Закрывать меню при изменении размера окна (если стало > 768px)
const handleResize = () => {
  if (window.innerWidth >= 768) {
    isMobileMenuOpen.value = false
  }
}

// Инициализация при загрузке
onMounted(() => {
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
img{
  height: 100px;
}

/* === Контейнер шапки === */
.header {
  background: var(--color-bg-subtle);
  border-bottom: 1px solid var(--color-border);
  box-shadow: var(--shadow-sm);
  position: sticky;
  top: 0;
  z-index: 1000;
  backdrop-filter: var(--backdrop-blur);
  backdrop-saturate: var(--backdrop-saturate);
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 var(--spacing-xl);
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: relative;
}

/* === Логотип === */
.logo {
  display: flex;
  align-items: center;
  flex-shrink: 0;
}

/* === Правая часть: навигация + переключатель темы === */
.header-right {
  display: flex;
  align-items: center;
  gap: var(--spacing-xl);
  flex-grow: 1;
  justify-content: flex-end;
}

/* === Навигация === */
.nav {
  display: flex;
  gap: var(--spacing-lg);
  align-items: center;
}

.nav-link {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 110px;
  height: 75px;
  color: var(--color-text-muted);
  text-decoration: none;
  font-size: 0.85rem;
  font-weight: var(--font-weight-medium);
  transition: all var(--transition-normal);
  border-radius: var(--border-radius-lg);
  padding: var(--spacing-md);
  border: 1px solid transparent;
  text-align: center;
  line-height: 1.2;
  cursor: pointer;
}

.nav-icon {
  font-size: 1.6rem;
  margin-bottom: var(--spacing-xs);
  transition: all var(--transition-normal);
}

.nav-link:hover {
  color: var(--color-primary);
  background: var(--color-primary-soft);
  border-color: var(--color-primary-muted);
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

.nav-link:hover .nav-icon {
  transform: translateY(-3px) scale(1.15);
}

.nav-link--active {
  color: var(--color-primary);
  background: var(--color-primary-soft);
  border: 1px solid var(--color-primary-muted);
  box-shadow: var(--shadow-md);
}

.nav-link--active .nav-icon {
  transform: translateY(-3px);
  filter: drop-shadow(0 3px 6px rgba(59, 130, 246, 0.3));
}

/* Специальные стили для кнопки входа */
.login-link {
  background: var(--color-success-soft);
  border-color: var(--color-success-muted);
  color: var(--color-success);
  margin-left: var(--spacing-sm);
}

.login-link:hover {
  background: var(--color-success);
  color: white;
  border-color: var(--color-success);
  transform: translateY(-2px);
}

.login-link.nav-link--active {
  background: var(--color-success);
  color: white;
  border-color: var(--color-success);
  transform: translateY(-1px);
}

/* Специальные стили для кнопки выхода */
.logout-link {
  background: var(--color-danger-soft);
  border-color: var(--color-danger-muted);
  color: var(--color-danger);
  margin-left: var(--spacing-sm);
}

.logout-link:hover {
  background: var(--color-danger);
  color: white;
  border-color: var(--color-danger);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(239, 68, 68, 0.3);
}

.logout-link:hover .nav-icon {
  transform: translateY(-3px) scale(1.15);
  animation: shake 0.5s ease-in-out;
}

/* Анимация тряски для иконки выхода */
@keyframes shake {
  0%, 100% { transform: translateY(-3px) scale(1.15); }
  25% { transform: translateY(-3px) scale(1.15) rotate(-5deg); }
  75% { transform: translateY(-3px) scale(1.15) rotate(5deg); }
}

/* Переключатель темы */
.theme-toggle--desktop {
  margin-left: var(--spacing-lg);
}

/* === Мобильное меню === */
.nav-mobile {
  display: none;
}

/* === Переключатель темы для мобильных === */
.theme-toggle--mobile {
  display: none;
}

/* === Бургер-меню === */
.burger {
  display: none;
  flex-direction: column;
  justify-content: space-between;
  width: 32px;
  height: 24px;
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 0;
  z-index: 1001;
  transition: transform var(--transition-normal);
}

.burger:hover {
  transform: scale(1.05);
}

.burger-line {
  width: 100%;
  height: 2px;
  background: var(--color-text);
  border-radius: var(--border-radius-full);
  transition: all var(--transition-normal);
  transform-origin: center;
}

.burger[aria-expanded='true'] .burger-line:nth-child(1) {
  transform: rotate(45deg) translate(6px, 6px);
  background: var(--color-primary);
}

.burger[aria-expanded='true'] .burger-line:nth-child(2) {
  opacity: 0;
  transform: scale(0);
}

.burger[aria-expanded='true'] .burger-line:nth-child(3) {
  transform: rotate(-45deg) translate(6px, -6px);
  background: var(--color-primary);
}

/* === Адаптивность === */
@media (max-width: 1024px) {
  .container {
    max-width: 100%;
    padding: 0 var(--spacing-lg);
  }
  
  .nav-link {
    width: 100px;
    height: 70px;
    font-size: 0.8rem;
  }
  
  .nav {
    gap: var(--spacing-md);
  }
}

@media (max-width: 768px) {
  .container {
    height: 75px;
    padding: 0 var(--spacing-md);
    justify-content: space-between;
  }

  img {
    height: 80px;
  }

  /* Скрыть правую часть на мобильных */
  .header-right {
    display: none;
  }

  /* Показать переключатель темы для мобильных */
  .theme-toggle--mobile {
    display: block;
    margin-right: var(--spacing-lg);
  }

  /* Скрыть переключатель темы в десктопной версии */
  .theme-toggle--desktop {
    display: none;
  }

  /* Показать бургер */
  .burger {
    display: flex;
  }

  /* Мобильное меню */
  .nav-mobile {
    display: flex;
    position: fixed;
    top: 0;
    right: 0;
    height: 100vh;
    width: 350px;
    max-width: 85vw;
    background: var(--color-bg-elevated);
    flex-direction: column;
    padding: 90px var(--spacing-lg) var(--spacing-xl);
    gap: var(--spacing-md);
    box-shadow: var(--shadow-xl);
    border-left: 1px solid var(--color-border);
    z-index: 999;
    overflow-y: auto;
    animation: slideInRight var(--transition-normal) ease-out;
  }

  .nav-link {
    width: 85%;
    height: 65px;
    flex-direction: row;
    justify-content: flex-start;
    padding: 0 var(--spacing-xl);
    gap: var(--spacing-lg);
    font-size: 1.15rem;
    font-weight: var(--font-weight-medium);
    border-radius: var(--border-radius-lg);
    border: 1px solid var(--color-border);
    margin-bottom: var(--spacing-sm);
  }

  .nav-link:hover {
    transform: translateX(6px);
  }

  .nav-icon {
    font-size: 1.4rem;
    margin-bottom: 0;
    width: 28px;
    text-align: center;
  }

  .nav-link--active {
    background: var(--color-primary-soft);
    border-color: var(--color-primary-muted);
    color: var(--color-primary);
    transform: translateX(4px);
  }

  /* Для мобильной версии кнопка входа */
  .login-link {
    margin-left: 0;
    margin-top: var(--spacing-md);
    background: var(--color-success-soft);
    border-color: var(--color-success-muted);
  }

  .login-link.nav-link--active {
    background: var(--color-success);
    color: white;
    border-color: var(--color-success);
  }

  /* Для мобильной версии кнопка выхода */
  .logout-link {
    margin-left: 0;
    margin-top: var(--spacing-md);
    background: var(--color-danger-soft);
    border-color: var(--color-danger-muted);
  }

  .logout-link:hover {
    background: var(--color-danger);
    color: white;
    border-color: var(--color-danger);
    transform: translateX(6px);
  }
}

@media (max-width: 480px) {
  .container {
    padding: 0 var(--spacing-md);
  }

  .nav-mobile {
    width: 300px;
  }

  .nav-link {
    padding: 0 var(--spacing-lg);
    height: 60px;
    font-size: 1.1rem;
  }
}

/* Анимация для мобильного меню */
@keyframes slideInRight {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

/* Затемнение фона при открытом мобильном меню */
.nav-mobile::before {
  content: '';
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: -1;
  opacity: 0;
  animation: fadeIn var(--transition-normal) ease-out forwards;
}

@keyframes fadeIn {
  to {
    opacity: 1;
  }
}
</style>