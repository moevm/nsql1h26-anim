import { Navigate } from 'react-router-dom';
import { useAuth } from '../../contexts';

export const ProtectedRoute = ({ children }) => {
  const { isAuthenticated } = useAuth();
  return isAuthenticated ? children : <Navigate to="/" replace />  
};