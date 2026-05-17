import axios from 'axios'

const baseURL = "/api/v1"

export const api = axios.create({
  baseURL: baseURL,
  withCredentials: true
})

const refreshApi = axios.create({
  baseURL,
  withCredentials: true
})

const refreshTokens = async () => {
  return await refreshApi.post('/auth/refresh', {})
}

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config
    if (
      error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      try {
        await refreshTokens()
        return api(originalRequest)
      } catch (refreshError) {
        window.dispatchEvent(new Event('unauthorized'))
        return Promise.reject(refreshError)
      }
    }
    return Promise.reject(error)
  }
)

export const request = async (
  method,
  url,
  data = null,
  config = {}
) => {
  const isGet = method.toLowerCase() === 'get'
  const response = await api({
    method,
    url,
    params: isGet ? data : null,
    data: isGet ? null : data,
    ...config
  });
  return response.data
}