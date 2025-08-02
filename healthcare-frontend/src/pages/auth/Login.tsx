import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { useForm } from 'react-hook-form';
import { Eye, EyeOff, Mail, Lock, Heart } from 'lucide-react';
import { toast } from 'react-toastify';
import { useAuthStore } from '../../store/authStore';
import { authAPI } from '../../services/api';

interface LoginForm {
  username: string;
  password: string;
}

const Login: React.FC = () => {
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const { login } = useAuthStore();
  const navigate = useNavigate();

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginForm>();

  const onSubmit = async (data: LoginForm) => {
    setIsLoading(true);
    try {
      const response = await authAPI.login(data);
      const { user, tokens } = response.data;
      
      login(user, tokens);
      toast.success('Welcome back!');
      navigate('/dashboard');
    } catch (error: any) {
      toast.error(error.response?.data?.message || 'Login failed. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen pt-16 flex items-center justify-center px-4">
      <div className="absolute inset-0 bg-gradient-to-br from-blue-900/30 via-purple-900/30 to-indigo-900/30"></div>
      
      {/* Floating Elements */}
      <div className="absolute top-20 left-10 w-20 h-20 bg-gradient-to-r from-pink-500 to-purple-500 rounded-full opacity-20 animate-bounce-slow"></div>
      <div className="absolute top-40 right-20 w-16 h-16 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-full opacity-30 animate-pulse-slow"></div>
      <div className="absolute bottom-20 left-20 w-24 h-24 bg-gradient-to-r from-green-500 to-emerald-500 rounded-full opacity-25 animate-bounce-slow"></div>

      <motion.div
        initial={{ opacity: 0, y: 20, scale: 0.95 }}
        animate={{ opacity: 1, y: 0, scale: 1 }}
        transition={{ duration: 0.6 }}
        className="relative w-full max-w-md"
      >
        <div className="glass rounded-2xl p-8 shadow-2xl border border-white border-opacity-20">
          {/* Header */}
          <div className="text-center mb-8">
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="inline-flex p-4 rounded-xl bg-gradient-to-r from-primary-500 to-secondary-500 mb-4"
            >
              <Heart className="h-8 w-8 text-white" />
            </motion.div>
            <h1 className="text-3xl font-bold text-white mb-2">Welcome Back</h1>
            <p className="text-white text-opacity-80">Sign in to your HealthCare+ account</p>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
            {/* Username Field */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.3 }}
            >
              <label htmlFor="username" className="block text-white font-medium mb-2">
                Username or Email
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Mail className="h-5 w-5 text-white text-opacity-50" />
                </div>
                <input
                  {...register('username', { required: 'Username is required' })}
                  type="text"
                  className="input-glass w-full pl-10 pr-4 py-3"
                  placeholder="Enter your username or email"
                />
              </div>
              {errors.username && (
                <p className="mt-1 text-red-400 text-sm">{errors.username.message}</p>
              )}
            </motion.div>

            {/* Password Field */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.4 }}
            >
              <label htmlFor="password" className="block text-white font-medium mb-2">
                Password
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Lock className="h-5 w-5 text-white text-opacity-50" />
                </div>
                <input
                  {...register('password', { required: 'Password is required' })}
                  type={showPassword ? 'text' : 'password'}
                  className="input-glass w-full pl-10 pr-12 py-3"
                  placeholder="Enter your password"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute inset-y-0 right-0 pr-3 flex items-center text-white text-opacity-50 hover:text-white transition-colors"
                >
                  {showPassword ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
                </button>
              </div>
              {errors.password && (
                <p className="mt-1 text-red-400 text-sm">{errors.password.message}</p>
              )}
            </motion.div>

            {/* Forgot Password */}
            <div className="text-right">
              <Link
                to="/forgot-password"
                className="text-white text-opacity-80 hover:text-white text-sm transition-colors"
              >
                Forgot your password?
              </Link>
            </div>

            {/* Submit Button */}
            <motion.button
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.5 }}
              type="submit"
              disabled={isLoading}
              className="w-full bg-gradient-to-r from-primary-500 to-secondary-500 text-white font-semibold py-3 px-6 rounded-lg shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
            >
              {isLoading ? (
                <div className="flex items-center justify-center space-x-2">
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                  <span>Signing In...</span>
                </div>
              ) : (
                'Sign In'
              )}
            </motion.button>
          </form>

          {/* Divider */}
          <div className="my-6 flex items-center">
            <div className="flex-1 border-t border-white border-opacity-20"></div>
            <span className="px-4 text-white text-opacity-60 text-sm">or</span>
            <div className="flex-1 border-t border-white border-opacity-20"></div>
          </div>

          {/* Sign Up Link */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.6, delay: 0.6 }}
            className="text-center"
          >
            <p className="text-white text-opacity-80">
              Don't have an account?{' '}
              <Link
                to="/signup"
                className="text-white font-semibold hover:text-opacity-80 transition-colors"
              >
                Sign up now
              </Link>
            </p>
          </motion.div>
        </div>
      </motion.div>
    </div>
  );
};

export default Login;