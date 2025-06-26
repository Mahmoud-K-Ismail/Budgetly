import { useState } from 'react'
import { useUser } from '../context/UserContext'
import { Wallet, Target, Calendar } from 'lucide-react'
import toast from 'react-hot-toast'

const UserSetupForm = ({ onSuccess }) => {
  const { login } = useUser()
  const [formData, setFormData] = useState({
    stipend: '',
    savings_goal: '',
    budget_cycle_start: new Date().toISOString().split('T')[0]
  })
  const [loading, setLoading] = useState(false)

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!formData.stipend || !formData.savings_goal || !formData.budget_cycle_start) {
      toast.error('Please fill in all fields')
      return
    }

    if (parseFloat(formData.savings_goal) > parseFloat(formData.stipend)) {
      toast.error('Savings goal cannot exceed your stipend')
      return
    }

    setLoading(true)
    
    try {
      const userData = {
        stipend: parseFloat(formData.stipend),
        savings_goal: parseFloat(formData.savings_goal),
        budget_cycle_start: formData.budget_cycle_start
      }
      
      await login(userData)
      toast.success('Profile created successfully!')
      if (onSuccess) onSuccess()
    } catch (error) {
      console.error('Setup error:', error)
      toast.error(error.response?.data?.detail || 'Failed to create profile')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="card max-w-md mx-auto">
      <div className="text-center mb-6">
        <div className="w-16 h-16 bg-gradient-to-br from-nyuad-500 to-primary-600 rounded-full flex items-center justify-center mx-auto mb-4">
          <Wallet className="w-8 h-8 text-white" />
        </div>
        <h2 className="text-2xl font-bold text-gray-900">Set Up Your Profile</h2>
        <p className="text-gray-600 mt-2">
          Tell us about your monthly stipend and financial goals
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Monthly Stipend */}
        <div>
          <label htmlFor="stipend" className="form-label flex items-center">
            <Wallet className="w-4 h-4 mr-2" />
            Monthly Stipend (AED)
          </label>
          <input
            type="number"
            id="stipend"
            name="stipend"
            value={formData.stipend}
            onChange={handleChange}
            placeholder="e.g., 2000"
            min="0"
            step="0.01"
            className="input-field"
            required
          />
          <p className="text-sm text-gray-500 mt-1">
            Your monthly stipend from NYUAD
          </p>
        </div>

        {/* Savings Goal */}
        <div>
          <label htmlFor="savings_goal" className="form-label flex items-center">
            <Target className="w-4 h-4 mr-2" />
            Monthly Savings Goal (AED)
          </label>
          <input
            type="number"
            id="savings_goal"
            name="savings_goal"
            value={formData.savings_goal}
            onChange={handleChange}
            placeholder="e.g., 300"
            min="0"
            step="0.01"
            className="input-field"
            required
          />
          <p className="text-sm text-gray-500 mt-1">
            How much you want to save each month
          </p>
        </div>

        {/* Budget Cycle Start */}
        <div>
          <label htmlFor="budget_cycle_start" className="form-label flex items-center">
            <Calendar className="w-4 h-4 mr-2" />
            Budget Cycle Start Date
          </label>
          <input
            type="date"
            id="budget_cycle_start"
            name="budget_cycle_start"
            value={formData.budget_cycle_start}
            onChange={handleChange}
            className="input-field"
            required
          />
          <p className="text-sm text-gray-500 mt-1">
            When your monthly budget cycle begins
          </p>
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          disabled={loading}
          className="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? 'Creating Profile...' : 'Create Profile'}
        </button>
      </form>

      {/* Tips */}
      <div className="mt-6 p-4 bg-nyuad-50 rounded-lg">
        <h4 className="font-medium text-nyuad-800 mb-2">💡 Tips for Success</h4>
        <ul className="text-sm text-nyuad-700 space-y-1">
          <li>• Set a realistic savings goal (10-20% of stipend)</li>
          <li>• Choose the 1st of the month for easy tracking</li>
          <li>• You can update these settings later</li>
        </ul>
      </div>
    </div>
  )
}

export default UserSetupForm 