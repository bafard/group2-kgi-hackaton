import React, { useState } from 'react'
import { BrowserRouter, Routes, Route, Link, Navigate } from 'react-router-dom'
import { Upload, MessageCircle, FolderOpen, FileText, FileSpreadsheet, BarChart3, Users, Settings, LogOut, User } from 'lucide-react'
import { Button } from './components/ui/button'
import { toast } from './hooks/use-toast'
import { AuthProvider, useAuth } from './contexts/AuthContext'
import Layout from './components/Layout'
import ProtectedRoute from './components/ProtectedRoute'
import LoginPage from './pages/LoginPage'
import UploadList from './pages/UploadList'
import ManageSource from './pages/ManageSource'
import UploadKnowledge from './pages/UploadKnowledge'
import ChatAsk from './pages/ChatAsk'
import UserManagement from './pages/UserManagement'
import MaintainWearnessFormula from './pages/MaintainWearnessFormula'
import './App.css'

function HomePage() {
  const { user, hasRole } = useAuth();

  const handleUploadKnowledge = () => {
    toast.success('Navigating to Upload Knowledge...')
  }

  const handleAsk = () => {
    toast.success('Ask functionality activated...')
  }

  const handleAnalyzeData = () => {
    toast.success('Navigating to Data Analysis...')
  }

  const handleMaintainWearnessFormula = () => {
    toast.success('Navigating to Maintain Wearness Formula...')
  }

  const handleUserManagement = () => {
    toast.success('Navigating to User Management...')
  }

  const handleManageKnowledge = () => {
    toast.success('Navigating to Manage Knowledge...')
  }

  return (
    <div className="p-8">
      <div className="max-w-2xl mx-auto">
        <div className="bg-white rounded-lg shadow-xl p-8">
          {/* Welcome Message */}
          <div className="text-center mb-6">
            <h2 className="text-2xl font-bold text-gray-800">Welcome, {user?.fullName}!</h2>
            <p className="text-gray-600 capitalize">Role: {user?.role}</p>
          </div>

          {/* Main Action Buttons */}
          <div className="space-y-4 mb-8">
            {/* Chat - Available to all roles */}
            <Link to="/chat" className="block">
              <Button 
                onClick={handleAsk}
                className="komatsu-button w-full gap-2 text-lg px-6 py-4 h-auto"
              >
                <MessageCircle className="h-6 w-6" />
                Ask AI
              </Button>
            </Link>

            {/* Upload Knowledge - Admin and Analyst only */}
            {hasRole(['admin', 'analyst']) && (
              <Link to="/upload-knowledge" className="block">
                <Button 
                  onClick={handleUploadKnowledge}
                  className="komatsu-button w-full gap-2 text-lg px-6 py-4 h-auto"
                >
                  <FileSpreadsheet className="h-6 w-6" />
                  Upload Knowledge
                </Button>
              </Link>
            )}
            
            {/* Analyze Data - Admin and Analyst only */}
            {hasRole(['admin', 'analyst']) && (
              <Link to="/analyze" className="block">
                <Button 
                  onClick={handleAnalyzeData}
                  className="komatsu-button w-full gap-2 text-lg px-6 py-4 h-auto"
                >
                  <BarChart3 className="h-6 w-6" />
                  Analyze Data
                </Button>
              </Link>
            )}
            
            {/* Manage Knowledge - Admin and Analyst only */}
            {hasRole(['admin', 'analyst']) && (
              <Link to="/manage-knowledge" className="block">
                <Button 
                  onClick={handleManageKnowledge}
                  className="komatsu-button w-full gap-2 text-lg px-6 py-4 h-auto"
                >
                  <FolderOpen className="h-6 w-6" />
                  Manage Knowledge
                </Button>
              </Link>
            )}

            {/* Maintain Wearness Formula - Admin and Analyst only */}
            {hasRole(['admin', 'analyst']) && (
              <Link to="/maintain-wearness-formula" className="block">
                <Button 
                  onClick={handleMaintainWearnessFormula}
                  className="komatsu-button w-full gap-2 text-lg px-6 py-4 h-auto"
                >
                  <Settings className="h-6 w-6" />
                  Maintain Wearness Formula
                </Button>
              </Link>
            )}

            {/* User Management - Admin only */}
            {hasRole(['admin']) && (
              <Link to="/user-management" className="block">
                <Button 
                  onClick={handleUserManagement}
                  className="komatsu-button w-full gap-2 text-lg px-6 py-4 h-auto"
                >
                  <Users className="h-6 w-6" />
                  User Management
                </Button>
              </Link>
            )}

            {/* Show message for limited access users */}
            {hasRole(['user', 'viewer', 'operator']) && (
              <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
                <p className="text-sm text-blue-700 text-center">
                  Your current role ({user?.role}) has access to Chat functionality. 
                  Contact your administrator for additional permissions.
                </p>
              </div>
            )}
          </div>

        </div>
      </div>
    </div>
  )
}

function AppRoutes() {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-komatsu-yellow"></div>
          <p className="mt-4 text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  if (!user) {
    return <LoginPage />;
  }

  return (
    <Layout>
      <Routes>
        <Route path="/login" element={<Navigate to="/" replace />} />
        <Route 
          path="/" 
          element={
            <ProtectedRoute>
              <HomePage />
            </ProtectedRoute>
          } 
        />
        <Route 
          path="/files" 
          element={
            <ProtectedRoute allowedRoles={['admin', 'analyst']}>
              <UploadList />
            </ProtectedRoute>
          } 
        />
        <Route 
          path="/manage-knowledge" 
          element={
            <ProtectedRoute allowedRoles={['admin', 'analyst']}>
              <ManageSource />
            </ProtectedRoute>
          } 
        />
        <Route 
          path="/upload-knowledge" 
          element={
            <ProtectedRoute allowedRoles={['admin', 'analyst']}>
              <UploadKnowledge />
            </ProtectedRoute>
          } 
        />
        <Route 
          path="/chat" 
          element={
            <ProtectedRoute allowedRoles={['admin', 'analyst', 'operator', 'user', 'viewer']}>
              <ChatAsk />
            </ProtectedRoute>
          } 
        />
        <Route 
          path="/user-management" 
          element={
            <ProtectedRoute allowedRoles={['admin']}>
              <UserManagement />
            </ProtectedRoute>
          } 
        />
        <Route 
          path="/maintain-wearness-formula" 
          element={
            <ProtectedRoute allowedRoles={['admin', 'analyst']}>
              <MaintainWearnessFormula />
            </ProtectedRoute>
          } 
        />
      </Routes>
    </Layout>
  );
}

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <AppRoutes />
      </AuthProvider>
    </BrowserRouter>
  )
}

export default App