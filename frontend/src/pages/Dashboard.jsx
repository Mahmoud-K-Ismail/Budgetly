import { useState, useEffect } from 'react'
import { useUser } from '../context/UserContext'
import { summaryAPI } from '../api/api'
import UserSetupForm from '../components/UserSetupForm'
import BudgetSummaryCard from '../components/BudgetSummaryCard'
import SpendingChart from '../components/SpendingChart'
import RecommendationsPanel from '../components/RecommendationsPanel'
import RecentExpenses from '../components/RecentExpenses'
import { Loader2 } from 'lucide-react'

const Dashboard = () => {
  const { currentUser } = useUser()
  const [dashboardData, setDashboardData] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    if (currentUser) {
      fetchDashboardData()
    }
  }, [currentUser])

  const fetchDashboardData = async () => {
    if (!currentUser) return
    
    setLoading(true)
    setError(null)
    
    try {
      const response = await summaryAPI.getDashboard(currentUser.id)
      setDashboardData(response.data)
    } catch (err) {
      setError('Failed to load dashboard data')
      console.error('Dashboard error:', err)
    } finally {
      setLoading(false)
    }
  }

  if (!currentUser) {
    return (
      <div className="max-w-2xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-4">
            Welcome to NYUAD Budgetly
          </h1>
          <p className="text-gray-600">
            Set up your profile to start tracking your monthly stipend and expenses
          </p>
        </div>
        <UserSetupForm onSuccess={fetchDashboardData} />
      </div>
    )
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-64">
        <div className="flex items-center space-x-2">
          <Loader2 className="w-6 h-6 animate-spin text-nyuad-600" />
          <span className="text-gray-600">Loading dashboard...</span>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="text-center py-8">
        <div className="text-red-600 mb-4">{error}</div>
        <button
          onClick={fetchDashboardData}
          className="btn-primary"
        >
          Try Again
        </button>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-600 mt-1">
            Track your budget and spending patterns
          </p>
        </div>
        <div className="mt-4 sm:mt-0">
          <button
            onClick={fetchDashboardData}
            className="btn-secondary"
          >
            Refresh
          </button>
        </div>
      </div>

      {dashboardData && (
        <>
          {/* Budget Summary Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <BudgetSummaryCard
              title="Monthly Stipend"
              value={`$${dashboardData.user.stipend.toLocaleString()}`}
              subtitle="Your monthly budget"
              color="nyuad"
            />
            <BudgetSummaryCard
              title="Total Spent"
              value={`$${dashboardData.budget_summary.total_expenses.toLocaleString()}`}
              subtitle="This month"
              color="primary"
            />
            <BudgetSummaryCard
              title="Remaining Budget"
              value={`$${dashboardData.budget_summary.remaining_budget.toLocaleString()}`}
              subtitle="Available to spend"
              color={dashboardData.budget_summary.remaining_budget >= 0 ? "success" : "danger"}
            />
            <BudgetSummaryCard
              title="Daily Limit"
              value={`$${dashboardData.budget_summary.daily_limit.toFixed(2)}`}
              subtitle="Recommended daily spending"
              color="warning"
            />
          </div>

          {/* Charts and Insights */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Spending Chart */}
            <div className="card">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                Spending by Category
              </h3>
              <SpendingChart data={dashboardData.budget_summary.expenses_by_category} />
            </div>

            {/* Recommendations */}
            <div className="card">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                Smart Recommendations
              </h3>
              <RecommendationsPanel recommendations={dashboardData.recommendations} />
            </div>
          </div>

          {/* Recent Expenses */}
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Recent Expenses
            </h3>
            <RecentExpenses expenses={dashboardData.recent_expenses} />
          </div>

          {/* Progress Overview */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="card">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                Budget Progress
              </h3>
              <div className="space-y-4">
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span>Budget Used</span>
                    <span>{((dashboardData.budget_summary.total_expenses / dashboardData.user.stipend) * 100).toFixed(1)}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-nyuad-600 h-2 rounded-full transition-all duration-300"
                      style={{
                        width: `${Math.min((dashboardData.budget_summary.total_expenses / dashboardData.user.stipend) * 100, 100)}%`
                      }}
                    ></div>
                  </div>
                </div>
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span>Savings Goal</span>
                    <span>${dashboardData.user.savings_goal.toLocaleString()}</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-success-600 h-2 rounded-full transition-all duration-300"
                      style={{
                        width: `${Math.min((dashboardData.budget_summary.remaining_budget / dashboardData.user.savings_goal) * 100, 100)}%`
                      }}
                    ></div>
                  </div>
                </div>
              </div>
            </div>

            <div className="card">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                Quick Stats
              </h3>
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-gray-600">Days Elapsed:</span>
                  <span className="font-medium">{dashboardData.budget_summary.days_elapsed}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Days Remaining:</span>
                  <span className="font-medium">{dashboardData.budget_summary.days_remaining}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Average Daily:</span>
                  <span className="font-medium">
                    ${(dashboardData.budget_summary.total_expenses / Math.max(dashboardData.budget_summary.days_elapsed, 1)).toFixed(2)}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Largest Category:</span>
                  <span className="font-medium capitalize">
                    {dashboardData.statistics.category_breakdown && 
                     Object.keys(dashboardData.statistics.category_breakdown).length > 0
                      ? Object.entries(dashboardData.statistics.category_breakdown)
                          .sort(([,a], [,b]) => b.total - a.total)[0][0]
                      : 'None'}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  )
}

export default Dashboard 