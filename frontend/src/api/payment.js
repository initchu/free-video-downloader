import axios from 'axios'
import { getToken } from './auth'
import { API_BASE } from './config'

function authHeaders() {
  const token = getToken()
  return token ? { Authorization: `Bearer ${token}` } : {}
}

export async function createCheckoutSession(planType = 'monthly') {
  const res = await axios.post(
    `${API_BASE}/api/payment/create-checkout`,
    { plan_type: planType },
    { headers: authHeaders() }
  )
  return res.data.data
}

export async function getOrders() {
  const res = await axios.get(`${API_BASE}/api/payment/orders`, { headers: authHeaders() })
  return res.data.data
}
