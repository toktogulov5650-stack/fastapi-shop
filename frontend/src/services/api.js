// frontend/src/services/api.js
/**
 * API сервис для взаимодействия с backend.
 * Централизует все HTTP запросы к FastAPI серверу.
 */

import axios from 'axios'

// Базовый URL — если VITE_API_BASE_URL не задан, используем '/api'
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api'

// Создаем axios-клиент
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
})

// Логирование ошибок
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message)
    return Promise.reject(error)
  }
)

/**
 * -----------------------------
 * PRODUCTS API
 * -----------------------------
 */
export const productsAPI = {
  async getAll() {
    const response = await apiClient.get('/products')
    return response.data // { products: [...] }
  },

  async getById(id) {
    const response = await apiClient.get(`/products/${id}`)
    return response.data // { id, title, ... }
  },

  async getByCategory(categoryId) {
    const response = await apiClient.get(`/products/category/${categoryId}`)
    return response.data
  },
}

/**
 * -----------------------------
 * CATEGORIES API
 * -----------------------------
 */
export const categoriesAPI = {
  async getAll() {
    const response = await apiClient.get('/categories')
    return response.data // [ {id,name}, ... ]
  },

  async getById(id) {
    const response = await apiClient.get(`/categories/${id}`)
    return response.data
  },
}

/**
 * -----------------------------
 * CART API
 * -----------------------------
 */
export const cartAPI = {
  async addItem(productId, quantity, cartData = {}) {
    const response = await apiClient.post('/cart/add', {
      product_id: productId,
      quantity,
      cart: cartData,
    })
    return response.data
  },

  async getCart(cartData = {}) {
    const response = await apiClient.post('/cart', {
      cart: cartData,
    })
    return response.data
  },

  async updateItem(productId, quantity, cartData = {}) {
    const response = await apiClient.put('/cart/update', {
      product_id: productId,
      quantity,
      cart: cartData,
    })
    return response.data
  },

  async removeItem(productId, cartData = {}) {
    const response = await apiClient.delete(`/cart/remove/${productId}`, {
      data: { cart: cartData },
    })
    return response.data
  },
}

export default apiClient
