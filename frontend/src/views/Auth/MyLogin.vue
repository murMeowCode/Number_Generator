<template>
  <div class="login-container" data-aos="flip-left">
    <div class="login-card">
      <!-- Заголовок -->
      <div class="login-header">
        <div class="logo-wrapper">
          <i class="pi pi-shield"></i>
        </div>
        <h1 class="login-title">Добро пожаловать</h1>
        <p class="login-subtitle">Войдите в свой аккаунт</p>
      </div>

      <!-- Форма входа -->
      <form @submit.prevent="handleSubmit" class="login-form">
        <!-- Поле для логина или email -->
        <div class="form-group floating-group">
          <div class="input-container">
            <input
              id="username"
              v-model="form.username"
              type="text"
              class="form-input floating-input"
              :class="{
                'form-input--error': errors.username,
              }"
              placeholder=" "
              required
              autocomplete="username"
              @focus="handleInputFocus"
              @blur="handleInputBlur"
            />
            <label
              for="username"
              class="floating-label"
              :class="{
                'floating-label--active': form.username || isFocused.username,
              }"
            >
              <i class="pi pi-user"></i>
              Логин
            </label>
            <div class="input-decoration"></div>
          </div>
          <span v-if="errors.username" class="form-error">
            <i class="pi pi-exclamation-circle"></i>
            {{ errors.username }}
          </span>
        </div>

        <!-- Поле пароля -->
        <div class="form-group floating-group">
          <div class="input-container">
            <input
              id="password"
              v-model="form.password"
              :type="showPassword ? 'text' : 'password'"
              class="form-input floating-input"
              :class="{
                'form-input--error': errors.password,
              }"
              placeholder=" "
              required
              autocomplete="current-password"
              @focus="handleInputFocus"
              @blur="handleInputBlur"
            />
            <label
              for="password"
              class="floating-label"
              :class="{
                'floating-label--active': form.password || isFocused.password,
              }"
            >
              <i class="pi pi-lock"></i>
              Пароль
            </label>
            <div class="input-decoration"></div>

            <button
              type="button"
              class="password-toggle beauty-toggle"
              @click="showPassword = !showPassword"
              :aria-label="showPassword ? 'Скрыть пароль' : 'Показать пароль'"
            >
              <i :class="showPassword ? 'pi pi-eye-slash' : 'pi pi-eye'"></i>
            </button>
          </div>

          <span v-if="errors.password" class="form-error">
            <i class="pi pi-exclamation-circle"></i>
            {{ errors.password }}
          </span>
        </div>
        <!-- Запомнить меня -->
        <div class="form-options">
          <div class="beauty-checkbox">
            <input
              id="rememberMe"
              v-model="form.rememberMe"
              type="checkbox"
              class="checkbox-input"
            />
            <label for="rememberMe" class="checkbox-label">
              <div class="checkbox-decoration">
                <i class="pi pi-check"></i>
              </div>
              <span class="checkbox-text">Запомнить меня</span>
            </label>
          </div>
        </div>

        <!-- Кнопка входа -->
        <button
          type="submit"
          class="submit-button beauty-button"
          :disabled="isSubmitting"
          :class="{
            'submit-button--loading': isSubmitting,
            'beauty-button--loading': isSubmitting,
          }"
        >
          <span v-if="!isSubmitting" class="button-content">
            <i class="pi pi-sign-in"></i>
            Войти в систему
          </span>
          <div v-else class="loading-spinner">
            <div class="spinner-circle"></div>
            <span>Выполняется вход...</span>
          </div>
        </button>
        <!-- Ссылка на регистрацию -->
        <div class="register-link beauty-register">
          <span class="register-text">Впервые у нас?</span>
          <RouterLink :to="{ name: 'auth' }" class="register-action beauty-link">
            <i class="pi pi-user-plus"></i>
            Создать аккаунт
          </RouterLink>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/useUserStore'
import { useNotificationsStore } from '@/stores/useToastStore'
import { useAuthStore } from '@/stores/useAuthStore'
import MyVk from '@/components/Auth/MyVk.vue'
const useAuth = useAuthStore()
// Состояние формы
const form = reactive({
  username: '',
  password: '',
  rememberMe: false,
})
const router = useRouter()
const useUser = useUserStore()
// Ошибки валидации
const errors = reactive({
  username: '',
  password: '',
})
const toast = useNotificationsStore()
// Состояние UI
const showPassword = ref(false)
const isSubmitting = ref(false)

// Отслеживание фокуса для каждого поля
const isFocused = reactive({
  username: false,
  password: false,
})

// Обработчики фокуса
const handleInputFocus = (event) => {
  const fieldName = event.target.id
  isFocused[fieldName] = true
}

const handleInputBlur = (event) => {
  const fieldName = event.target.id
  isFocused[fieldName] = false
}

