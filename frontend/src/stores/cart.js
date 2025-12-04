// frontend/src/stores/cart.js
/**
 * Pinia store для управления корзиной покупок.
 * Хранит состояние корзины в памяти и синхронизирует с backend.
 */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { cartAPI } from '@/services/api'

export const useCartStore = defineStore('cart', () => {
  // State - храним корзину как объект {product_id: quantity}
  const cartItems = ref({})
  const cartDetails = ref(null)
  const loading = ref(false)
  const error = ref(null)

  // Getters
  const itemsCount = computed(() => {
    return Object.values(cartItems.value).reduce((sum, qty) => sum + qty, 0)
  })

  const totalPrice = computed(() => {
    return cartDetails.value?.total || 0
  })

  const hasItems = computed(() => {
    return Object.keys(cartItems.value).length > 0
  })

  // Actions
  /**
   * Добавить товар в корзину
   */
  async function addToCart(productId, quantity = 1) {
    loading.value = true
    error.value = null

    try {
      const response = await cartAPI.addItem(productId, quantity, cartItems.value)

      if (response && response.cart) {
        cartItems.value = response.cart
        await fetchCartDetails()
        console.log('✅ Товар добавлен в корзину:', cartItems.value)
        return true
      }

      throw new Error('Неверный формат ответа от сервера')
    } catch (err) {
      console.error('❌ Ошибка добавления в корзину:', err)
      error.value = err.message
      return false
    } finally {
      loading.value = false
    }
  }

  /**
   * Получить детальную информацию о корзине
   */
  async function fetchCartDetails() {
    if (!hasItems.value) {
      cartDetails.value = { items: [], total: 0, items_count: 0 }
      return
    }

    loading.value = true
    try {
      const response = await cartAPI.getCart(cartItems.value)
      cartDetails.value = response
      console.log('📦 Детали корзины загружены:', cartDetails.value)
    } catch (err) {
      console.error('❌ Ошибка загрузки корзины:', err)
      error.value = err.message
    } finally {
      loading.value = false
    }
  }

  /**
   * Обновить количество товара
   */
  async function updateQuantity(productId, quantity) {
    if (quantity <= 0) {
      return removeFromCart(productId)
    }

    loading.value = true
    error.value = null

    try {
      const response = await cartAPI.updateItem(productId, quantity, cartItems.value)

      if (response && response.cart) {
        cartItems.value = response.cart
        await fetchCartDetails()
        return true
      }

      throw new Error('Неверный формат ответа от сервера')
    } catch (err) {
      console.error('❌ Ошибка обновления корзины:', err)
      error.value = err.message
      return false
    } finally {
      loading.value = false
    }
  }

  /**
   * Удалить товар из корзины
   */
  async function removeFromCart(productId) {
    loading.value = true
    error.value = null

    try {
      const response = await cartAPI.removeItem(productId, cartItems.value)

      if (response && response.cart) {
        cartItems.value = response.cart
        await fetchCartDetails()
        return true
      }

      throw new Error('Неверный формат ответа от сервера')
    } catch (err) {
      console.error('❌ Ошибка удаления из корзины:', err)
      error.value = err.message
      return false
    } finally {
      loading.value = false
    }
  }

  /**
   * Очистить корзину
   */
  function clearCart() {
    cartItems.value = {}
    cartDetails.value = null
    error.value = null
  }

  return {
    // State
    cartItems,
    cartDetails,
    loading,
    error,
    // Getters
    itemsCount,
    totalPrice,
    hasItems,
    // Actions
    addToCart,
    fetchCartDetails,
    updateQuantity,
    removeFromCart,
    clearCart,
  }
})
