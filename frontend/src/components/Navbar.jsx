import { Link, useLocation } from 'react-router-dom'
import { useUser } from '../context/UserContext'
import { Wallet, Plus, History, TrendingUp, LogOut, ListTodo } from 'lucide-react'

const Navbar = () => {
  const { currentUser, logout } = useUser()
  const location = useLocation()

  const navItems = [
    { path: '/', label: 'Dashboard', icon: Wallet },
    { path: '/add-expense', label: 'Add Expense', icon: Plus },
    { path: '/history', label: 'History', icon: History },
    { path: '/insights', label: 'Insights', icon: TrendingUp },
    { path: '/wishlist', label: 'Wishlist', icon: ListTodo },
  ]

  const isActive = (path) => location.pathname === path

  return (
    <nav className="bg-white shadow-sm border-b border-gray-200">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-gradient-to-br from-nyuad-500 to-primary-600 rounded-lg flex items-center justify-center">
              <Wallet className="w-5 h-5 text-white" />
            </div>
            <span className="text-xl font-bold text-gradient">NYUAD Budgetly</span>
          </Link>

          {/* Navigation Links */}
          {currentUser && (
            <div className="hidden md:flex items-center space-x-1">
              {navItems.map((item) => {
                const Icon = item.icon
                return (
                  <Link
                    key={item.path}
                    to={item.path}
                    className={`flex items-center space-x-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors duration-200 ${
                      isActive(item.path)
                        ? 'bg-nyuad-50 text-nyuad-700 border border-nyuad-200'
                        : 'text-gray-600 hover:text-nyuad-600 hover:bg-gray-50'
                    }`}
                  >
                    <Icon className="w-4 h-4" />
                    <span>{item.label}</span>
                  </Link>
                )
              })}
            </div>
          )}

          {/* User Menu */}
          <div className="flex items-center space-x-4">
            {currentUser ? (
              <>
                <div className="hidden md:flex items-center space-x-2 text-sm text-gray-600">
                  <span>Welcome,</span>
                  <span className="font-medium text-nyuad-600">
                    ${currentUser.stipend.toLocaleString()}/month
                  </span>
                </div>
                <button
                  onClick={logout}
                  className="flex items-center space-x-2 px-3 py-2 text-sm text-gray-600 hover:text-danger-600 hover:bg-red-50 rounded-lg transition-colors duration-200"
                >
                  <LogOut className="w-4 h-4" />
                  <span className="hidden sm:inline">Logout</span>
                </button>
              </>
            ) : (
              <div className="text-sm text-gray-500">
                Please set up your profile
              </div>
            )}
          </div>
        </div>

        {/* Mobile Navigation */}
        {currentUser && (
          <div className="md:hidden border-t border-gray-200 py-2">
            <div className="flex justify-around">
              {navItems.map((item) => {
                const Icon = item.icon
                return (
                  <Link
                    key={item.path}
                    to={item.path}
                    className={`flex flex-col items-center space-y-1 px-3 py-2 rounded-lg text-xs font-medium transition-colors duration-200 ${
                      isActive(item.path)
                        ? 'text-nyuad-600 bg-nyuad-50'
                        : 'text-gray-600 hover:text-nyuad-600'
                    }`}
                  >
                    <Icon className="w-5 h-5" />
                    <span>{item.label}</span>
                  </Link>
                )
              })}
            </div>
          </div>
        )}
      </div>
    </nav>
  )
}

export default Navbar 