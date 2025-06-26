import { format } from 'date-fns'
import { Calendar, Tag, DollarSign } from 'lucide-react'

const RecentExpenses = ({ expenses = [] }) => {
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

  if (!expenses || expenses.length === 0) {
    return (
      <div className="flex items-center justify-center h-32 text-gray-500">
        <div className="text-center">
          <div className="text-3xl mb-2">📝</div>
          <p>No expenses yet</p>
          <p className="text-sm">Add your first expense to get started</p>
        </div>
      </div>
    )
  }

  return (
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
                <div className="flex items-center space-x-2">
                  <Calendar className="w-4 h-4 text-gray-400" />
                  <span className="text-sm text-gray-600">
                    {format(new Date(expense.date), 'MMM dd, yyyy')}
                  </span>
                </div>
              </td>
              <td className="py-3 px-4">
                <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${getCategoryColor(expense.category)}`}>
                  <Tag className="w-3 h-3 mr-1" />
                  {expense.category.charAt(0).toUpperCase() + expense.category.slice(1)}
                </span>
              </td>
              <td className="py-3 px-4">
                <span className="text-sm text-gray-900">
                  {expense.description || 'No description'}
                </span>
              </td>
              <td className="py-3 px-4 text-right">
                <div className="flex items-center justify-end space-x-1">
                  <DollarSign className="w-4 h-4 text-gray-400" />
                  <span className="font-medium text-gray-900">
                    {expense.amount.toFixed(2)}
                  </span>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default RecentExpenses 