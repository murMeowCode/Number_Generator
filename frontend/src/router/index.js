import MyDescription from '@/components/Descriction/MyDescription.vue'
import NotFound from '@/components/NotFound/NotFound.vue'
import ContainerSravn from '@/components/Sravn/ContainerSravn.vue'
import { useUserStore } from '@/stores/useUserStore'
import MyLogin from '@/views/Auth/MyLogin.vue'
import MyRegistration from '@/views/Auth/MyRegistration.vue'
import FileViews from '@/views/FileViews.vue'
import One from '@/views/One/One.vue'
import Three from '@/views/Three/Three.vue'
import Two from '@/views/Two/Two.vue'
import { storeToRefs } from 'pinia'
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'one',
      component: One,
    },
    {
      path: '/comparation',
      name: 'comparation',
      component: ContainerSravn,
    },
    {
      path: '/description',
      name: 'description',
      component: MyDescription,
    },
    {
      path: '/two',
      name: 'two',
      component: Two,
      beforeEnter: (to, from, next) => {
        const { getAuth } = storeToRefs(useUserStore())

        if (!getAuth.value) {
          next('/login')
        } else {
          next()
        }
      },
    },
    {
      path: '/three',
      name: 'three',
      component: Three,
       beforeEnter: (to, from, next) => {
        const { getAuth } = storeToRefs(useUserStore())

        if (!getAuth.value) {
          next('/login')
        } else {
          next()
        }
      },
    },
    {
      path: '/authentification',
      name: 'auth',
      component: MyRegistration,
    },
    {
      path: '/login',
      name: 'login',
      component: MyLogin,
    },
    {
      path: '/file',
      name: 'file',
      component: FileViews,
       beforeEnter: (to, from, next) => {
        const { getAuth } = storeToRefs(useUserStore())

        if (!getAuth.value) {
          next('/login')
        } else {
          next()
        }
      },
    },
    {
      path: '/:any(.*)',
      name: 'e404',
      component: NotFound,
    },
  ],
})

export default router
