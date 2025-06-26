import { useState, useEffect } from 'react'
import { useUser } from '../context/UserContext'
import { expenseAPI } from '../api/api'
import { Plus, DollarSign, Tag, Calendar, FileText } from 'lucide-react'
import toast from 'react-hot-toast'

const AddExpense = () => {
  const { currentUser } = useUser()
  const [categories, setCategories] = useState([])
  const [loading, setLoading] = useState(false)
  const [formData, setFormData] = useState({
    amount: '',
    category: '',
    description: '',
    date: new Date().toISOString().split('T')[0]
  })

  useEffect(() => {
    fetchCategories()
  }, [])

  const fetchCategories = async () => {
    try {
      const response = await expenseAPI.getCategories()
      setCategories(response.data)
    } catch (error) {
      console.error('Failed to fetch categories:', error)
    }
  }

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!currentUser) {
      toast.error('Please set up your profile first')
      return
    }

    if (!formData.amount || !formData.category || !formData.date) {
      toast.error('Please fill in all required fields')
      return
    }

    if (parseFloat(formData.amount) <= 0) {
      toast.error('Amount must be greater than 0')
      return
    }

    setLoading(true)
    
    try {
      const expenseData = {
        user_id: currentUser.id,
        amount: parseFloat(formData.amount),
        category: formData.category,
        description: formData.description,
        date: formData.date
      }
      
      await expenseAPI.createExpense(expenseData)
      
      toast.success('Expense added successfully!')
      
      // Reset form
      setFormData({
        amount: '',
        category: '',
        description: '',
        date: new Date().toISOString().split('T')[0]
      })
    } catch (error) {
      console.error('Add expense error:', error)
      toast.error(error.response?.data?.detail || 'Failed to add expense')
    } finally {
      setLoading(false)
    }
  }

  if (!currentUser) {
    return (
      <div className="text-center py-8">
        <div className="text-red-600 mb-4">Please set up your profile first</div>
        <p className="text-gray-600">Go to the dashboard to create your profile</p>
      </div>
    )
  }

  return (
    <div className="max-w-2xl mx-auto">
      <div className="text-center mb-8">
        <div className="w-16 h-16 bg-gradient-to-br from-nyuad-500 to-primary-600 rounded-full flex items-center justify-center mx-auto mb-4">
          <Plus className="w-8 h-8 text-white" />
        </div>
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Add New Expense</h1>
        <p className="text-gray-600">
          Track your spending to stay on budget
        </p>
      </div>

      <div className="card">
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Amount */}
          <div>
            <label htmlFor="amount" className="form-label flex items-center">
              <DollarSign className="w-4 h-4 mr-2" />
              Amount (AED)
            </label>
            <input
              type="number"
              id="amount"
              name="amount"
              value={formData.amount}
              onChange={handleChange}
              placeholder="e.g., 25.50"
              min="0"
              step="0.01"
              className="input-field"
              required
            />
          </div>

          {/* Category */}
          <div>
            <label htmlFor="category" className="form-label flex items-center">
              <Tag className="w-4 h-4 mr-2" />
              Category
            </label>
            <select
              id="category"
              name="category"
              value={formData.category}
              onChange={handleChange}
              className="input-field"
              required
            >
              <option value="">Select a category</option>
              {categories.map((category) => (
                <option key={category} value={category}>
                  {category.charAt(0).toUpperCase() + category.slice(1)}
                </option>
              ))}
            </select>
          </div>

          {/* Date */}
          <div>
            <label htmlFor="date" className="form-label flex items-center">
              <Calendar className="w-4 h-4 mr-2" />
              Date
            </label>
            <input
              type="date"
              id="date"
              name="date"
              value={formData.date}
              onChange={handleChange}
              className="input-field"
              required
            />
          </div>

          {/* Description */}
          <div>
            <label htmlFor="description" className="form-label flex items-center">
              <FileText className="w-4 h-4 mr-2" />
              Description (Optional)
            </label>
            <textarea
              id="description"
              name="description"
              value={formData.description}
              onChange={handleChange}
              placeholder="e.g., Lunch at cafeteria, Bus fare, etc."
              rows="3"
              className="input-field resize-none"
            />
          </div>

          {/* Submit Button */}
          <button
            type="submit"
            disabled={loading}
            className="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? 'Adding Expense...' : 'Add Expense'}
          </button>
        </form>
      </div>

      {/* Quick Add Categories */}
      <div className="mt-6 card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Add Common Categories</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          {['food', 'transport', 'entertainment', 'shopping', 'utilities', 'health', 'education'].map((category) => (
            <button
              key={category}
              onClick={() => setFormData(prev => ({ ...prev, category }))}
              className="px-3 py-2 text-sm border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors duration-200"
            >
              {category.charAt(0).toUpperCase() + category.slice(1)}
            </button>
          ))}
        </div>
      </div>

      {/* Tips */}
      <div className="mt-6 p-4 bg-nyuad-50 rounded-lg">
        <h4 className="font-medium text-nyuad-800 mb-2">💡 Tips for Better Tracking</h4>
        <ul className="text-sm text-nyuad-700 space-y-1">
          <li>• Add expenses as soon as you make them</li>
          <li>• Use descriptive names for better insights</li>
          <li>• Categorize consistently for accurate reports</li>
          <li>• Include even small expenses - they add up!</li>
        </ul>
      </div>
    </div>
  )
}

export default AddExpense 