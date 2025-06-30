import { Trash2 } from 'lucide-react'
import { plannedPurchaseAPI } from '../api/api'
import toast from 'react-hot-toast'

const PlannedPurchaseList = ({ purchases = [], onDelete }) => {
  const handleDelete = async (id) => {
    try {
      await plannedPurchaseAPI.delete(id)
      toast.success('Removed')
      onDelete && onDelete(id)
    } catch {
      toast.error('Failed to delete')
    }
  }

  if (!purchases.length) {
    return <p className="text-gray-500">No items in wishlist yet.</p>
  }

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full text-sm">
        <thead className="bg-gray-50 text-gray-700">
          <tr>
            <th className="px-4 py-2 text-left">Item</th>
            <th className="px-4 py-2 text-right">Price</th>
            <th className="px-4 py-2 text-center">Priority</th>
            <th className="px-4 py-2 text-center">Date</th>
            <th className="px-4 py-2"></th>
            <th className="px-4 py-2 text-center">Deal</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-200">
          {purchases.map((p) => (
            <tr key={p.id}>
              <td className="px-4 py-2 font-medium text-gray-800">{p.item_name}</td>
              <td className="px-4 py-2 text-right">${p.expected_price.toLocaleString()}</td>
              <td className="px-4 py-2 text-center capitalize">{p.priority}</td>
              <td className="px-4 py-2 text-center">{p.desired_date}</td>
              <td className="px-4 py-2 text-center">
                <button onClick={() => handleDelete(p.id)} className="text-danger-600 hover:text-danger-800">
                  <Trash2 className="w-4 h-4" />
                </button>
              </td>
              <td className="px-4 py-2 text-center">
                <a href={`/deals/${p.id}`} className="text-nyuad-600 hover:underline text-sm">Where to buy?</a>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default PlannedPurchaseList 