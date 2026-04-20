import { createContext, useContext, useState, useEffect } from "react";
import { request } from "@api/axios";

const AuthContext = createContext();

export const AuthProvider = ({
  children
}) => {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const handleUnauthorized = () => {
      setUser(null)
      setLoading(false)
    }

    window.addEventListener('unauthorized', handleUnauthorized)

    const initAuth = async () => {
      try {
        const userData = await request('get', '/users/me')
        setUser(userData)
      } catch (e) {
        setUser(null)
      } finally {
        setLoading(false)
      }
    }

    initAuth()

    return () => {
      window.removeEventListener('unauthorized', handleUnauthorized)
    }
  }, [])

  const login = async (data) => {
    const res = await request('post', '/auth/login', data)
    setUser(res)
  }

  const logout = async () => {
    await request('post', '/auth/logout').catch(() => {})
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{
        user,
        loading,
        login,
        logout,
        isAuthenticated: !!user
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used inside AuthProvider')
  }
  return context
}