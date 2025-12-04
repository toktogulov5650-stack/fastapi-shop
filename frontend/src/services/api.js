// frontend/src/services/api.js
/**
 * API сервис для взаимодействия с backend.
 * Централизует все HTTP запросы к FastAPI серверу.
 * Использует axios для выполнения запросов.
 */

import axios from 'axios'

// Базовый URL API - используем относительный путь для одного порта
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api'

// Создаем экземпляр axios с настройками по умолчанию
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000, // 10 секунд
})

// Interceptor для логирования ошибок
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message)
    return Promise.reject(error)
  }
)

/**
 * API методы для работы с товарами
 */
export const productsAPI = {
  /**
   * Получить все товары
   */
  async getAll() {
    const response = await apiClient.get('/products')
    return response.data
  },

  /**
   * Получить товар по ID
   */
  async getById(id) {
    const response = await apiClient.get(`/products/${id}`)
    return response.data
  },

  /**
   * Получить товары по категории
   */
  async getByCategory(categoryId) {
    const response = await apiClient.get(`/products/category/${categoryId}`)
    return response.data
  },
}

/**
 * API методы для работы с категориями
 */
export const categoriesAPI = {
  /**
   * Получить все категории
   */
  async getAll() {
    const response = await apiClient.get('/categories')
    return response.data
  },

  /**
   * Получить категорию по ID
   */
  async getById(id) {
    const response = await apiClient.get(`/categories/${id}`)
    return response.data
  },
}

/**
 * API методы для работы с корзиной
 */
export const cartAPI = {
  /**
   * Добавить товар в корзину
   */
  async addItem(productId, quantity, cartData = {}) {
    const response = await apiClient.post('/cart/add', {
      product_id: productId,
      quantity: quantity,
      cart: cartData,
    })
    return response.data
  },

  /**
   * Получить содержимое корзины
   */
  async getCart(cartData = {}) {
    const response = await apiClient.post('/cart', {
      cart: cartData
    })
    return response.data
  },

  /**
   * Обновить количество товара
   */
  async updateItem(productId, quantity, cartData = {}) {
    const response = await apiClient.put('/cart/update', {
      product_id: productId,
      quantity: quantity,
      cart: cartData,
    })
    return response.data
  },

  /**
   * Удалить товар из корзины
   */
  async removeItem(productId, cartData = {}) {
    const response = await apiClient.delete(`/cart/remove/${productId}`, {
      data: {
        cart: cartData,
      },
    })
    return response.data
  },
}

export default apiClient
