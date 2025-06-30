import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add any auth tokens here if needed
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message)
    return Promise.reject(error)
  }
)

// User API
export const userAPI = {
  createUser: (userData) => api.post('/user', userData),
  getUser: (userId) => api.get(`/user/${userId}`),
  updateUser: (userId, userData) => api.put(`/user/${userId}`, userData),
  deleteUser: (userId) => api.delete(`/user/${userId}`),
}

// Expense API
export const expenseAPI = {
  createExpense: (expenseData) => api.post('/expenses', expenseData),
  getUserExpenses: (userId, filters = {}) => api.get(`/expenses/${userId}`, { params: filters }),
  getExpense: (expenseId) => api.get(`/expense/${expenseId}`),
  updateExpense: (expenseId, expenseData) => api.put(`/expense/${expenseId}`, expenseData),
  deleteExpense: (expenseId) => api.delete(`/expense/${expenseId}`),
  getCategories: () => api.get('/expenses/categories'),
  getRecentExpenses: (userId, limit = 5) => api.get(`/expenses/recent/${userId}`, { params: { limit } }),
}

// Summary API
export const summaryAPI = {
  getBudgetSummary: (userId) => api.get(`/summary/${userId}`),
  getRecommendations: (userId) => api.get(`/recommendations/${userId}`),
  getInsights: (userId) => api.get(`/insights/${userId}`),
  getStatistics: (userId) => api.get(`/statistics/${userId}`),
  getDashboard: (userId) => api.get(`/dashboard/${userId}`),
  getReport: (userId, format = 'json', startDate = null, endDate = null) => 
    api.get(`/report/${userId}`, { 
      params: { format, start_date: startDate, end_date: endDate },
      responseType: format === 'csv' ? 'blob' : 'json'
    }),
}

// Planned Purchase API
export const plannedPurchaseAPI = {
  add: (data) => api.post('/planned-purchases', data),
  list: (userId) => api.get(`/planned-purchases/${userId}`),
  delete: (purchaseId) => api.delete(`/planned-purchases/${purchaseId}`),
}

// Advice API
export const adviceAPI = {
  getAdvice: (userId) => api.get(`/advice/${userId}`),
}

export default api 