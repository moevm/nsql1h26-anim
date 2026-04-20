import { createRoot } from 'react-dom/client'
import './styles/index.css'
import { BrowserRouter } from 'react-router'
import { AuthProvider } from './contexts'
import { App } from './App.jsx'

createRoot(document.getElementById('root')).render(
  <BrowserRouter>
    <AuthProvider>
      <App/>
    </AuthProvider>
  </BrowserRouter>
)
