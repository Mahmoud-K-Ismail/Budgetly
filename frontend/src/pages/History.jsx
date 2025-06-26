import { useState, useEffect } from 'react'
import { useUser } from '../context/UserContext'
import { expenseAPI } from '../api/api'
import { History as HistoryIcon, Search, Filter, Download } from 'lucide-react'
import { format } from 'date-fns'
import toast from 'react-hot-toast'

const HistoryPage = () => {
  const { currentUser } = useUser()
  const [expenses, setExpenses] = useState([])
  const [loading, setLoading] = useState(false)
  const [categories, setCategories] = useState([])
  const [filters, setFilters] = useState({
    category: '',
    start_date: '',
    end_date: '',
    search: ''
  })

  useEffect(() => {
    if (currentUser) {
      fetchExpenses()
      fetchCategories()
    }
  }, [currentUser, filters])

  const fetchExpenses = async () => {
    if (!currentUser) return
    
    setLoading(true)
    try {
      const response = await expenseAPI.getUserExpenses(currentUser.id, filters)
      setExpenses(response.data)
    } catch (error) {
      console.error('Failed to fetch expenses:', error)
      toast.error('Failed to load expenses')
    } finally {
      setLoading(false)
    }
  }

  const fetchCategories = async () => {
    try {
      const response = await expenseAPI.getCategories()
      setCategories(response.data)
    } catch (error) {
      console.error('Failed to fetch categories:', error)
    }
  }

  const handleFilterChange = (name, value) => {
    setFilters(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const clearFilters = () => {
    setFilters({
      category: '',
      start_date: '',
      end_date: '',
      search: ''
    })
  }

  const downloadReport = async () => {
    if (!currentUser) return
    
    try {
      const response = await expenseAPI.getReport(currentUser.id, 'csv', filters.start_date, filters.end_date)
      
      // Create download link
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `expenses_${currentUser.id}_${new Date().toISOString().split('T')[0]}.csv`)
      document.body.appendChild(link)
      link.click()
      link.remove()
      
      toast.success('Report downloaded successfully!')
    } catch (error) {
      console.error('Download error:', error)
      toast.error('Failed to download report')
    }
  }

  const getCategoryColor = (category) => {
    const colors = {
      food: 'bg-orange-100 text-orange-800',
      transport: 'bg-blue-100 text-blue-800',
      entertainment: 'bg-purple-100 text-purple-800',
      shopping: 'bg-pink-100 text-pink-800',
      utilities: 'bg-gray-100 text-gray-800',
      health: 'bg-green-100 text-green-800',
      education: 'bg-indigo-100 text-indigo-800',
    }
    return colors[category] || 'bg-gray-100 text-gray-800'
  }

  if (!currentUser) {
    return (
      <div className="text-center py-8">
        <div className="text-red-600 mb-4">Please set up your profile first</div>
        <p className="text-gray-600">Go to the dashboard to create your profile</p>
      </div>
    )
  }

  const totalAmount = expenses.reduce((sum, expense) => sum + expense.amount, 0)

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Expense History</h1>
          <p className="text-gray-600 mt-1">
            View and manage all your expenses
          </p>
        </div>
        <div className="mt-4 sm:mt-0 flex space-x-2">
          <button
            onClick={downloadReport}
            className="btn-secondary flex items-center space-x-2"
          >
            <Download className="w-4 h-4" />
            <span>Export CSV</span>
          </button>
          <button
            onClick={fetchExpenses}
            className="btn-primary"
          >
            Refresh
          </button>
        </div>
      </div>

      {/* Filters */}
      <div className="card">
        <div className="flex items-center space-x-2 mb-4">
          <Filter className="w-5 h-5 text-gray-600" />
          <h3 className="text-lg font-semibold text-gray-900">Filters</h3>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          {/* Search */}
          <div>
            <label className="form-label">Search</label>
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
              <input
                type="text"
                placeholder="Search descriptions..."
                value={filters.search}
                onChange={(e) => handleFilterChange('search', e.target.value)}
                className="input-field pl-10"
              />
            </div>
          </div>

          {/* Category */}
          <div>
            <label className="form-label">Category</label>
            <select
              value={filters.category}
              onChange={(e) => handleFilterChange('category', e.target.value)}
              className="input-field"
            >
              <option value="">All Categories</option>
              {categories.map((category) => (
                <option key={category} value={category}>
                  {category.charAt(0).toUpperCase() + category.slice(1)}
                </option>
              ))}
            </select>
          </div>

          {/* Start Date */}
          <div>
            <label className="form-label">Start Date</label>
            <input
              type="date"
              value={filters.start_date}
              onChange={(e) => handleFilterChange('start_date', e.target.value)}
              className="input-field"
            />
          </div>

          {/* End Date */}
          <div>
            <label className="form-label">End Date</label>
            <input
              type="date"
              value={filters.end_date}
              onChange={(e) => handleFilterChange('end_date', e.target.value)}
              className="input-field"
            />
          </div>
        </div>

        <div className="mt-4 flex justify-between items-center">
          <button
            onClick={clearFilters}
            className="text-sm text-nyuad-600 hover:text-nyuad-700"
          >
            Clear Filters
          </button>
          <div className="text-sm text-gray-600">
            {expenses.length} expenses • Total: ${totalAmount.toFixed(2)}
          </div>
        </div>
      </div>

      {/* Expenses Table */}
      <div className="card">
        {loading ? (
          <div className="flex items-center justify-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-nyuad-600"></div>
          </div>
        ) : expenses.length === 0 ? (
          <div className="text-center py-8">
            <HistoryIcon className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-600">No expenses found</p>
            <p className="text-sm text-gray-500">Try adjusting your filters or add some expenses</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-200">
                  <th className="text-left py-3 px-4 font-medium text-gray-700">Date</th>
                  <th className="text-left py-3 px-4 font-medium text-gray-700">Category</th>
                  <th className="text-left py-3 px-4 font-medium text-gray-700">Description</th>
                  <th className="text-right py-3 px-4 font-medium text-gray-700">Amount</th>
                </tr>
              </thead>
              <tbody>
                {expenses.map((expense) => (
                  <tr key={expense.id} className="border-b border-gray-100 hover:bg-gray-50">
                    <td className="py-3 px-4">
                      <span className="text-sm text-gray-600">
                        {format(new Date(expense.date), 'MMM dd, yyyy')}
                      </span>
                    </td>
                    <td className="py-3 px-4">
                      <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${getCategoryColor(expense.category)}`}>
                        {expense.category.charAt(0).toUpperCase() + expense.category.slice(1)}
                      </span>
                    </td>
                    <td className="py-3 px-4">
                      <span className="text-sm text-gray-900">
                        {expense.description || 'No description'}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-right">
                      <span className="font-medium text-gray-900">
                        ${expense.amount.toFixed(2)}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  )
}

export default HistoryPage 