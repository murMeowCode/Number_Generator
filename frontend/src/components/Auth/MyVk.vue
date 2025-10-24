<template>
  <div class="vk-auth-simple">
    <button @click="openVKAuth" class="vk-auth-button">
      <img src="https://vk.com/images/icons/favicons/fav_logo.ico" alt="VK" class="vk-icon" />
      Войти через VK ID
    </button>
  </div>
</template>

<script setup>
import { useApiGet } from '@/utils/api/useApiGet'
import axios from 'axios'
import { ref, computed } from 'vue'

const emit = defineEmits(['success', 'error'])

const redirectUrl = computed(() => {
  // Для разработки используем localhost, для продакшена - ваш домен
  return 'http://codedepartament.ru/api/auth/auth/vk'
})
const openVKAuth = async () => {
  try {
    // Сохраняем state в localStorage для проверки после редиректа
    const response = await axios.get(redirectUrl.value)
    console.log(response.data)
    // Открываем в новом окне
    const width = 500
    const height = 600
    const left = (screen.width - width) / 2
    const top = (screen.height - height) / 2

    const authWindow = window.open(
      url.toString(),
      'vk_auth',
      `width=${width},height=${height},left=${left},top=${top},scrollbars=yes`,
    )

    if (!authWindow) {
      alert('Пожалуйста, разрешите всплывающие окна для этого сайта')
      return
    }

    // Слушаем сообщения от popup окна (если нужно)
    const messageHandler = (event) => {
      if (event.data?.type === 'vk_auth_success') {
        emit('success', event.data.payload)
        window.removeEventListener('message', messageHandler)
      }
    }

    window.addEventListener('message', messageHandler)

    // Проверяем закрытие окна каждую секунду
    const checkInterval = setInterval(() => {
      if (authWindow.closed) {
        clearInterval(checkInterval)
        window.removeEventListener('message', messageHandler)
        console.log('VK auth window closed')
      }
    }, 1000)
  } catch (error) {
    console.error('Error opening VK auth:', error)
    emit('error', error)
  }
}
</script>

<style scoped>
.vk-auth-simple {
  display: flex;
  justify-content: center;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.vk-auth-button {
  display: flex;
  align-items: center;
  gap: 12px;
  background: #0077ff;
  color: white;
  border: none;
  padding: 14px 28px;
  border-radius: 12px;
  cursor: pointer;
  font-size: 16px;
  font-weight: 500;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(0, 119, 255, 0.3);
}

.vk-auth-button:hover {
  background: #0055cc;
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0, 119, 255, 0.4);
}

.vk-auth-button:active {
  transform: translateY(0);
}

.vk-icon {
  width: 24px;
  height: 24px;
}

.debug-info {
  background: var(--color-bg-muted);
  border: 1px solid var(--color-border);
  border-radius: 8px;
  padding: 1rem;
  margin-top: 1rem;
  max-width: 400px;
  width: 100%;
}

.debug-info p {
  margin: 0.5rem 0;
  font-size: 14px;
  word-break: break-all;
}

.debug-button {
  background: var(--color-primary);
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 12px;
  margin-top: 0.5rem;
}

.debug-button:hover {
  background: var(--color-primary-hover);
}
</style>