// Валидация формы
const validateForm = () => {
  let isValid = true

  // Очистка предыдущих ошибок
  Object.keys(errors).forEach((key) => {
    errors[key] = ''
  })

  // Валидация логина/email
  if (!form.username.trim()) {
    errors.username = 'Введите логин или email'
    isValid = false
  } else if (form.username.length < 3) {
    errors.username = 'Логин должен содержать минимум 3 символа'
    isValid = false
  }

  // Валидация пароля
  if (!form.password) {
    errors.password = 'Введите пароль'
    isValid = false
  } else if (form.password.length < 6) {
    errors.password = 'Пароль должен содержать минимум 6 символов'
    isValid = false
  }

  return isValid
}

// Обработчик входа
const handleSubmit = async () => {
  if (!validateForm()) {
    return
  }

  isSubmitting.value = true

  try {
    // await new Promise((resolve) => setTimeout(resolve, 1500))
    // await useAuth.legacyLogin({ username: form.username, password: form.password })
    await useAuth.login({ username: form.username, password: form.password })

    toast.success('Вошли успешно')
    // Здесь будет реальный API вызов
    console.log('Вход выполнен:', {
      username: form.username,
      password: form.password,
    })
    router.push({ name: 'one' })
  } catch (error) {
    console.error('Ошибка входа:', error)
    toast.error('Проверьте правильность введённых данных')
    if (error.message?.includes('credentials')) {
      errors.username = 'Неверный логин или пароль'
      errors.password = 'Неверный логин или пароль'
    } else {
    }
  } finally {
    isSubmitting.value = false
  }
}

// Обработчик социального входа
const handleSocialLogin = (provider) => {
  console.log(`Социальный вход через: ${provider}`)
  alert(`Вход через ${provider} (в разработке)`)
}
</script>

<style scoped>
.login-container {
  min-height: 80vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
  background: var(--color-bg-muted);
}

.login-card {
  background: var(--color-bg-elevated);
  border-radius: 16px;
  box-shadow:
    0 8px 32px rgba(0, 0, 0, 0.1),
    0 0 0 1px rgba(255, 255, 255, 0.1);
  padding: 2rem;
  width: 100%;
  max-width: 400px;
  backdrop-filter: blur(10px);
  position: relative;
  overflow: hidden;
}

.login-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: var(--color-primary);
}

.login-header {
  text-align: center;
  margin-bottom: 2rem;
}

.logo-wrapper {
  margin-bottom: 0.75rem;
}

.logo-wrapper i {
  font-size: 2rem;
  color: var(--color-primary);
}

