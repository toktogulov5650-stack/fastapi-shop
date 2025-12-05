/**
 * Pinia store для управления состоянием товаров и категорий
 */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { productsAPI, categoriesAPI } from '@/services/api'

export const useProductsStore = defineStore('products', () => {
  // State
  const products = ref([])
  const categories = ref([])
  const selectedCategory = ref(null)
  const loading = ref(false)
  const error = ref(null)

  // Getters
  const filteredProducts = computed(() => {
    if (!selectedCategory.value) {
      return products.value
    }
    return products.value.filter(
      (product) => product.category_id === selectedCategory.value
    )
  })

  const productsCount = computed(() => filteredProducts.value.length)

  // Actions
  async function fetchProducts() {
    loading.value = true
    error.value = null
    try {
      const response = await productsAPI.getAll()
      products.value = response.products // исправлено для согласования с API
    } catch (err) {
      error.value = 'Failed to load products'
      console.error('Error fetching products:', err)
    } finally {
      loading.value = false
    }
  }

  async function fetchProductById(id) {
    loading.value = true
    error.value = null
    try {
      const response = await productsAPI.getById(id)
      return response // уже объект продукта
    } catch (err) {
      error.value = 'Failed to load product'
      console.error('Error fetching product:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchCategories() {
    try {
      const response = await categoriesAPI.getAll()
      categories.value = response // теперь categories.value — массив
    } catch (err) {
      console.error('Error fetching categories:', err)
    }
  }

  function setCategory(categoryId) {
    selectedCategory.value = categoryId
  }

  function clearCategoryFilter() {
    selectedCategory.value = null
  }

  return {
    // State
    products,
    categories,
    selectedCategory,
    loading,
    error,
    // Getters
    filteredProducts,
    productsCount,
    // Actions
    fetchProducts,
    fetchProductById,
    fetchCategories,
    setCategory,
    clearCategoryFilter,
  }
})

