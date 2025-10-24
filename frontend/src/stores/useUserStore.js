import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', () => {
  const userData = localStorage.getItem('user')
  const user = ref(null)

  const isauth = ref(false)
  try {
    if (userData) {
      user.value = JSON.parse(userData) // Только если данные есть
      isauth.value = true
    }
  } catch (e) {
    localStorage.removeItem('user') // Очищаем битые данные
    isauth.value = false
  }
  function setUser(newUser) {
    if (!user.value) {
      // Если пользователя нет, просто устанавливаем новые данные
      user.value = newUser
    } else {
      // Если пользователь есть, объединяем данные
      user.value = {
        ...user.value,
        ...newUser,
      }
    }
    isauth.value = true
    localStorage.setItem('user', JSON.stringify(user.value))
    console.log(user.value, 'USERVALUE')
    console.log(isauth.value, 'erty')
  }
  function removeUser() {
    user.value = null
    isauth.value = false
    localStorage.removeItem('user')

    console.log('Пользователь удален, хранилище очищено')
  }
  function updateUser(updatedFields) {
    console.log('update')
    if (user.value && typeof updatedFields === 'object') {
      console.log('update1')
      user.value = { ...user.value, ...updatedFields }
      localStorage.setItem('user', JSON.stringify(user.value))
    }
  }
  const getUser = computed(() => user.value)
  const getAuth = computed(() => isauth.value)
  return {
    setUser,
    getUser,
    removeUser,
    updateUser,
    getAuth,
  }
})
