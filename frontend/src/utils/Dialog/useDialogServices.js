// composables/useDialogServices.js
import DialogUpdateProfileEmailPhone from '@/components/DialogComponents/DialogUpdateProfileEmailPhone.vue'
import { useDialog } from 'primevue/usedialog'

export const useDialogServices = () => {
  const dialog = useDialog()

  function showUpdateEmailPhone(onSuccess = null) {
    // Открываем диалог и получаем его экземпляр
    const dialogInstance = dialog.open(DialogUpdateProfileEmailPhone, {
      props: {
        header: 'Изменение данных',
        style: {
          width: '40vw',
          backgroundColor: 'var(--color-bg)',
          border: 'none',
          color: 'var(--color-text)',
        },
        breakpoints: {
          '960px': '75vw',
          '640px': '80vw',
        },
        modal: true,
        draggable: false,
        closable: true,
      },
      // Передаем колбэки через props
      emits: {
        onAddData: (formData) => {
          console.log('Данные получены из диалога:', formData)

          // Вызываем внешний колбэк
          if (onSuccess && typeof onSuccess === 'function') {
            onSuccess(formData)
          }

          // Закрываем диалог
          dialogInstance.close()
        },
        onClose: () => {
          console.log('Диалог закрыт')
          dialogInstance.close()
        },
      },
    })

    return dialogInstance
  }

  return {
    showUpdateEmailPhone,
  }
}
