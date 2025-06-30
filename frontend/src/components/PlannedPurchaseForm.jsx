import { useState } from 'react'
import { plannedPurchaseAPI } from '../api/api'
import { useUser } from '../context/UserContext'
import toast from 'react-hot-toast'

const PlannedPurchaseForm = ({ onAdd }) => {
  const { currentUser } = useUser()
  const [formData, setFormData] = useState({
    item_name: '',
    expected_price: '',
    priority: 'medium',
    desired_date: '',
  })
  const [loading, setLoading] = useState(false)

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!currentUser) return
    setLoading(true)
    try {
      const payload = {
        ...formData,
        expected_price: parseFloat(formData.expected_price || 0),
        user_id: currentUser.id,
      }
      const res = await plannedPurchaseAPI.add(payload)
      toast.success('Added to wishlist')
      setFormData({ item_name: '', expected_price: '', priority: 'medium', desired_date: '' })
      onAdd && onAdd(res.data)
    } catch (err) {
      toast.error('Failed to add')
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {/* Row 1 */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="flex flex-col">
          <label className="text-sm font-medium mb-1">Item Name</label>
          <input
            type="text"
            name="item_name"
            value={formData.item_name}
            onChange={handleChange}
            className="input"
            placeholder="e.g., AirPods"
            required
          />
        </div>
        <div className="flex flex-col">
          <label className="text-sm font-medium mb-1">Expected Price ($)</label>
          <input
            type="number"
            name="expected_price"
            min="0"
            step="0.01"
            value={formData.expected_price}
            onChange={handleChange}
            className="input"
            placeholder="0.00"
            required
          />
        </div>
      </div>

      {/* Row 2 */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="flex flex-col">
          <label className="text-sm font-medium mb-1">Desired Date</label>
          <input
            type="date"
            name="desired_date"
            value={formData.desired_date}
            onChange={handleChange}
            className="input"
            required
          />
        </div>
        <div className="flex flex-col">
          <label className="text-sm font-medium mb-1">Priority</label>
          <select name="priority" value={formData.priority} onChange={handleChange} className="input">
            <option value="high">High</option>
            <option value="medium">Medium</option>
            <option value="low">Low</option>
          </select>
        </div>
      </div>

      <div className="text-right">
        <button type="submit" className="btn-primary" disabled={loading}>
          {loading ? 'Adding…' : 'Add to Wishlist'}
        </button>
      </div>
    </form>
  )
}

export default PlannedPurchaseForm 