.login-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--color-text);
  margin: 0 0 0.5rem;
  background: var(--color-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.login-subtitle {
  color: var(--color-text-muted);
  margin: 0;
  font-size: 0.9rem;
  font-weight: 400;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

/* Floating Label Styles */
.floating-group {
  position: relative;
}

.input-container {
  position: relative;
}

.floating-input {
  padding: 1rem 0.75rem 0.5rem 0.75rem;
  border: 1.5px solid var(--color-border);
  border-radius: 8px;
  background: var(--color-bg);
  color: var(--color-text);
  font-size: 0.875rem;
  transition: all 0.2s ease;
  outline: none;
  width: 100%;
  height: 50px;
}

.floating-input:focus {
  border-color: var(--color-primary);
  background: var(--color-bg-elevated);
  box-shadow: 0 0 0 3px var(--color-primary-soft);
}

.floating-input--error {
  border-color: var(--color-error);
  background: var(--color-error-soft);
}

.floating-label {
  position: absolute;
  top: 50%;
  left: 0.75rem;
  transform: translateY(-50%);
  color: var(--color-text-muted);
  font-size: 0.875rem;
  font-weight: 400;
  pointer-events: none;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.floating-label i {
  font-size: 0.8rem;
  opacity: 0.7;
}

/* Ключевое изменение: лейбл остается сверху когда есть значение ИЛИ поле в фокусе */
.floating-input:focus + .floating-label,
.floating-label--active {
  top: 0.5rem;
  transform: none;
  font-size: 0.75rem;
  color: var(--color-primary);
  font-weight: 500;
}

.input-decoration {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: var(--color-primary);
  transform: scaleX(0);
  transition: transform 0.2s ease;
}

.floating-input:focus ~ .input-decoration {
  transform: scaleX(1);
}

.input-decoration {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: var(--color-primary);
  transform: scaleX(0);
  transition: transform 0.2s ease;
}

.floating-input:focus ~ .input-decoration {
  transform: scaleX(1);
}

/* Password Toggle */
.beauty-toggle {
  position: absolute;
  right: 0.5rem;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: var(--color-text-muted);
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 4px;
  transition: all 0.2s ease;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.beauty-toggle:hover {
  background: var(--color-primary-soft);
  color: var(--color-primary);
}

/* Password Actions */
.password-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 0.5rem;
}

.beauty-link {
  color: var(--color-primary);
  text-decoration: none;
  font-size: 0.8rem;
  font-weight: 500;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.beauty-link:hover {
  color: var(--color-primary-hover);
}

.beauty-link i {
  font-size: 0.7rem;
}

/* Checkbox Styles */
.beauty-checkbox {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.checkbox-input {
  display: none;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.checkbox-decoration {
  width: 16px;
  height: 16px;
  border: 1.5px solid var(--color-border);
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  background: var(--color-bg);
}

.checkbox-input:checked + .checkbox-label .checkbox-decoration {
  background: var(--color-primary);
  border-color: var(--color-primary);
  color: white;
}

.checkbox-input:checked + .checkbox-label .checkbox-decoration i {
  transform: scale(1);
}

.checkbox-decoration i {
  font-size: 0.7rem;
  transform: scale(0);
  transition: transform 0.2s ease;
}

.checkbox-text {
  color: var(--color-text);
  font-size: 0.8rem;
  font-weight: 400;
}

/* Button Styles */
.beauty-button {
  background: var(--color-primary);
  color: white;
  border: none;
  border-radius: 8px;
  padding: 0.75rem 1.5rem;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  height: 44px;
  margin-top: 0.5rem;
}

.beauty-button:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.beauty-button:active:not(:disabled) {
  transform: translateY(0);
}

.beauty-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.button-content {
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-bg-elevated);
  gap: 0.5rem;
}

.button-content i {
  font-size: 0.9rem;
}

/* Loading Spinner */
.loading-spinner {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.spinner-circle {
  width: 16px;
  height: 16px;
  border: 2px solid transparent;
  border-top: 2px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

/* Divider Styles */
.beauty-divider {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin: 1.25rem 0;
}

.divider-line {
  flex: 1;
  height: 1px;
  background: var(--color-border);
}

.divider-text {
  color: var(--color-text-muted);
  font-size: 0.75rem;
  font-weight: 500;
  white-space: nowrap;
}

/* Social Login Styles - ИСПРАВЛЕННЫЕ СТИЛИ */
.social-login {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  width: 100%;
}

.beauty-social {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  border: 1.5px solid var(--color-border);
  border-radius: 8px;
  background: var(--color-bg);
  color: var(--color-text);
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  width: 100%;
  height: 48px;
  box-sizing: border-box;
  text-decoration: none;
}

.beauty-social:hover {
  transform: translateY(-1px);
  border-color: var(--color-primary);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.social-icon {
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  background: var(--color-bg-elevated);
  transition: all 0.2s ease;
  flex-shrink: 0;
}

.social-button--google:hover .social-icon {
  background: #db4437;
  color: white;
}

.social-button--github:hover .social-icon {
  background: #333;
  color: white;
}

.social-text {
  font-weight: 500;
  flex: 1;
  text-align: left;
}

/* Специфичные стили для компонента MyVk */
.social-login :deep(.beauty-social) {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  border: 1.5px solid var(--color-border);
  border-radius: 8px;
  background: var(--color-bg);
  color: var(--color-text);
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  width: 100%;
  height: 48px;
  box-sizing: border-box;
  text-decoration: none;
}

.social-login :deep(.beauty-social):hover {
  transform: translateY(-1px);
  border-color: var(--color-primary);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.social-login :deep(.social-icon) {
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  background: var(--color-bg-elevated);
  transition: all 0.2s ease;
  flex-shrink: 0;
}

.social-login :deep(.beauty-social):hover .social-icon {
  background: #0077ff;
  color: white;
}

/* Register Link Styles */
.beauty-register {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 1rem 0 0;
  border-top: 1px solid var(--color-border);
  margin-top: 1rem;
}

.register-text {
  color: var(--color-text-muted);
  font-size: 0.8rem;
}

.register-action {
  font-weight: 500;
}

/* Error Styles */
.form-error {
  display: flex;
  align-items: center;
  color: var(--color-error);
  font-size: 0.7rem;
  font-weight: 400;
  margin-top: 0.25rem;
  padding: 0.25rem 0.5rem;
  background: var(--color-error-soft);
  border-radius: 4px;
  border-left: 2px solid var(--color-error);
  gap: 0.25rem;
}

.form-error i {
  font-size: 0.65rem;
}

/* Адаптивность */
@media (max-width: 768px) {
  .login-container {
    padding: 0.5rem;
  }

  .login-card {
    padding: 1.5rem;
    margin: 0.5rem;
  }

  .login-title {
    font-size: 1.25rem;
  }

  .social-login {
    gap: 0.5rem;
  }

  .beauty-social {
    height: 44px;
    padding: 0.625rem 0.75rem;
  }

  .beauty-register {
    flex-direction: column;
    gap: 0.25rem;
    text-align: center;
  }
}

@media (max-width: 480px) {
  .login-card {
    padding: 1rem;
    border-radius: 12px;
  }

  .login-title {
    font-size: 1.1rem;
  }

  .login-subtitle {
    font-size: 0.8rem;
  }

  .login-form {
    gap: 1rem;
  }

  .floating-input {
    height: 42px;
    font-size: 0.85rem;
  }

  .beauty-button {
    height: 42px;
    font-size: 0.85rem;
  }

  .beauty-social {
    height: 42px;
    font-size: 0.8rem;
  }
}
</style>
