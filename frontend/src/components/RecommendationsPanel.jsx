import { AlertCircle, CheckCircle, Info, TrendingUp } from 'lucide-react'

const RecommendationsPanel = ({ recommendations = [] }) => {
  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'high':
        return 'border-danger-200 bg-danger-50 text-danger-800'
      case 'medium':
        return 'border-warning-200 bg-warning-50 text-warning-800'
      case 'low':
        return 'border-nyuad-200 bg-nyuad-50 text-nyuad-800'
      default:
        return 'border-gray-200 bg-gray-50 text-gray-800'
    }
  }

  const getPriorityIcon = (priority) => {
    switch (priority) {
      case 'high':
        return <AlertCircle className="w-4 h-4" />
      case 'medium':
        return <TrendingUp className="w-4 h-4" />
      case 'low':
        return <CheckCircle className="w-4 h-4" />
      default:
        return <Info className="w-4 h-4" />
    }
  }

  if (!recommendations || recommendations.length === 0) {
    return (
      <div className="flex items-center justify-center h-64 text-gray-500">
        <div className="text-center">
          <div className="text-4xl mb-2">💡</div>
          <p>No recommendations yet</p>
          <p className="text-sm">Add some expenses to get personalized advice</p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-3">
      {recommendations.map((rec, index) => (
        <div
          key={index}
          className={`p-4 rounded-lg border-l-4 ${getPriorityColor(rec.priority)}`}
        >
          <div className="flex items-start space-x-3">
            <div className="flex-shrink-0 mt-0.5">
              {getPriorityIcon(rec.priority)}
            </div>
            <div className="flex-1">
              <p className="text-sm font-medium">{rec.message}</p>
              <div className="mt-2 flex items-center space-x-2">
                <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                  rec.priority === 'high' ? 'bg-danger-100 text-danger-800' :
                  rec.priority === 'medium' ? 'bg-warning-100 text-warning-800' :
                  'bg-nyuad-100 text-nyuad-800'
                }`}>
                  {rec.priority} priority
                </span>
                <span className="text-xs text-gray-500 capitalize">
                  {rec.type.replace('_', ' ')}
                </span>
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}

export default RecommendationsPanel 