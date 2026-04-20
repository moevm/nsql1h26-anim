import { Navigate } from "react-router-dom"
import { useAuth } from "../../contexts"

export const PublicRoute = ({ children }) => {
  const { isAuthenticated, loading} = useAuth()

  if (loading) {
    return null
  }

  if (isAuthenticated) {
    return <Navigate to="/" replace />
  }

  return children
}