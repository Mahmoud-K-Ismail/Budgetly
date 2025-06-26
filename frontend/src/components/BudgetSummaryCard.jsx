import { clsx } from 'clsx'

const BudgetSummaryCard = ({ title, value, subtitle, color = 'primary' }) => {
  const colorClasses = {
    primary: 'border-primary-200 bg-primary-50 text-primary-700',
    nyuad: 'border-nyuad-200 bg-nyuad-50 text-nyuad-700',
    success: 'border-success-200 bg-success-50 text-success-700',
    warning: 'border-warning-200 bg-warning-50 text-warning-700',
    danger: 'border-danger-200 bg-danger-50 text-danger-700',
  }

  return (
    <div className={clsx(
      'card border-2 transition-all duration-200 hover:shadow-md',
      colorClasses[color]
    )}>
      <div className="text-center">
        <h3 className="text-sm font-medium text-gray-600 mb-1">{title}</h3>
        <div className="text-2xl font-bold mb-1">{value}</div>
        <p className="text-xs text-gray-500">{subtitle}</p>
      </div>
    </div>
  )
}

export default BudgetSummaryCard 