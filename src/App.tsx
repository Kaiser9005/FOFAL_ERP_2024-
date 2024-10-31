import React from 'react'
import { Routes, Route } from 'react-router-dom'
import DashboardLayout from './components/layout/DashboardLayout'
import LoginPage from './components/auth/LoginPage'
import ProtectedRoute from './components/auth/ProtectedRoute'

const App: React.FC = () => {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route
        path="/*"
        element={
          <ProtectedRoute>
            <DashboardLayout />
          </ProtectedRoute>
        }
      />
    </Routes>
  )
}

export default App