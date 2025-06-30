import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { dealsAPI } from '../api/api'
import { Loader2 } from 'lucide-react'

const DealFinder = () => {
  const { id } = useParams()
  const [deals, setDeals] = useState(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    const fetchDeals = async () => {
      setLoading(true)
      try {
        const res = await dealsAPI.getDeals(id)
        setDeals(res.data)
      } catch (err) {
        console.error('Deals error', err)
      } finally {
        setLoading(false)
      }
    }

    fetchDeals()
  }, [id])

  if (loading || !deals) {
    return (
      <div className="flex items-center justify-center min-h-64">
        <Loader2 className="w-6 h-6 animate-spin text-nyuad-600" />
      </div>
    )
  }

  return (
    <div className="max-w-xl mx-auto space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Best Deals</h1>
      <ul className="space-y-4">
        {deals.map((d, idx) => (
          <li key={idx} className="p-4 border rounded-md space-y-1">
            <div className="flex items-center justify-between">
              <span className="font-medium text-gray-800">{d.merchant}</span>
              {typeof d.price === 'number' && d.price > 0 ? (
                <span className="text-sm text-gray-600">${d.price.toLocaleString()}</span>
              ) : typeof d.price === 'string' ? (
                <span className="text-sm text-gray-500 italic">{d.price}</span>
              ) : null}
            </div>
            <div className="text-sm text-gray-700">{d.item_name}</div>
            <a href={d.url} target="_blank" rel="noopener noreferrer" className="text-nyuad-600 hover:underline text-sm">
              View offer
            </a>
          </li>
        ))}
      </ul>
      <Link to="/wishlist" className="text-sm text-gray-600 hover:underline">← Back to wishlist</Link>
    </div>
  )
}

export default DealFinder 