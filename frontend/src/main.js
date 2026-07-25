import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios'
import './style.css'

const API_BASE = 'http://127.0.0.1:5000/api'
const AUTH_ENDPOINTS = ['/login', '/register', '/refresh', '/forgot-password', '/reset-password']

function isAuthEndpoint(url = '') {
  return AUTH_ENDPOINTS.some(path => url.includes(path))
}

function logoutAndRedirect() {
  localStorage.removeItem('token')
  localStorage.removeItem('refresh_token')
  localStorage.removeItem('user')
  router.push('/login')
}

let refreshPromise = null

axios.interceptors.response.use(
  response => response,
  async (error) => {
    const originalRequest = error.config

    const shouldAttemptRefresh =
      error.response?.status === 401 &&
      originalRequest &&
      !originalRequest._retry &&
      !isAuthEndpoint(originalRequest.url || '')

    if (!shouldAttemptRefresh) {
      return Promise.reject(error)
    }

    const refreshToken = localStorage.getItem('refresh_token')
    if (!refreshToken) {
      logoutAndRedirect()
      return Promise.reject(error)
    }

    originalRequest._retry = true

    try {
      if (!refreshPromise) {
        refreshPromise = axios
          .post(`${API_BASE}/refresh`, {}, {
            headers: { Authorization: `Bearer ${refreshToken}` }
          })
          .finally(() => { refreshPromise = null })
      }

      const { data } = await refreshPromise
      localStorage.setItem('token', data.access_token)

      originalRequest.headers = originalRequest.headers || {}
      originalRequest.headers.Authorization = `Bearer ${data.access_token}`
      return axios(originalRequest)
    } catch (refreshError) {
      logoutAndRedirect()
      return Promise.reject(refreshError)
    }
  }
)

const app = createApp(App)

app.use(router)

app.mount('#app')
