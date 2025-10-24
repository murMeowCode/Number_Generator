import { defineStore } from 'pinia'
import { useToast } from 'vue-toastification'

export const useNotificationsStore = defineStore('notifications', () => {
  const toast = useToast()

  const success = (message, title = 'Успешно') => {
    toast.success(message)
  }

  const error = (message, title = 'Ошибка') => {
    toast.error(message)
  }

  const warning = (message, title = 'Внимание') => {
    toast.warning(message)
  }

  const info = (message, title = 'Информация') => {
    toast.info(message)
  }

  const api = {
    success: (message = 'Операция выполнена успешно') => success(message),
    error: (message = 'Произошла ошибка') => error(message),
  }

  return {
    success,
    error,
    warning,
    info,
    api,
  }
})
