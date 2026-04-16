/**
 * API 基础地址
 * - 本地开发：VITE_API_BASE_URL 为空，走 vite.config.js proxy（/api → localhost:8000）
 * - 生产环境：VITE_API_BASE_URL=https://api.yourdomain.com
 */
export const API_BASE = import.meta.env.VITE_API_BASE_URL || ''
