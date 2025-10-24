import { reactive } from 'vue'
export function useValidation() {
  const errors = reactive({
    name: '',
    surname: '',
    fathername: '',
    username: '',
    email: '',
    birth_date: '',
    password: '',
    confirmPassword: '',
  })
  const formSubmitted = reactive({ value: false })

  const validateForm = (form) => {
    formSubmitted.value = true
    let isValid = true

    // Очистка предыдущих ошибок
    Object.keys(errors).forEach((key) => {
      errors[key] = ''
    })
    if (!form.birth_date) {
      errors.birth_date = 'Дата рождения обязательна'
      isValid = false
    } else {
      const birth_date = new Date(form.birth_date)
      const today = new Date()
      const minDate = new Date()
      minDate.setFullYear(today.getFullYear() - 100)

      if (birth_date > today) {
        errors.birth_date = 'Дата рождения не может быть в будущем'
        isValid = false
      } else if (birth_date < minDate) {
        errors.birth_date = 'Проверьте корректность даты рождения'
        isValid = false
      }
    }

    // Валидация ФИО
    if (!form.surname?.trim()) {
      errors.surname = 'Фамилия обязательна'
      isValid = false
    }

    if (!form.name?.trim()) {
      errors.name = 'Имя обязательно'
      isValid = false
    }
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (!form.email?.trim()) {
      errors.email = 'Email обязателен'
      isValid = false
    } else if (!emailRegex.test(form.email)) {
      errors.email = 'Введите корректный email'
      isValid = false
    }
    // Валидация логина
    if (!form.username?.trim()) {
      errors.username = 'Логин обязателен'
      isValid = false
    } else if (form.username.length < 3) {
      errors.username = 'Логин должен содержать минимум 3 символа'
      isValid = false
    }

    // Валидация пароля
    if (!form.password) {
      errors.password = 'Пароль обязателен'
      isValid = false
    } else if (form.password.length < 8) {
      errors.password = 'Пароль должен содержать минимум 8 символов'
      isValid = false
    }

    // Подтверждение пароля
    if (!form.confirmPassword) {
      errors.confirmPassword = 'Подтвердите пароль'
      isValid = false
    } else if (form.password !== form.confirmPassword) {
      errors.confirmPassword = 'Пароли не совпадают'
      isValid = false
    }

    return isValid
  }

  return {
    errors,
    formSubmitted,
    validateForm,
  }
}
