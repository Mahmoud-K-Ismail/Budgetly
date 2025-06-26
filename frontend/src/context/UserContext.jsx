import { createContext, useContext, useState, useEffect } from 'react'
import { userAPI } from '../api/api'

const UserContext = createContext()

export const useUser = () => {
  const context = useContext(UserContext)
  if (!context) {
    throw new Error('useUser must be used within a UserProvider')
  }
  return context
}

export const UserProvider = ({ children }) => {
  const [currentUser, setCurrentUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Load user from localStorage on app start
    const savedUser = localStorage.getItem('currentUser')
    if (savedUser) {
      try {
        const user = JSON.parse(savedUser)
        setCurrentUser(user)
      } catch (error) {
        console.error('Error parsing saved user:', error)
        localStorage.removeItem('currentUser')
      }
    }
    setLoading(false)
  }, [])

  const login = async (userData) => {
    try {
      const response = await userAPI.createUser(userData)
      const user = response.data
      setCurrentUser(user)
      localStorage.setItem('currentUser', JSON.stringify(user))
      return user
    } catch (error) {
      throw error
    }
  }

  const logout = () => {
    setCurrentUser(null)
    localStorage.removeItem('currentUser')
  }

  const updateUser = async (userData) => {
    if (!currentUser) throw new Error('No user logged in')
    
    try {
      const response = await userAPI.updateUser(currentUser.id, userData)
      const updatedUser = response.data
      setCurrentUser(updatedUser)
      localStorage.setItem('currentUser', JSON.stringify(updatedUser))
      return updatedUser
    } catch (error) {
      throw error
    }
  }

  const value = {
    currentUser,
    setCurrentUser,
    loading,
    login,
    logout,
    updateUser,
  }

  return (
    <UserContext.Provider value={value}>
      {children}
    </UserContext.Provider>
  )
} 