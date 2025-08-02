import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { 
  Heart, 
  Stethoscope, 
  Pill, 
  MessageCircle, 
  Shield, 
  Zap,
  Users,
  Award,
  ArrowRight,
  CheckCircle
} from 'lucide-react';

const Home = () => {
  const features = [
    {
      icon: Stethoscope,
      title: 'Symptom Checker',
      description: 'Get instant health insights by checking your symptoms with our AI-powered diagnostic tool.',
      color: 'from-blue-500 to-blue-600',
    },
    {
      icon: Heart,
      title: 'Disease Predictor',
      description: 'Advanced ML algorithms predict potential diseases based on your symptoms and health data.',
      color: 'from-red-500 to-red-600',
    },
    {
      icon: Pill,
      title: 'Medicine Store',
      description: 'Browse and purchase medicines with detailed information and professional recommendations.',
      color: 'from-green-500 to-green-600',
    },
    {
      icon: MessageCircle,
      title: 'Doctor Chatbot',
      description: '24/7 virtual doctor consultation with real-time chat support for your health queries.',
      color: 'from-purple-500 to-purple-600',
    },
  ];

  const benefits = [
    'AI-powered symptom analysis',
    'Real-time disease prediction',
    'Professional medicine recommendations',
    '24/7 virtual doctor support',
    'Secure health data management',
    'Mobile-responsive design',
  ];

  return (
    <div className="pt-16">
      {/* Hero Section */}
      <section className="relative bg-gradient-to-br from-primary-50 to-secondary-50 py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <motion.div
              initial={{ opacity: 0, x: -50 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6 }}
            >
              <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
                Your Health,{' '}
                <span className="text-gradient">Our Priority</span>
              </h1>
              <p className="text-xl text-gray-600 mb-8">
                Experience the future of healthcare with our comprehensive platform. 
                Get instant symptom analysis, disease predictions, and professional 
                medical guidance all in one place.
              </p>
              <div className="flex flex-col sm:flex-row gap-4">
                <Link
                  to="/symptom-checker"
                  className="btn-primary text-lg px-8 py-3 flex items-center justify-center space-x-2"
                >
                  <span>Start Symptom Check</span>
                  <ArrowRight className="w-5 h-5" />
                </Link>
                <Link
                  to="/signup"
                  className="btn-outline text-lg px-8 py-3"
                >
                  Get Started Free
                </Link>
              </div>
            </motion.div>
            
            <motion.div
              initial={{ opacity: 0, x: 50 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="relative"
            >
              <div className="glass p-8 rounded-2xl">
                <div className="grid grid-cols-2 gap-4">
                  {features.slice(0, 4).map((feature, index) => {
                    const Icon = feature.icon;
                    return (
                      <motion.div
                        key={feature.title}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.4, delay: 0.3 + index * 0.1 }}
                        className="text-center p-4 rounded-lg bg-white/50"
                      >
                        <div className={`w-12 h-12 bg-gradient-to-r ${feature.color} rounded-lg flex items-center justify-center mx-auto mb-3`}>
                          <Icon className="w-6 h-6 text-white" />
                        </div>
                        <h3 className="font-semibold text-gray-900 mb-1">{feature.title}</h3>
                        <p className="text-sm text-gray-600">{feature.description}</p>
                      </motion.div>
                    );
                  })}
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Comprehensive Healthcare Solutions
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Our platform combines cutting-edge technology with medical expertise 
              to provide you with the best healthcare experience.
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => {
              const Icon = feature.icon;
              return (
                <motion.div
                  key={feature.title}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.4, delay: index * 0.1 }}
                  viewport={{ once: true }}
                  className="card-hover text-center"
                >
                  <div className={`w-16 h-16 bg-gradient-to-r ${feature.color} rounded-xl flex items-center justify-center mx-auto mb-6`}>
                    <Icon className="w-8 h-8 text-white" />
                  </div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-3">{feature.title}</h3>
                  <p className="text-gray-600">{feature.description}</p>
                </motion.div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Benefits Section */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <motion.div
              initial={{ opacity: 0, x: -50 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6 }}
              viewport={{ once: true }}
            >
              <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-6">
                Why Choose HealthCare Pro?
              </h2>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {benefits.map((benefit, index) => (
                  <motion.div
                    key={benefit}
                    initial={{ opacity: 0, x: -20 }}
                    whileInView={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.4, delay: index * 0.1 }}
                    viewport={{ once: true }}
                    className="flex items-center space-x-3"
                  >
                    <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0" />
                    <span className="text-gray-700">{benefit}</span>
                  </motion.div>
                ))}
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, x: 50 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              viewport={{ once: true }}
              className="relative"
            >
              <div className="glass p-8 rounded-2xl">
                <div className="grid grid-cols-3 gap-6 text-center">
                  <div>
                    <div className="text-3xl font-bold text-primary-600 mb-2">10K+</div>
                    <div className="text-sm text-gray-600">Happy Users</div>
                  </div>
                  <div>
                    <div className="text-3xl font-bold text-secondary-600 mb-2">99%</div>
                    <div className="text-sm text-gray-600">Accuracy Rate</div>
                  </div>
                  <div>
                    <div className="text-3xl font-bold text-accent-600 mb-2">24/7</div>
                    <div className="text-sm text-gray-600">Support Available</div>
                  </div>
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-primary-600 to-secondary-600">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
          >
            <h2 className="text-3xl md:text-4xl font-bold text-white mb-6">
              Ready to Take Control of Your Health?
            </h2>
            <p className="text-xl text-primary-100 mb-8 max-w-2xl mx-auto">
              Join thousands of users who trust HealthCare Pro for their healthcare needs. 
              Start your journey to better health today.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                to="/signup"
                className="bg-white text-primary-600 hover:bg-gray-100 font-semibold py-3 px-8 rounded-lg transition-colors duration-200"
              >
                Get Started Free
              </Link>
              <Link
                to="/symptom-checker"
                className="border-2 border-white text-white hover:bg-white hover:text-primary-600 font-semibold py-3 px-8 rounded-lg transition-colors duration-200"
              >
                Try Symptom Checker
              </Link>
            </div>
          </motion.div>
        </div>
      </section>
    </div>
  );
};

export default Home;