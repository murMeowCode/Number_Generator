// src/composables/useTheme.js
import { ref, watch, onMounted } from 'vue'

const THEME_KEY = 'user-theme-preference'

export function useTheme() {
  const isDark = ref(false)

  // Применить тему к <html>
  const setTheme = (dark) => {
    isDark.value = dark
    if (dark) {
      document.documentElement.setAttribute('data-theme', 'dark')
    } else {
      document.documentElement.removeAttribute('data-theme')
    }
    localStorage.setItem(THEME_KEY, dark ? 'dark' : 'light')
  }

  // Переключить тему
  const toggleTheme = () => {
    setTheme(!isDark.value)
  }

  // Инициализация при загрузке
  onMounted(() => {
    // 1. Проверяем сохранённое значение
    const saved = localStorage.getItem(THEME_KEY)
    if (saved === 'dark') {
      setTheme(true)
      return
    }
    if (saved === 'light') {
      setTheme(false)
      return
    }

    // 2. Если нет сохранённого — используем системную тему
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
    setTheme(prefersDark)
  })

  return {
    isDark,
    toggleTheme,
  }
}
