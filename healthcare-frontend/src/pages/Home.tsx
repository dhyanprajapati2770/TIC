import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
  Activity,
  Brain,
  Pill,
  MessageCircle,
  ShoppingCart,
  Users,
  Clock,
  Shield,
  Zap,
  Heart,
  Stethoscope,
  Star,
} from 'lucide-react';

const Home: React.FC = () => {
  const features = [
    {
      icon: Activity,
      title: 'AI Symptom Checker',
      description: 'Advanced AI analyzes your symptoms and provides instant health insights.',
      color: 'from-red-500 to-pink-500',
    },
    {
      icon: Brain,
      title: 'Disease Prediction',
      description: 'Machine learning algorithms predict potential conditions based on symptoms.',
      color: 'from-blue-500 to-cyan-500',
    },
    {
      icon: Pill,
      title: 'Medicine Recommendations',
      description: 'Get personalized medicine suggestions based on your condition.',
      color: 'from-green-500 to-emerald-500',
    },
    {
      icon: MessageCircle,
      title: '24/7 Doctor Chat',
      description: 'Connect with AI doctors and real physicians anytime, anywhere.',
      color: 'from-purple-500 to-violet-500',
    },
    {
      icon: ShoppingCart,
      title: 'Online Pharmacy',
      description: 'Order medicines online with prescription verification and fast delivery.',
      color: 'from-orange-500 to-red-500',
    },
    {
      icon: Users,
      title: 'Health Dashboard',
      description: 'Track your health journey with comprehensive analytics and insights.',
      color: 'from-teal-500 to-blue-500',
    },
  ];

  const stats = [
    { icon: Users, value: '50K+', label: 'Happy Users' },
    { icon: Stethoscope, value: '500+', label: 'Expert Doctors' },
    { icon: Clock, value: '24/7', label: 'Support Available' },
    { icon: Star, value: '4.9', label: 'User Rating' },
  ];

  return (
    <div className="min-h-screen pt-16">
      {/* Hero Section */}
      <section className="relative overflow-hidden py-20 lg:py-32">
        <div className="absolute inset-0 bg-gradient-to-br from-blue-900/20 via-purple-900/20 to-indigo-900/20"></div>
        
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="text-center"
          >
            <motion.h1
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.2 }}
              className="text-4xl md:text-6xl lg:text-7xl font-bold text-white mb-6"
            >
              Your Health,{' '}
              <span className="text-lamborghini bg-gradient-to-r from-pink-500 via-purple-500 to-blue-500 bg-clip-text text-transparent">
                Reimagined
              </span>
            </motion.h1>
            
            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.4 }}
              className="text-xl md:text-2xl text-white text-opacity-90 mb-8 max-w-3xl mx-auto"
            >
              Experience the future of healthcare with AI-powered diagnostics, 
              instant doctor consultations, and personalized treatment recommendations.
            </motion.p>
            
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.6 }}
              className="flex flex-col sm:flex-row gap-4 justify-center items-center"
            >
              <Link
                to="/symptom-checker"
                className="group relative px-8 py-4 bg-gradient-to-r from-pink-500 to-purple-600 text-white font-semibold rounded-xl shadow-2xl hover:shadow-pink-500/25 transform hover:scale-105 transition-all duration-300 overflow-hidden"
              >
                <div className="absolute inset-0 bg-gradient-to-r from-pink-600 to-purple-700 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                <div className="relative flex items-center space-x-2">
                  <Activity className="h-5 w-5" />
                  <span>Check Symptoms Now</span>
                </div>
              </Link>
              
              <Link
                to="/doctor-chat"
                className="group px-8 py-4 glass text-white font-semibold rounded-xl hover:bg-white hover:bg-opacity-20 transition-all duration-300 flex items-center space-x-2"
              >
                <MessageCircle className="h-5 w-5" />
                <span>Talk to Doctor</span>
              </Link>
            </motion.div>
          </motion.div>
        </div>

        {/* Floating Elements */}
        <div className="absolute top-20 left-10 w-20 h-20 bg-gradient-to-r from-pink-500 to-purple-500 rounded-full opacity-20 animate-bounce-slow"></div>
        <div className="absolute top-40 right-20 w-16 h-16 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-full opacity-30 animate-pulse-slow"></div>
        <div className="absolute bottom-20 left-20 w-24 h-24 bg-gradient-to-r from-green-500 to-emerald-500 rounded-full opacity-25 animate-bounce-slow"></div>
      </section>

      {/* Features Section */}
      <section className="py-20 relative">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-3xl md:text-5xl font-bold text-white mb-6">
              Powerful Features for{' '}
              <span className="text-lamborghini">Modern Healthcare</span>
            </h2>
            <p className="text-xl text-white text-opacity-80 max-w-3xl mx-auto">
              Discover our comprehensive suite of AI-powered healthcare tools designed to 
              revolutionize your health management experience.
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                viewport={{ once: true }}
                className="group card-glass p-8 hover:scale-105 transition-all duration-300"
              >
                <div className={`inline-flex p-4 rounded-xl bg-gradient-to-r ${feature.color} mb-6 group-hover:scale-110 transition-transform duration-300`}>
                  <feature.icon className="h-8 w-8 text-white" />
                </div>
                <h3 className="text-xl font-bold text-white mb-4">{feature.title}</h3>
                <p className="text-white text-opacity-80">{feature.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-20 glass-dark">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {stats.map((stat, index) => (
              <motion.div
                key={stat.label}
                initial={{ opacity: 0, scale: 0.8 }}
                whileInView={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                viewport={{ once: true }}
                className="text-center"
              >
                <div className="inline-flex p-4 rounded-xl bg-gradient-to-r from-primary-500 to-secondary-500 mb-4">
                  <stat.icon className="h-8 w-8 text-white" />
                </div>
                <div className="text-3xl md:text-4xl font-bold text-white mb-2">{stat.value}</div>
                <div className="text-white text-opacity-80">{stat.label}</div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-pink-500/20 via-purple-500/20 to-blue-500/20"></div>
        
        <div className="relative max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
          >
            <h2 className="text-3xl md:text-5xl font-bold text-white mb-6">
              Ready to Transform Your{' '}
              <span className="text-lamborghini">Health Journey?</span>
            </h2>
            <p className="text-xl text-white text-opacity-90 mb-8">
              Join thousands of users who trust HealthCare+ for their health management needs.
            </p>
            <Link
              to="/signup"
              className="inline-flex items-center space-x-2 px-8 py-4 bg-gradient-to-r from-green-500 to-emerald-600 text-white font-semibold rounded-xl shadow-2xl hover:shadow-green-500/25 transform hover:scale-105 transition-all duration-300"
            >
              <Heart className="h-5 w-5" />
              <span>Get Started Today</span>
            </Link>
          </motion.div>
        </div>
      </section>
    </div>
  );
};

export default Home;