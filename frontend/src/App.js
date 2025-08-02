import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import { AuthProvider } from './contexts/AuthContext';
import { CartProvider } from './contexts/CartContext';

// Components
import Navbar from './components/Navbar';
import Footer from './components/Footer';

// Pages
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import SymptomChecker from './pages/SymptomChecker';
import DiseaseResult from './pages/DiseaseResult';
import MedicineSuggestion from './pages/MedicineSuggestion';
import Pharmacy from './pages/Pharmacy';
import DoctorChat from './pages/DoctorChat';
import Dashboard from './pages/Dashboard';
import Profile from './pages/Profile';
import Contact from './pages/Contact';
import About from './pages/About';

// Protected Route Component
import ProtectedRoute from './components/ProtectedRoute';

function App() {
  return (
    <AuthProvider>
      <CartProvider>
        <Router>
          <div className="min-h-screen bg-gray-50">
            <Navbar />
            <main className="pt-16">
              <Routes>
                {/* Public Routes */}
                <Route path="/" element={<Home />} />
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />
                <Route path="/about" element={<About />} />
                <Route path="/contact" element={<Contact />} />
                
                {/* Protected Routes */}
                <Route path="/symptom-checker" element={
                  <ProtectedRoute>
                    <SymptomChecker />
                  </ProtectedRoute>
                } />
                <Route path="/disease-result/:predictionId" element={
                  <ProtectedRoute>
                    <DiseaseResult />
                  </ProtectedRoute>
                } />
                <Route path="/medicine-suggestion" element={
                  <ProtectedRoute>
                    <MedicineSuggestion />
                  </ProtectedRoute>
                } />
                <Route path="/pharmacy" element={
                  <ProtectedRoute>
                    <Pharmacy />
                  </ProtectedRoute>
                } />
                <Route path="/doctor-chat" element={
                  <ProtectedRoute>
                    <DoctorChat />
                  </ProtectedRoute>
                } />
                <Route path="/dashboard" element={
                  <ProtectedRoute>
                    <Dashboard />
                  </ProtectedRoute>
                } />
                <Route path="/profile" element={
                  <ProtectedRoute>
                    <Profile />
                  </ProtectedRoute>
                } />
              </Routes>
            </main>
            <Footer />
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
        </Router>
      </CartProvider>
    </AuthProvider>
  );
}

export default App;