import React, { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Heart,
  Menu,
  X,
  User,
  ShoppingCart,
  MessageCircle,
  Activity,
  Pill,
  LogOut,
  Settings,
} from 'lucide-react';
import { useAuthStore } from '../../store/authStore';
import { toast } from 'react-toastify';

const Navbar: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [showUserMenu, setShowUserMenu] = useState(false);
  const { user, isAuthenticated, logout } = useAuthStore();
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    logout();
    toast.success('Logged out successfully');
    navigate('/');
    setShowUserMenu(false);
  };

  const navItems = [
    { name: 'Home', path: '/', icon: Heart },
    { name: 'Symptom Checker', path: '/symptom-checker', icon: Activity },
    { name: 'Pharmacy', path: '/pharmacy', icon: Pill },
    { name: 'Doctor Chat', path: '/doctor-chat', icon: MessageCircle },
  ];

  const isActivePath = (path: string) => location.pathname === path;

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 glass border-b border-white border-opacity-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2 group">
            <div className="p-2 rounded-lg bg-gradient-to-r from-primary-500 to-secondary-500 group-hover:scale-110 transition-transform duration-200">
              <Heart className="h-6 w-6 text-white" />
            </div>
            <span className="text-xl font-bold text-white text-lamborghini">
              HealthCare+
            </span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-1">
            {navItems.map((item) => (
              <Link
                key={item.name}
                to={item.path}
                className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-all duration-200 ${
                  isActivePath(item.path)
                    ? 'bg-white bg-opacity-20 text-white'
                    : 'text-white text-opacity-80 hover:bg-white hover:bg-opacity-10 hover:text-white'
                }`}
              >
                <item.icon className="h-4 w-4" />
                <span className="font-medium">{item.name}</span>
              </Link>
            ))}
          </div>

          {/* User Actions */}
          <div className="hidden md:flex items-center space-x-4">
            {isAuthenticated ? (
              <>
                {/* Cart Icon */}
                <Link
                  to="/cart"
                  className="p-2 rounded-lg text-white hover:bg-white hover:bg-opacity-10 transition-all duration-200 relative"
                >
                  <ShoppingCart className="h-5 w-5" />
                  <span className="absolute -top-1 -right-1 bg-danger-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center">
                    0
                  </span>
                </Link>

                {/* User Menu */}
                <div className="relative">
                  <button
                    onClick={() => setShowUserMenu(!showUserMenu)}
                    className="flex items-center space-x-2 p-2 rounded-lg text-white hover:bg-white hover:bg-opacity-10 transition-all duration-200"
                  >
                    <div className="w-8 h-8 rounded-full bg-gradient-to-r from-primary-500 to-secondary-500 flex items-center justify-center">
                      <User className="h-4 w-4 text-white" />
                    </div>
                    <span className="font-medium">{user?.first_name || user?.username}</span>
                  </button>

                  <AnimatePresence>
                    {showUserMenu && (
                      <motion.div
                        initial={{ opacity: 0, scale: 0.95, y: -10 }}
                        animate={{ opacity: 1, scale: 1, y: 0 }}
                        exit={{ opacity: 0, scale: 0.95, y: -10 }}
                        transition={{ duration: 0.2 }}
                        className="absolute right-0 mt-2 w-48 glass rounded-lg shadow-lg py-2"
                      >
                        <Link
                          to="/dashboard"
                          className="flex items-center space-x-2 px-4 py-2 text-white hover:bg-white hover:bg-opacity-10"
                          onClick={() => setShowUserMenu(false)}
                        >
                          <User className="h-4 w-4" />
                          <span>Dashboard</span>
                        </Link>
                        <Link
                          to="/settings"
                          className="flex items-center space-x-2 px-4 py-2 text-white hover:bg-white hover:bg-opacity-10"
                          onClick={() => setShowUserMenu(false)}
                        >
                          <Settings className="h-4 w-4" />
                          <span>Settings</span>
                        </Link>
                        <button
                          onClick={handleLogout}
                          className="flex items-center space-x-2 px-4 py-2 text-white hover:bg-white hover:bg-opacity-10 w-full text-left"
                        >
                          <LogOut className="h-4 w-4" />
                          <span>Logout</span>
                        </button>
                      </motion.div>
                    )}
                  </AnimatePresence>
                </div>
              </>
            ) : (
              <div className="flex items-center space-x-3">
                <Link
                  to="/login"
                  className="text-white hover:text-opacity-80 font-medium transition-colors duration-200"
                >
                  Login
                </Link>
                <Link
                  to="/signup"
                  className="btn-glass"
                >
                  Sign Up
                </Link>
              </div>
            )}
          </div>

          {/* Mobile menu button */}
          <button
            onClick={() => setIsOpen(!isOpen)}
            className="md:hidden p-2 rounded-lg text-white hover:bg-white hover:bg-opacity-10 transition-all duration-200"
          >
            {isOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
          </button>
        </div>
      </div>

      {/* Mobile Navigation */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.3 }}
            className="md:hidden glass-dark border-t border-white border-opacity-20"
          >
            <div className="px-4 py-4 space-y-2">
              {navItems.map((item) => (
                <Link
                  key={item.name}
                  to={item.path}
                  className={`flex items-center space-x-3 px-4 py-3 rounded-lg transition-all duration-200 ${
                    isActivePath(item.path)
                      ? 'bg-white bg-opacity-20 text-white'
                      : 'text-white text-opacity-80 hover:bg-white hover:bg-opacity-10 hover:text-white'
                  }`}
                  onClick={() => setIsOpen(false)}
                >
                  <item.icon className="h-5 w-5" />
                  <span className="font-medium">{item.name}</span>
                </Link>
              ))}

              {isAuthenticated ? (
                <>
                  <div className="border-t border-white border-opacity-20 my-4"></div>
                  <Link
                    to="/cart"
                    className="flex items-center space-x-3 px-4 py-3 rounded-lg text-white hover:bg-white hover:bg-opacity-10"
                    onClick={() => setIsOpen(false)}
                  >
                    <ShoppingCart className="h-5 w-5" />
                    <span className="font-medium">Cart</span>
                  </Link>
                  <Link
                    to="/dashboard"
                    className="flex items-center space-x-3 px-4 py-3 rounded-lg text-white hover:bg-white hover:bg-opacity-10"
                    onClick={() => setIsOpen(false)}
                  >
                    <User className="h-5 w-5" />
                    <span className="font-medium">Dashboard</span>
                  </Link>
                  <button
                    onClick={handleLogout}
                    className="flex items-center space-x-3 px-4 py-3 rounded-lg text-white hover:bg-white hover:bg-opacity-10 w-full text-left"
                  >
                    <LogOut className="h-5 w-5" />
                    <span className="font-medium">Logout</span>
                  </button>
                </>
              ) : (
                <>
                  <div className="border-t border-white border-opacity-20 my-4"></div>
                  <Link
                    to="/login"
                    className="flex items-center space-x-3 px-4 py-3 rounded-lg text-white hover:bg-white hover:bg-opacity-10"
                    onClick={() => setIsOpen(false)}
                  >
                    <User className="h-5 w-5" />
                    <span className="font-medium">Login</span>
                  </Link>
                  <Link
                    to="/signup"
                    className="flex items-center space-x-3 px-4 py-3 rounded-lg text-white hover:bg-white hover:bg-opacity-10"
                    onClick={() => setIsOpen(false)}
                  >
                    <User className="h-5 w-5" />
                    <span className="font-medium">Sign Up</span>
                  </Link>
                </>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </nav>
  );
};

export default Navbar;