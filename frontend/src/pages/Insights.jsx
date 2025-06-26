import { useState, useEffect } from 'react'
import { useUser } from '../context/UserContext'
import { summaryAPI } from '../api/api'
import { TrendingUp, BarChart3, PieChart, Target, AlertTriangle, CheckCircle } from 'lucide-react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts'

const Insights = () => {
  const { currentUser } = useUser()
  const [insightsData, setInsightsData] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    if (currentUser) {
      fetchInsights()
    }
  }, [currentUser])

  const fetchInsights = async () => {
    if (!currentUser) return
    
    setLoading(true)
    setError(null)
    
    try {
      const [insightsResponse, statisticsResponse, recommendationsResponse] = await Promise.all([
        summaryAPI.getInsights(currentUser.id),
        summaryAPI.getStatistics(currentUser.id),
        summaryAPI.getRecommendations(currentUser.id)
      ])
      
      setInsightsData({
        insights: insightsResponse.data,
        statistics: statisticsResponse.data,
        recommendations: recommendationsResponse.data
      })
    } catch (err) {
      setError('Failed to load insights data')
      console.error('Insights error:', err)
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

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-64">
        <div className="flex items-center space-x-2">
          <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-nyuad-600"></div>
          <span className="text-gray-600">Loading insights...</span>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="text-center py-8">
        <div className="text-red-600 mb-4">{error}</div>
        <button
          onClick={fetchInsights}
          className="btn-primary"
        >
          Try Again
        </button>
      </div>
    )
  }

  if (!insightsData) {
    return null
  }

  const { insights, statistics, recommendations } = insightsData

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Financial Insights</h1>
          <p className="text-gray-600 mt-1">
            Deep dive into your spending patterns and financial health
          </p>
        </div>
        <div className="mt-4 sm:mt-0">
          <button
            onClick={fetchInsights}
            className="btn-secondary"
          >
            Refresh
          </button>
        </div>
      </div>

      {/* Key Insights */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div className="card">
          <div className="flex items-center space-x-3 mb-4">
            <div className="w-10 h-10 bg-nyuad-100 rounded-lg flex items-center justify-center">
              <TrendingUp className="w-5 h-5 text-nyuad-600" />
            </div>
            <div>
              <h3 className="font-semibold text-gray-900">Average Daily Spending</h3>
              <p className="text-sm text-gray-600">Your daily average</p>
            </div>
          </div>
          <div className="text-2xl font-bold text-nyuad-600">
            ${statistics.statistics.average_daily_spending?.toFixed(2) || '0.00'}
          </div>
        </div>

        <div className="card">
          <div className="flex items-center space-x-3 mb-4">
            <div className="w-10 h-10 bg-primary-100 rounded-lg flex items-center justify-center">
              <BarChart3 className="w-5 h-5 text-primary-600" />
            </div>
            <div>
              <h3 className="font-semibold text-gray-900">Total Expenses</h3>
              <p className="text-sm text-gray-600">This month</p>
            </div>
          </div>
          <div className="text-2xl font-bold text-primary-600">
            ${statistics.statistics.total_expenses?.toFixed(2) || '0.00'}
          </div>
        </div>

        <div className="card">
          <div className="flex items-center space-x-3 mb-4">
            <div className="w-10 h-10 bg-success-100 rounded-lg flex items-center justify-center">
              <Target className="w-5 h-5 text-success-600" />
            </div>
            <div>
              <h3 className="font-semibold text-gray-900">Largest Expense</h3>
              <p className="text-sm text-gray-600">Single purchase</p>
            </div>
          </div>
          <div className="text-2xl font-bold text-success-600">
            ${statistics.statistics.largest_expense?.toFixed(2) || '0.00'}
          </div>
        </div>
      </div>

      {/* Spending Analysis */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Category Breakdown */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
            <PieChart className="w-5 h-5 mr-2" />
            Category Breakdown
          </h3>
          {statistics.statistics.category_breakdown && Object.keys(statistics.statistics.category_breakdown).length > 0 ? (
            <div className="space-y-3">
              {Object.entries(statistics.statistics.category_breakdown)
                .sort(([,a], [,b]) => b.total - a.total)
                .map(([category, data]) => (
                  <div key={category} className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      <div className="w-3 h-3 bg-nyuad-500 rounded-full"></div>
                      <span className="font-medium capitalize">{category}</span>
                    </div>
                    <div className="text-right">
                      <div className="font-semibold">${data.total.toFixed(2)}</div>
                      <div className="text-sm text-gray-500">{data.count} expenses</div>
                    </div>
                  </div>
                ))}
            </div>
          ) : (
            <div className="text-center py-8 text-gray-500">
              <PieChart className="w-12 h-12 mx-auto mb-2 text-gray-300" />
              <p>No category data available</p>
            </div>
          )}
        </div>

        {/* Spending Insights */}
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
            <TrendingUp className="w-5 h-5 mr-2" />
            Key Insights
          </h3>
          {insights.insights && insights.insights.length > 0 ? (
            <div className="space-y-3">
              {insights.insights.map((insight, index) => (
                <div key={index} className="flex items-start space-x-3 p-3 bg-gray-50 rounded-lg">
                  <div className="flex-shrink-0 mt-0.5">
                    <div className="w-2 h-2 bg-nyuad-500 rounded-full"></div>
                  </div>
                  <p className="text-sm text-gray-700">{insight}</p>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-8 text-gray-500">
              <TrendingUp className="w-12 h-12 mx-auto mb-2 text-gray-300" />
              <p>No insights available yet</p>
              <p className="text-sm">Add more expenses to get personalized insights</p>
            </div>
          )}
        </div>
      </div>

      {/* Recommendations */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
          <CheckCircle className="w-5 h-5 mr-2" />
          Smart Recommendations
        </h3>
        {recommendations && recommendations.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {recommendations.map((rec, index) => (
              <div
                key={index}
                className={`p-4 rounded-lg border-l-4 ${
                  rec.priority === 'high' ? 'border-danger-200 bg-danger-50' :
                  rec.priority === 'medium' ? 'border-warning-200 bg-warning-50' :
                  'border-nyuad-200 bg-nyuad-50'
                }`}
              >
                <div className="flex items-start space-x-3">
                  <div className="flex-shrink-0 mt-0.5">
                    {rec.priority === 'high' ? (
                      <AlertTriangle className="w-4 h-4 text-danger-600" />
                    ) : (
                      <CheckCircle className="w-4 h-4 text-nyuad-600" />
                    )}
                  </div>
                  <div>
                    <p className="text-sm font-medium text-gray-900">{rec.message}</p>
                    <div className="mt-2">
                      <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                        rec.priority === 'high' ? 'bg-danger-100 text-danger-800' :
                        rec.priority === 'medium' ? 'bg-warning-100 text-warning-800' :
                        'bg-nyuad-100 text-nyuad-800'
                      }`}>
                        {rec.priority} priority
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-8 text-gray-500">
            <CheckCircle className="w-12 h-12 mx-auto mb-2 text-gray-300" />
            <p>No recommendations available</p>
            <p className="text-sm">Add more expenses to get personalized advice</p>
          </div>
        )}
      </div>

      {/* Suggestions */}
      {insights.suggestions && insights.suggestions.length > 0 && (
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Actionable Suggestions</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {insights.suggestions.map((suggestion, index) => (
              <div key={index} className="flex items-center space-x-3 p-3 bg-success-50 rounded-lg">
                <div className="w-2 h-2 bg-success-500 rounded-full"></div>
                <span className="text-sm text-success-800">{suggestion}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default Insights 