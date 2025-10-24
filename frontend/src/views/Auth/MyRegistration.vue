<template>
  <div class="register-container" data-aos="flip-right">
    <div class="register-card">
      <!-- Заголовок -->
      <div class="register-header">
        <div class="logo-wrapper">
          <i class="pi pi-user-plus"></i>
        </div>
        <h1 class="register-title">Регистрация</h1>
        <p class="register-subtitle">Заполните форму для регистрации</p>
      </div>

      <!-- Форма регистрации -->
      <form @submit.prevent="handleSubmit" class="register-form">
        <!-- ФИО - в одной строке -->
        <div class="form-row form-row--three">
          <div class="form-group floating-group">
            <div class="input-container">
              <input
                id="surname"
                v-model="form.surname"
                type="text"
                class="form-input floating-input"
                :class="{
                  'form-input--error': errors.surname,
                  'form-input--filled': form.surname,
                }"
                placeholder=" "
                required
              />
              <label for="surname" class="floating-label">
                <i class="pi pi-id-card"></i>
                Фамилия
              </label>
              <div class="input-decoration"></div>
            </div>
            <span v-if="errors.surname" class="form-error">
              <i class="pi pi-exclamation-circle"></i>
              {{ errors.surname }}
            </span>
          </div>

          <div class="form-group floating-group">
            <div class="input-container">
              <input
                id="name"
                v-model="form.name"
                type="text"
                class="form-input floating-input"
                :class="{
                  'form-input--error': errors.name,
                  'form-input--filled': form.name,
                }"
                placeholder=" "
                required
              />
              <label for="name" class="floating-label">
                <i class="pi pi-user"></i>
                Имя
              </label>
              <div class="input-decoration"></div>
            </div>
            <span v-if="errors.fathername" class="form-error">
              <i class="pi pi-exclamation-circle"></i>
              {{ errors.name }}
            </span>
          </div>

          <div class="form-group floating-group">
            <div class="input-container">
              <input
                id="fathername"
                v-model="form.fathername"
                type="text"
                class="form-input floating-input"
                :class="{
                  'form-input--error': errors.fathername,
                  'form-input--filled': form.fathername,
                }"
                placeholder=" "
              />
              <label for="fathername" class="floating-label">
                <i class="pi pi-users"></i>
                Отчество
              </label>
              <div class="input-decoration"></div>
            </div>
            <span v-if="errors.fathername" class="form-error">
              <i class="pi pi-exclamation-circle"></i>
              {{ errors.fathername }}
            </span>
          </div>
        </div>

        <!-- Основные поля -->
        <div class="form-group floating-group">
          <div class="input-container">
            <input
              id="username"
              v-model="form.username"
              type="text"
              class="form-input floating-input"
              :class="{
                'form-input--error': errors.username,
                'form-input--filled': form.username,
              }"
              placeholder=" "
              required
            />
            <label for="username" class="floating-label">
              <i class="pi pi-at"></i>
              Логин
            </label>
            <div class="input-decoration"></div>
          </div>
          <span v-if="errors.username" class="form-error">
            <i class="pi pi-exclamation-circle"></i>
            {{ errors.username }}
          </span>
        </div>

        <div class="form-group floating-group">
          <div class="input-container">
            <input
              id="email"
              v-model="form.email"
              type="email"
              class="form-input floating-input"
              :class="{
                'form-input--error': errors.email,
                'form-input--filled': form.email,
              }"
              placeholder=" "
              required
            />
            <label for="email" class="floating-label">
              <i class="pi pi-envelope"></i>
              Email
            </label>
            <div class="input-decoration"></div>
          </div>
          <span v-if="errors.email" class="form-error">
            <i class="pi pi-exclamation-circle"></i>
            {{ errors.email }}
          </span>
        </div>

        <div class="form-group floating-group">
          <div class="input-container">
            <input
              id="birth_date"
              v-model="form.birth_date"
              type="date"
              class="form-input floating-input"
              :class="{
                'form-input--error': errors.birth_date,
                'form-input--filled': form.birth_date,
              }"
              placeholder=" "
              required
            />
            <label for="birth_date" class="floating-label">
              <i class="pi pi-calendar"></i>
              Дата рождения
            </label>
            <div class="input-decoration"></div>
          </div>
          <span v-if="errors.birth_date" class="form-error">
            <i class="pi pi-exclamation-circle"></i>
            {{ errors.birth_date }}
          </span>
        </div>
        <div class="form-row form-row--two">
          <div class="form-group floating-group">
            <div class="input-container">
              <input
                id="password"
                v-model="form.password"
                :type="showPassword ? 'text' : 'password'"
                class="form-input floating-input"
                :class="{
                  'form-input--error': errors.password,
                  'form-input--filled': form.password,
                }"
                placeholder=" "
                required
              />
              <label for="password" class="floating-label">
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

          <div class="form-group floating-group">
            <div class="input-container">
              <input
                id="confirmPassword"
                v-model="form.confirmPassword"
                :type="showConfirmPassword ? 'text' : 'password'"
                class="form-input floating-input"
                :class="{
                  'form-input--error': errors.confirmPassword,
                  'form-input--filled': form.confirmPassword,
                }"
                placeholder=" "
                required
              />
              <label for="confirmPassword" class="floating-label">
                <i class="pi pi-shield"></i>
                Подтверждение
              </label>
              <div class="input-decoration"></div>

              <button
                type="button"
                class="password-toggle beauty-toggle"
                @click="showConfirmPassword = !showConfirmPassword"
                :aria-label="showConfirmPassword ? 'Скрыть пароль' : 'Показать пароль'"
              >
                <i :class="showConfirmPassword ? 'pi pi-eye-slash' : 'pi pi-eye'"></i>
              </button>
            </div>
            <span v-if="errors.confirmPassword" class="form-error">
              <i class="pi pi-exclamation-circle"></i>
              {{ errors.confirmPassword }}
            </span>
          </div>
        </div>

        <!-- Кнопка отправки -->
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
            <i class="pi pi-user-plus"></i>
            Создать аккаунт
          </span>
          <div v-else class="loading-spinner">
            <div class="spinner-circle"></div>
            <span>Регистрируем...</span>
          </div>
        </button>

        <!-- Ссылка на вход -->
        <div class="login-link beauty-login">
          <span class="login-text">Уже есть аккаунт?</span>
          <RouterLink :to="{ name: 'login' }" class="login-action beauty-link">
            <i class="pi pi-sign-in"></i>
            Войти в систему
          </RouterLink>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { useUserStore } from '@/stores/useUserStore'
