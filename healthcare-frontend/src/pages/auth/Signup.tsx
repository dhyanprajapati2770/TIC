import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { useForm } from 'react-hook-form';
import { Eye, EyeOff, Mail, Lock, User, Phone, Heart } from 'lucide-react';
import { toast } from 'react-toastify';
import { useAuthStore } from '../../store/authStore';
import { authAPI } from '../../services/api';

interface SignupForm {
  username: string;
  email: string;
  password: string;
  password_confirm: string;
  first_name: string;
  last_name: string;
  phone_number?: string;
  user_type: 'patient' | 'doctor';
}

const Signup: React.FC = () => {
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const { login } = useAuthStore();
  const navigate = useNavigate();

  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm<SignupForm>();

  const password = watch('password');

  const onSubmit = async (data: SignupForm) => {
    setIsLoading(true);
    try {
      const response = await authAPI.register(data);
      const { user, tokens } = response.data;
      
      login(user, tokens);
      toast.success('Account created successfully! Welcome to HealthCare+');
      navigate('/dashboard');
    } catch (error: any) {
      const errorMessage = error.response?.data?.message || 
                          error.response?.data?.error ||
                          'Registration failed. Please try again.';
      toast.error(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen pt-16 flex items-center justify-center px-4 py-8">
      <div className="absolute inset-0 bg-gradient-to-br from-blue-900/30 via-purple-900/30 to-indigo-900/30"></div>
      
      {/* Floating Elements */}
      <div className="absolute top-20 left-10 w-20 h-20 bg-gradient-to-r from-pink-500 to-purple-500 rounded-full opacity-20 animate-bounce-slow"></div>
      <div className="absolute top-40 right-20 w-16 h-16 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-full opacity-30 animate-pulse-slow"></div>
      <div className="absolute bottom-20 left-20 w-24 h-24 bg-gradient-to-r from-green-500 to-emerald-500 rounded-full opacity-25 animate-bounce-slow"></div>

      <motion.div
        initial={{ opacity: 0, y: 20, scale: 0.95 }}
        animate={{ opacity: 1, y: 0, scale: 1 }}
        transition={{ duration: 0.6 }}
        className="relative w-full max-w-2xl"
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
            <h1 className="text-3xl font-bold text-white mb-2">Join HealthCare+</h1>
            <p className="text-white text-opacity-80">Create your account and start your health journey</p>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
            {/* User Type Selection */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.3 }}
            >
              <label className="block text-white font-medium mb-3">I am a:</label>
              <div className="grid grid-cols-2 gap-4">
                <label className="relative">
                  <input
                    {...register('user_type', { required: 'Please select user type' })}
                    type="radio"
                    value="patient"
                    className="sr-only"
                  />
                  <div className="glass p-4 rounded-lg cursor-pointer border-2 border-transparent hover:border-white hover:border-opacity-30 transition-all duration-200">
                    <div className="flex items-center space-x-3">
                      <User className="h-5 w-5 text-white" />
                      <span className="text-white font-medium">Patient</span>
                    </div>
                  </div>
                </label>
                <label className="relative">
                  <input
                    {...register('user_type', { required: 'Please select user type' })}
                    type="radio"
                    value="doctor"
                    className="sr-only"
                  />
                  <div className="glass p-4 rounded-lg cursor-pointer border-2 border-transparent hover:border-white hover:border-opacity-30 transition-all duration-200">
                    <div className="flex items-center space-x-3">
                      <Heart className="h-5 w-5 text-white" />
                      <span className="text-white font-medium">Doctor</span>
                    </div>
                  </div>
                </label>
              </div>
              {errors.user_type && (
                <p className="mt-1 text-red-400 text-sm">{errors.user_type.message}</p>
              )}
            </motion.div>

            {/* Name Fields */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.6, delay: 0.4 }}
              >
                <label htmlFor="first_name" className="block text-white font-medium mb-2">
                  First Name
                </label>
                <input
                  {...register('first_name', { required: 'First name is required' })}
                  type="text"
                  className="input-glass w-full px-4 py-3"
                  placeholder="Enter your first name"
                />
                {errors.first_name && (
                  <p className="mt-1 text-red-400 text-sm">{errors.first_name.message}</p>
                )}
              </motion.div>

              <motion.div
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.6, delay: 0.4 }}
              >
                <label htmlFor="last_name" className="block text-white font-medium mb-2">
                  Last Name
                </label>
                <input
                  {...register('last_name', { required: 'Last name is required' })}
                  type="text"
                  className="input-glass w-full px-4 py-3"
                  placeholder="Enter your last name"
                />
                {errors.last_name && (
                  <p className="mt-1 text-red-400 text-sm">{errors.last_name.message}</p>
                )}
              </motion.div>
            </div>

            {/* Username and Email */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.6, delay: 0.5 }}
              >
                <label htmlFor="username" className="block text-white font-medium mb-2">
                  Username
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <User className="h-5 w-5 text-white text-opacity-50" />
                  </div>
                  <input
                    {...register('username', { 
                      required: 'Username is required',
                      minLength: { value: 3, message: 'Username must be at least 3 characters' }
                    })}
                    type="text"
                    className="input-glass w-full pl-10 pr-4 py-3"
                    placeholder="Choose a username"
                  />
                </div>
                {errors.username && (
                  <p className="mt-1 text-red-400 text-sm">{errors.username.message}</p>
                )}
              </motion.div>

              <motion.div
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.6, delay: 0.5 }}
              >
                <label htmlFor="email" className="block text-white font-medium mb-2">
                  Email Address
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <Mail className="h-5 w-5 text-white text-opacity-50" />
                  </div>
                  <input
                    {...register('email', { 
                      required: 'Email is required',
                      pattern: {
                        value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                        message: 'Invalid email address'
                      }
                    })}
                    type="email"
                    className="input-glass w-full pl-10 pr-4 py-3"
                    placeholder="Enter your email"
                  />
                </div>
                {errors.email && (
                  <p className="mt-1 text-red-400 text-sm">{errors.email.message}</p>
                )}
              </motion.div>
            </div>

            {/* Phone Number */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.6 }}
            >
              <label htmlFor="phone_number" className="block text-white font-medium mb-2">
                Phone Number (Optional)
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Phone className="h-5 w-5 text-white text-opacity-50" />
                </div>
                <input
                  {...register('phone_number')}
                  type="tel"
                  className="input-glass w-full pl-10 pr-4 py-3"
                  placeholder="Enter your phone number"
                />
              </div>
            </motion.div>

            {/* Password Fields */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.6, delay: 0.7 }}
              >
                <label htmlFor="password" className="block text-white font-medium mb-2">
                  Password
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <Lock className="h-5 w-5 text-white text-opacity-50" />
                  </div>
                  <input
                    {...register('password', { 
                      required: 'Password is required',
                      minLength: { value: 8, message: 'Password must be at least 8 characters' }
                    })}
                    type={showPassword ? 'text' : 'password'}
                    className="input-glass w-full pl-10 pr-12 py-3"
                    placeholder="Create a password"
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

              <motion.div
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.6, delay: 0.7 }}
              >
                <label htmlFor="password_confirm" className="block text-white font-medium mb-2">
                  Confirm Password
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <Lock className="h-5 w-5 text-white text-opacity-50" />
                  </div>
                  <input
                    {...register('password_confirm', { 
                      required: 'Please confirm your password',
                      validate: value => value === password || 'Passwords do not match'
                    })}
                    type={showConfirmPassword ? 'text' : 'password'}
                    className="input-glass w-full pl-10 pr-12 py-3"
                    placeholder="Confirm your password"
                  />
                  <button
                    type="button"
                    onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                    className="absolute inset-y-0 right-0 pr-3 flex items-center text-white text-opacity-50 hover:text-white transition-colors"
                  >
                    {showConfirmPassword ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
                  </button>
                </div>
                {errors.password_confirm && (
                  <p className="mt-1 text-red-400 text-sm">{errors.password_confirm.message}</p>
                )}
              </motion.div>
            </div>

            {/* Submit Button */}
            <motion.button
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.8 }}
              type="submit"
              disabled={isLoading}
              className="w-full bg-gradient-to-r from-primary-500 to-secondary-500 text-white font-semibold py-3 px-6 rounded-lg shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
            >
              {isLoading ? (
                <div className="flex items-center justify-center space-x-2">
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                  <span>Creating Account...</span>
                </div>
              ) : (
                'Create Account'
              )}
            </motion.button>
          </form>

          {/* Divider */}
          <div className="my-6 flex items-center">
            <div className="flex-1 border-t border-white border-opacity-20"></div>
            <span className="px-4 text-white text-opacity-60 text-sm">or</span>
            <div className="flex-1 border-t border-white border-opacity-20"></div>
          </div>

          {/* Login Link */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.6, delay: 0.9 }}
            className="text-center"
          >
            <p className="text-white text-opacity-80">
              Already have an account?{' '}
              <Link
                to="/login"
                className="text-white font-semibold hover:text-opacity-80 transition-colors"
              >
                Sign in here
              </Link>
            </p>
          </motion.div>
        </div>
      </motion.div>
    </div>
  );
};

export default Signup;