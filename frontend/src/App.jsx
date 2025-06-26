import { Routes, Route } from 'react-router-dom'
import { useState, useEffect } from 'react'
import Navbar from './components/Navbar'
import Dashboard from './pages/Dashboard'
import AddExpense from './pages/AddExpense'
import HistoryPage from './pages/History.jsx'
import Insights from './pages/Insights'
import { UserProvider } from './context/UserContext'
import { Toaster } from 'react-hot-toast'

function App() {
  const [currentUser, setCurrentUser] = useState(null)

  useEffect(() => {
    // Check if user exists in localStorage
    const savedUser = localStorage.getItem('currentUser')
    if (savedUser) {
      setCurrentUser(JSON.parse(savedUser))
    }
  }, [])

  return (
    <UserProvider value={{ currentUser, setCurrentUser }}>
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <main className="container mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/add-expense" element={<AddExpense />} />
            <Route path="/history" element={<HistoryPage />} />
            <Route path="/insights" element={<Insights />} />
          </Routes>
        </main>
        <Toaster 
          position="top-right"
          toastOptions={{
            duration: 4000,
            style: {
              background: '#363636',
              color: '#fff',
            },
            success: {
              duration: 3000,
              iconTheme: {
                primary: '#22c55e',
                secondary: '#fff',
              },
            },
            error: {
              duration: 5000,
              iconTheme: {
                primary: '#ef4444',
                secondary: '#fff',
              },
            },
          }}
        />
      </div>
    </UserProvider>
  )
}

export default App 