import { ref, reactive, computed } from 'vue'
import { RouterLink } from 'vue-router'
import { useRouter } from 'vue-router'
import { useValidation } from '@/utils/useValidation'
import { useNotificationsStore } from '@/stores/useToastStore'
import { useAuthStore } from '@/stores/useAuthStore'
const toast = useNotificationsStore()
const useAuth = useAuthStore()
// Список ролей
const roles = [
  {
    value: 1,
    title: 'Роль 1',
    description: 'Базовый доступ',
  },
  {
    value: 2,
    title: 'Роль 2',
    description: 'Расширенный доступ',
  },
  {
    value: 3,
    title: 'Роль 3',
    description: 'Полный доступ',
  },
]
const { errors, formSubmitted, validateForm } = useValidation()
const router = useRouter()
// Состояние формы
const form = reactive({
  name: '',
  surname: '',
  fathername: '',
  username: '',
  email: '',
  birth_date: '',
  password: '',
  confirmPassword: '',
})

// Состояние UI
const showPassword = ref(false)
const showConfirmPassword = ref(false)
const isSubmitting = ref(false)

const useUser = useUserStore()

// Валидация формы

// Обработчик отправки формы
const handleSubmit = async () => {
  if (!validateForm(form)) {
    return
  }

  isSubmitting.value = true

  try {
    // Имитация API запроса

    // await new Promise((resolve) => setTimeout(resolve, 2000))
    // await useAuth.legacyLogin(form)
    await useAuth.register(form)

    toast.success('Вы успешно зарегестрировались')

    router.push({ name: 'login' })
    formSubmitted.value = false
  } catch (error) {
    console.error('Ошибка регистрации:', error)
    if (error.Errors === 'User with this username already exists') {
      toast.error('Пользователь с таким логином уже существует')
    }
    if (error.Errors === 'User with this email already exists') {
      toast.error('Пользователь с такой почтой уже существует')
    } else {
      toast.error('Ошибка регистрации, попробуйте позже')
    }
  } finally {
    isSubmitting.value = false
  }
}
</script>

