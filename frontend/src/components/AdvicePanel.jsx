import { Lightbulb, Slash, Clock } from 'lucide-react'

const AdvicePanel = ({ advice, loading, purchases = [] }) => {
  if (loading) {
    return <p className="text-gray-500 animate-pulse">Fetching fresh advice…</p>
  }

  if (!advice) {
    return <p className="text-gray-500">No advice yet.</p>
  }

  return (
    <div className="space-y-6">
      {/* Cuts Section */}
      <div>
        <h4 className="font-semibold text-gray-800 mb-2 flex items-center space-x-2">
          <Slash className="w-4 h-4" />
          <span>Expenses to Cut</span>
        </h4>
        {advice.cuts && advice.cuts.length ? (
          <ul className="list-disc list-inside space-y-1">
            {advice.cuts.map((c) => (
              <li key={c.expense_id} className="text-sm text-danger-700">
                Save ${c.amount_saved.toLocaleString()} &mdash; {c.reason}
              </li>
            ))}
          </ul>
        ) : (
          <p className="text-sm text-gray-500">No major cuts identified.</p>
        )}
      </div>

      {/* Planned Purchases */}
      <div>
        <h4 className="font-semibold text-gray-800 mb-2 flex items-center space-x-2">
          <Lightbulb className="w-4 h-4" />
          <span>Upcoming Purchases</span>
        </h4>
        {advice.next_purchases && advice.next_purchases.length ? (
          <ul className="space-y-2">
            {advice.next_purchases.map((p) => {
              const purchase = purchases.find((pp) => pp.id === p.id)
              const verdictColor =
                p.verdict === 'buy_now'
                  ? 'bg-success-100 text-success-800'
                  : p.verdict === 'postpone'
                  ? 'bg-warning-100 text-warning-800'
                  : 'bg-danger-100 text-danger-800'
              return (
                <li key={p.id} className="p-4 rounded-md border space-y-2">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                      <span className={`px-2 py-1 rounded-full text-xs font-semibold capitalize ${verdictColor}`}>
                        {p.verdict.replace('_', ' ')}
                      </span>
                      {purchase && (
                        <span className="text-xs text-gray-700 font-medium">{purchase.item_name}</span>
                      )}
                    </div>
                    <span className="text-xs text-gray-500">Score {p.score}</span>
                  </div>
                  <p className="text-sm text-gray-700">{p.suggestion}</p>
                  {/* Score bar */}
                  <div className="w-full bg-gray-200 h-1 rounded-full">
                    <div
                      className={`${verdictColor.replace('100', '500')} h-1 rounded-full`}
                      style={{ width: `${p.score}%` }}
                    ></div>
                  </div>
                </li>
              )
            })}
          </ul>
        ) : (
          <p className="text-sm text-gray-500">No planned purchases yet.</p>
        )}
      </div>
    </div>
  )
}

export default AdvicePanel 