// composables/useApiMutations.js
import { useMutation } from '@tanstack/vue-query'
import { useNotificationsStore } from '@/stores/useToastStore'

const createMutation =
  (method) =>
  (url, options = {}) => {
    const toast = useNotificationsStore()
    console.log(url, 'url')
    return useMutation({
      mutationFn: (data) => {
        return fetch(url, {
          method: method.toUpperCase(),
          headers: {
            'Content-Type': 'application/json',
            ...options.headers,
          },
          body: data ? JSON.stringify(data) : undefined,
        }).then(async (response) => {
          if (!response.ok) {
            const error = await response.text()
            throw new Error(error || `HTTP error! status: ${response.status}`)
          }
          return response.json()
        })
      },
      onSuccess: (data, variables, context) => {
        console.log(`✅ ${method.toUpperCase()} Success: ${url}`, data)
        options.onSuccess?.(data, variables, context)
      },
      onError: (error, variables, context) => {
        toast.error('Не вошли')
        console.error(`❌ ${method.toUpperCase()} Error: ${url}`, error.message)
        options.onError?.(error, variables, context)
      },
      ...options,
    })
  }

export function useApiMutations() {
  return {
    usePost: createMutation('post'),
    usePut: createMutation('put'),
    usePatch: createMutation('patch'),
    useDelete: createMutation('delete'),
  }
}