<style scoped>
.register-container {
  min-height: 80vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
  background: var(--color-bg-muted);
}

.register-card {
  background: var(--color-bg-elevated);
  border-radius: 16px;
  box-shadow:
    0 8px 32px rgba(0, 0, 0, 0.1),
    0 0 0 1px rgba(255, 255, 255, 0.1);
  padding: 2rem;
  width: 100%;
  max-width: 800px;
  backdrop-filter: blur(10px);
  position: relative;
  overflow: hidden;
}

.register-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: var(--color-primary);
}

.register-header {
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

.register-title {
  font-size: 2.5rem;
  font-weight: 600;
  color: var(--color-text);
  margin: 0 0 0.5rem;
  background: var(--color-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.register-subtitle {
  color: var(--color-text-muted);
  margin: 0;
  font-size: 1.1rem;
  font-weight: 400;
}

.register-form {
  display: flex;
  flex-direction: column;
  gap: 0.7rem;
}

/* Form Layout */
.form-row--three {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 0.5rem;
}

.form-row--two {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.5rem;
}

.form-group {
  position: relative;
}

/* Floating Label Styles */
.floating-group {
  position: relative;
}

.input-container {
  position: relative;
}

.form-input {
  padding: 1.5rem 0.75rem 0.5rem 0.75rem;
  border: 1.5px solid var(--color-border);
  border-radius: 8px;
  background: var(--color-bg);
  color: var(--color-text);
  font-size: 0.8rem;
  transition: all 0.2s ease;
  outline: none;
  width: 100%;
  height: 40px;
  box-sizing: border-box;
}

.form-input:focus {
  border-color: var(--color-primary);
  background: var(--color-bg-elevated);
  box-shadow: 0 0 0 3px var(--color-primary-soft);
}

.form-input--filled {
  border-color: var(--color-primary-muted);
}

.form-input--error {
  border-color: var(--color-error);
  background: var(--color-error-soft);
}

/* Плавающая метка */
.floating-label {
  position: absolute;
  top: 50%;
  left: 0.75rem;
  transform: translateY(-50%);
  color: var(--color-text-muted);
  font-size: 0.8rem;
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

.form-input:focus + .floating-label,
.form-input--filled + .floating-label {
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

.form-input:focus ~ .input-decoration {
  transform: scaleX(1);
}

/* Стили для выбора роли */
.roles-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--color-text);
  font-size: 0.875rem;
  font-weight: 500;
  margin-bottom: 0.75rem;
}

.roles-label i {
  font-size: 0.8rem;
  opacity: 0.7;
}

.roles-container {
  display: flex;
  flex-direction: row;
  width: 100%;
  justify-content: space-between;
  gap: 0.5rem;
}

.role-checkbox-wrapper {
  position: relative;
  width: 100%;
}

.role-checkbox-input {
  position: absolute;
  opacity: 0;
  pointer-events: none;
}

.role-checkbox-label {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  padding: 1rem;
  border: 1.5px solid var(--color-border);
  border-radius: 8px;
  background: var(--color-bg);
  color: var(--color-text);
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.role-checkbox-label:hover {
  border-color: var(--color-primary-muted);
  background: var(--color-bg-elevated);
  transform: translateY(-1px);
}

.role-checkbox-label--selected {
  border-color: var(--color-primary);
  background: var(--color-bg-elevated);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.role-checkbox-label--selected::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: var(--color-primary);
}

.role-checkbox-decoration {
  width: 20px;
  height: 20px;
  border: 1.5px solid var(--color-border);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  background: var(--color-bg);
  flex-shrink: 0;
  margin-top: 0.1rem;
}

.role-checkbox-label--selected .role-checkbox-decoration {
  background: var(--color-primary);
  border-color: var(--color-primary);
  color: white;
}

.role-checkbox-label--selected .role-checkbox-decoration i {
  transform: scale(1);
}

.role-checkbox-decoration i {
  font-size: 0.7rem;
  transform: scale(0);
  transition: transform 0.3s ease;
}

.role-content {
  flex: 1;
}

.role-title {
  font-weight: 600;
  font-size: 0.9rem;
  color: var(--color-text);
  margin-bottom: 0.25rem;
}

.role-checkbox-label--selected .role-title {
  color: var(--color-primary);
}

.role-description {
  font-size: 0.8rem;
  color: var(--color-text-muted);
  line-height: 1.3;
}

/* Анимация при выборе */
.role-checkbox-label {
  animation: fadeInUp 0.3s ease;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(5px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
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

/* Checkbox Styles */
.form-options {
  margin: 1rem 0;
}

.beauty-checkbox {
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
}

.checkbox-input {
  display: none;
}

.checkbox-label {
  display: flex;
  align-items: flex-start;
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
  flex-shrink: 0;
  margin-top: 0.1rem;
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
  line-height: 1.3;
}

/* Button Styles */
.beauty-button {
  background: var(--color-primary);
  color: var(--color-bg-elevated);
  border: none;
  border-radius: 8px;
  padding: 0.75rem 1.5rem;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  height: 44px;
  margin-top: 0.5rem;
  position: relative;
  overflow: hidden;
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

/* Links */
.beauty-link {
  color: var(--color-primary);
  text-decoration: none;
  font-weight: 500;
  transition: all 0.2s ease;
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.8rem;
}

.beauty-link:hover {
  color: var(--color-primary-hover);
}

.beauty-link i {
  font-size: 0.7rem;
}

/* Login Link */
.beauty-login {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 1rem 0 0;
  border-top: 1px solid var(--color-border);
  margin-top: 1rem;
}

.login-text {
  color: var(--color-text-muted);
  font-size: 0.8rem;
}

.login-action {
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
  .register-container {
    padding: 0.5rem;
  }

  .register-card {
    padding: 1.5rem;
    margin: 0.5rem;
  }

  .register-title {
    font-size: 1.25rem;
  }

  .form-row--three,
  .form-row--two {
    grid-template-columns: 1fr;
    gap: 0.5rem;
  }

  .beauty-login {
    flex-direction: column;
    gap: 0.25rem;
    text-align: center;
  }

  .floating-input {
    height: 42px;
    font-size: 0.85rem;
  }

  .beauty-button {
    height: 42px;
    font-size: 0.85rem;
  }

  .roles-container {
    gap: 0.375rem;
  }

  .role-checkbox-label {
    padding: 0.75rem;
  }

  .role-title {
    font-size: 0.85rem;
  }

  .role-description {
    font-size: 0.75rem;
  }
}

@media (max-width: 480px) {
  .register-card {
    padding: 1rem;
    border-radius: 12px;
  }

  .register-title {
    font-size: 1.1rem;
  }

  .register-subtitle {
    font-size: 0.8rem;
  }

  .register-form {
    gap: 1rem;
  }

  .role-checkbox-label {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }

  .role-checkbox-decoration {
    align-self: flex-start;
  }
}

input[type='date']:invalid::-webkit-datetime-edit {
  color: transparent;
}

input[type='date']:focus::-webkit-datetime-edit,
input[type='date']:valid::-webkit-datetime-edit {
  color: var(--color-text);
}

/* Для Firefox */
input[type='date']:invalid {
  color: transparent;
}

input[type='date']:focus,
input[type='date']:valid {
  color: var(--color-text);
}
</style>
