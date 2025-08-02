import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

// Components
import Navbar from './components/layout/Navbar';
import Footer from './components/layout/Footer';

// Pages
import Home from './pages/Home';
import Login from './pages/auth/Login';
import Signup from './pages/auth/Signup';
import SymptomChecker from './pages/SymptomChecker';
import DiseaseResult from './pages/DiseaseResult';
import MedicineSuggestion from './pages/MedicineSuggestion';
import PharmacyStore from './pages/pharmacy/PharmacyStore';
import Cart from './pages/pharmacy/Cart';
import Checkout from './pages/pharmacy/Checkout';
import DoctorChat from './pages/DoctorChat';
import Dashboard from './pages/Dashboard';
import About from './pages/About';
import Contact from './pages/Contact';

// Store
import { useAuthStore } from './store/authStore';

function App() {
  const { user } = useAuthStore();

  return (
    <Router>
      <div className="min-h-screen bg-gradient-to-br from-blue-900 via-purple-900 to-indigo-900">
        <Navbar />
        
        <main className="flex-1">
          <Routes>
            {/* Public Routes */}
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/signup" element={<Signup />} />
            <Route path="/about" element={<About />} />
            <Route path="/contact" element={<Contact />} />
            
            {/* Protected Routes */}
            <Route path="/symptom-checker" element={<SymptomChecker />} />
            <Route path="/disease-result" element={<DiseaseResult />} />
            <Route path="/medicine-suggestion" element={<MedicineSuggestion />} />
            <Route path="/pharmacy" element={<PharmacyStore />} />
            <Route path="/cart" element={<Cart />} />
            <Route path="/checkout" element={<Checkout />} />
            <Route path="/doctor-chat" element={<DoctorChat />} />
            <Route path="/dashboard" element={<Dashboard />} />
          </Routes>
        </main>
        
        <Footer />
        
        {/* Toast Notifications */}
        <ToastContainer
          position="top-right"
          autoClose={5000}
          hideProgressBar={false}
          newestOnTop={false}
          closeOnClick
          rtl={false}
          pauseOnFocusLoss
          draggable
          pauseOnHover
          theme="dark"
          className="mt-16"
        />
      </div>
    </Router>
  );
}

export default App;
