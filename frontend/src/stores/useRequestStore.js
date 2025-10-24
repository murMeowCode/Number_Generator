import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useRequestsStore = defineStore('requests', () => {
  const requests = ref(null)
  function setRequests(newR) {
    requests.value = newR
    console.log(requests.value, 'USERVALUE')
  }
  function removeRequests(newR) {
    requests.value = null
    console.log(requests.value, 'NULLLLLLLLLLLLLLLL')
  }
  const getRequests = computed(() => requests.value)

  return {
    setRequests,
    removeRequests,
    getRequests,
  }
})
