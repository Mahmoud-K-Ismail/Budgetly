import { useEffect, useState } from 'react'
import PlannedPurchaseForm from '../components/PlannedPurchaseForm'
import PlannedPurchaseList from '../components/PlannedPurchaseList'
import { plannedPurchaseAPI, adviceAPI } from '../api/api'
import { useUser } from '../context/UserContext'
import AdvicePanel from '../components/AdvicePanel'
import { Loader2 } from 'lucide-react'

const Wishlist = () => {
  const { currentUser } = useUser()
  const [purchases, setPurchases] = useState([])
  const [advice, setAdvice] = useState(null)
  const [loading, setLoading] = useState(false)
  const [adviceLoading, setAdviceLoading] = useState(false)

  const loadData = async () => {
    if (!currentUser) return
    setLoading(true)
    try {
      const pRes = await plannedPurchaseAPI.list(currentUser.id)
      setPurchases(pRes.data)
      await fetchAdvice()
    } catch (err) {
      console.error('Wishlist load error', err)
    } finally {
      setLoading(false)
    }
  }

  const fetchAdvice = async () => {
    if (!currentUser) return
    setAdviceLoading(true)
    try {
      const res = await adviceAPI.getAdvice(currentUser.id)
      setAdvice(res.data)
    } finally {
      setAdviceLoading(false)
    }
  }

  useEffect(() => {
    loadData()
  }, [currentUser])

  const handleAdd = (purchase) => {
    setPurchases((prev) => [...prev, purchase])
    fetchAdvice()
  }

  const handleDelete = (id) => {
    setPurchases((prev) => prev.filter((p) => p.id !== id))
    fetchAdvice()
  }

  if (!currentUser) {
    return <p>Please set up your profile first.</p>
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-64">
        <Loader2 className="w-6 h-6 animate-spin text-nyuad-600" />
      </div>
    )
  }

  return (
    <div className="space-y-8">
      <div className="card">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Add to Wishlist</h2>
        <PlannedPurchaseForm onAdd={handleAdd} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Your Wishlist</h3>
          <PlannedPurchaseList purchases={purchases} onDelete={handleDelete} />
        </div>
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Personal Advisor</h3>
          <AdvicePanel advice={advice} loading={adviceLoading} purchases={purchases} />
        </div>
      </div>
    </div>
  )
}

export default Wishlist 