import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { 
  Heart, 
  ShoppingCart, 
  User, 
  Menu, 
  X, 
  LogOut,
  Activity,
  Pill,
  MessageCircle,
  Home
} from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import { useCart } from '../contexts/CartContext';

const Navbar = () => {
  const { user, isAuthenticated, logout } = useAuth();
  const { getCartItemCount } = useCart();
  const navigate = useNavigate();
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/');
    setIsMenuOpen(false);
  };

  const navItems = [
    { name: 'Home', path: '/', icon: Home },
    { name: 'Symptom Checker', path: '/symptom-checker', icon: Activity, protected: true },
    { name: 'Pharmacy', path: '/pharmacy', icon: Pill, protected: true },
    { name: 'Doctor Chat', path: '/doctor-chat', icon: MessageCircle, protected: true },
    { name: 'Dashboard', path: '/dashboard', icon: User, protected: true },
  ];

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-white/90 backdrop-blur-md border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="flex items-center"
          >
            <Link to="/" className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-gradient-to-r from-primary-600 to-secondary-600 rounded-lg flex items-center justify-center">
                <Heart className="w-5 h-5 text-white" />
              </div>
              <span className="text-xl font-bold bg-gradient-to-r from-primary-600 to-secondary-600 bg-clip-text text-transparent">
                HealthCare
              </span>
            </Link>
          </motion.div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-8">
            {navItems.map((item) => {
              if (item.protected && !isAuthenticated) return null;
              return (
                <Link
                  key={item.name}
                  to={item.path}
                  className="flex items-center space-x-1 text-gray-700 hover:text-primary-600 transition-colors duration-200"
                >
                  <item.icon className="w-4 h-4" />
                  <span>{item.name}</span>
                </Link>
              );
            })}
          </div>

          {/* Right side items */}
          <div className="flex items-center space-x-4">
            {/* Cart Icon */}
            {isAuthenticated && (
              <Link
                to="/pharmacy"
                className="relative p-2 text-gray-700 hover:text-primary-600 transition-colors duration-200"
              >
                <ShoppingCart className="w-5 h-5" />
                {getCartItemCount() > 0 && (
                  <span className="absolute -top-1 -right-1 bg-primary-600 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                    {getCartItemCount()}
                  </span>
                )}
              </Link>
            )}

            {/* Auth Buttons */}
            {isAuthenticated ? (
              <div className="hidden md:flex items-center space-x-4">
                <span className="text-sm text-gray-600">
                  Welcome, {user?.first_name || user?.username}
                </span>
                <button
                  onClick={handleLogout}
                  className="flex items-center space-x-1 text-gray-700 hover:text-danger-600 transition-colors duration-200"
                >
                  <LogOut className="w-4 h-4" />
                  <span>Logout</span>
                </button>
              </div>
            ) : (
              <div className="hidden md:flex items-center space-x-4">
                <Link
                  to="/login"
                  className="text-gray-700 hover:text-primary-600 transition-colors duration-200"
                >
                  Login
                </Link>
                <Link
                  to="/register"
                  className="btn-primary"
                >
                  Register
                </Link>
              </div>
            )}

            {/* Mobile menu button */}
            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="md:hidden p-2 text-gray-700 hover:text-primary-600 transition-colors duration-200"
            >
              {isMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Menu */}
      {isMenuOpen && (
        <motion.div
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height: 'auto' }}
          exit={{ opacity: 0, height: 0 }}
          className="md:hidden bg-white border-t border-gray-200"
        >
          <div className="px-4 py-4 space-y-4">
            {navItems.map((item) => {
              if (item.protected && !isAuthenticated) return null;
              return (
                <Link
                  key={item.name}
                  to={item.path}
                  onClick={() => setIsMenuOpen(false)}
                  className="flex items-center space-x-3 text-gray-700 hover:text-primary-600 transition-colors duration-200 py-2"
                >
                  <item.icon className="w-5 h-5" />
                  <span>{item.name}</span>
                </Link>
              );
            })}
            
            {isAuthenticated ? (
              <div className="pt-4 border-t border-gray-200">
                <div className="text-sm text-gray-600 mb-4">
                  Welcome, {user?.first_name || user?.username}
                </div>
                <button
                  onClick={handleLogout}
                  className="flex items-center space-x-3 text-gray-700 hover:text-danger-600 transition-colors duration-200 py-2"
                >
                  <LogOut className="w-5 h-5" />
                  <span>Logout</span>
                </button>
              </div>
            ) : (
              <div className="pt-4 border-t border-gray-200 space-y-2">
                <Link
                  to="/login"
                  onClick={() => setIsMenuOpen(false)}
                  className="block text-gray-700 hover:text-primary-600 transition-colors duration-200 py-2"
                >
                  Login
                </Link>
                <Link
                  to="/register"
                  onClick={() => setIsMenuOpen(false)}
                  className="btn-primary block text-center"
                >
                  Register
                </Link>
              </div>
            )}
          </div>
        </motion.div>
      )}
    </nav>
  );
};

export default Navbar;