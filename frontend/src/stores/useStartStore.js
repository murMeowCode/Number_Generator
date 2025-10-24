import { defineStore } from 'pinia'

export const useStarStore = defineStore('useStarStore', {
  state: () => ({
    componentsData: [
      {
        title: 'Технологии будущего',
        description: 'Инновационные решения для современного мира',
        features: ['AI интеграция', 'Облачные вычисления', 'Безопасность', 'Масштабируемость'],
      },
      {
        title: 'Дизайн система',
        description: 'Единый подход к созданию интерфейсов',
        features: ['Компонентный подход', 'Темы оформления', 'Адаптивность', 'Документация'],
      },
      {
        title: 'Разработка ПО',
        description: 'Профессиональная разработка программного обеспечения',
        features: ['Agile методология', 'Code review', 'Тестирование', 'Деплоймент'],
      },
      {
        title: 'Аналитика данных',
        description: 'Глубокий анализ и визуализация информации',
        features: ['Big Data', 'ML алгоритмы', 'Дашборды', 'Отчетность'],
      },
      {
        title: 'Мобильные решения',
        description: 'Кроссплатформенные мобильные приложения',
        features: ['iOS & Android', 'Оффлайн режим', 'Push уведомления', 'Нативный UX'],
      },
    ],
  }),

  getters: {
    getComponentsData: (state) => {
      return state.componentsData
    },

    getComponentById: (state) => {
      return (id) => state.componentsData.find((component) => component.id === id)
    },

    getComponentsCount: (state) => {
      return state.componentsData.length
    },
  },

  actions: {
    addComponent(componentData) {
      this.componentsData.push(componentData)
    },

    updateComponent(id, updatedData) {
      const index = this.componentsData.findIndex((component) => component.id === id)
      if (index !== -1) {
        this.componentsData[index] = { ...this.componentsData[index], ...updatedData }
      }
    },

    removeComponent(id) {
      this.componentsData = this.componentsData.filter((component) => component.id !== id)
    },

    setComponentsData(newData) {
      this.componentsData = newData
    },
  },
})
