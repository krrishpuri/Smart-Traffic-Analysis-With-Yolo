
import axios from 'axios'

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000',
  headers: {
    'Content-Type': 'application/json',
  },
})

export const getTrafficSummary = async () => {
  const response = await api.get('/api/traffic/summary')
  return response.data
}

export const getHealth = async () => {
  const response = await api.get('/api/health')
  return response.data
}

export const getAvailableVideos = async () => {
  const response = await api.get('/api/traffic/videos')
  return response.data
}

export const selectVideo = async (filename) => {
  const response = await api.post('/api/traffic/videos/select', { filename })
  return response.data
}

export default api
