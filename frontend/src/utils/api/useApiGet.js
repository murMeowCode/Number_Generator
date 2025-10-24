// composables/useApiGet.js
import { useQuery } from '@tanstack/vue-query'
import axios from 'axios'

export function useApiGet() {
  const useGet = (endpoint, params = {}, options = {}) => {
    const queryKey = ['api', endpoint, params, options.headers] // включаем headers в ключ

    return useQuery({
      queryKey,
      queryFn: async () => {
        const startTime = Date.now()
        console.log(`🔄 GET ${endpoint}`, { params, headers: options.headers })

        try {
          const response = await axios.get(endpoint, {
            params,
            headers: options.headers, // передаем заголовки
          })
          const duration = Date.now() - startTime

          console.log(`✅ Успех: GET ${endpoint}`, {
            duration: `${duration}ms`,
            data: response.data,
          })

          return response.data
        } catch (error) {
          const duration = Date.now() - startTime
          console.error(`❌ Ошибка: GET ${endpoint}`, {
            duration: `${duration}ms`,
            error: error.response?.data || error.message,
          })
          throw error
        }
      },
      ...options,
    })
  }

  return {
    useGet,
  }
}
