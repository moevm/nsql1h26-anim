import { LoginPage } from "./pages/login/LoginPage";
import { RegisterPage } from "./pages/register/RegisterPage";
import { FeedPage } from "@pages/feed/FeedPage";
import { Routes, Route, Navigate } from "react-router-dom";
import { ProtectedRoute, PublicRoute } from "./components/route";
import { useAuth } from "./contexts";

export const App = () => { 
  const { loading, isAuthenticated } = useAuth()
  if (loading) {
    return <div>Загрузка...</div>
  }

  return (
    <Routes>
      <Route 
        path="/" 
        element={<Navigate to={isAuthenticated ? "/feed" : "/login"} replace />} 
      />
      <Route 
        path="/login" 
        element={
          <PublicRoute>
            <LoginPage/>
          </PublicRoute>
        } 
      />

      <Route 
        path="/register" 
        element={
          <PublicRoute>
            <RegisterPage/>
          </PublicRoute>
        } 
      />
      <Route 
        path="/feed" 
        element={
          <ProtectedRoute>
            <FeedPage/>
          </ProtectedRoute>
        }
      />
    </Routes>
  )
}