import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useAchivesStore = defineStore('achives', () => {
  const ACHIVES = [
    { text: 'Регистрация!!!', procent: 100 },
    { text: 'Пусть меня все знают', procent: 70 },
    { text: 'Участник', procent: 50 },
    { text: 'Победитель', procent: 12 },
  ]

  return { ACHIVES }
})
