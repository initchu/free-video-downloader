import axios from 'axios'
import { API_BASE } from './config'

const api = axios.create({
  baseURL: `${API_BASE}/api`,
  timeout: 120000,
})

export async function parseVideo(url) {
  const { data } = await api.post('/parse', { url })
  return data
}

export async function getDirectUrl(url, formatId) {
  const { data } = await api.post('/direct-url', { url, format_id: formatId })
  return data
}

export function getDownloadUrl() {
  return `${API_BASE}/api/download`
}

export async function downloadViaServer(url, formatId) {
  const response = await api.post(
    '/download',
    { url, format_id: formatId },
    { responseType: 'blob', timeout: 600000 }
  )
  return response
}
