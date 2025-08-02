import React from 'react';
import { motion } from 'framer-motion';
import { Heart, Shield, Zap, Users } from 'lucide-react';

const About: React.FC = () => {
  const features = [
    {
      icon: Heart,
      title: 'Patient-Centered Care',
      description: 'We put your health and well-being at the center of everything we do.',
    },
    {
      icon: Shield,
      title: 'Privacy & Security',
      description: 'Your health data is protected with enterprise-grade security measures.',
    },
    {
      icon: Zap,
      title: 'AI-Powered Insights',
      description: 'Advanced machine learning provides accurate health predictions and recommendations.',
    },
    {
      icon: Users,
      title: 'Expert Network',
      description: 'Connect with qualified healthcare professionals and AI specialists.',
    },
  ];

  return (
    <div className="min-h-screen pt-20 px-4">
      <div className="max-w-6xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <h1 className="text-4xl md:text-6xl font-bold text-white mb-6">
            About <span className="text-lamborghini">HealthCare+</span>
          </h1>
          <p className="text-xl text-white text-opacity-80 max-w-3xl mx-auto">
            We're revolutionizing healthcare with AI-powered diagnostics, personalized treatment recommendations, 
            and seamless patient experiences.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-16">
          {features.map((feature, index) => (
            <motion.div
              key={feature.title}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
              className="glass rounded-2xl p-8 hover:scale-105 transition-all duration-300"
            >
              <div className="inline-flex p-4 rounded-xl bg-gradient-to-r from-primary-500 to-secondary-500 mb-6">
                <feature.icon className="h-8 w-8 text-white" />
              </div>
              <h3 className="text-2xl font-bold text-white mb-4">{feature.title}</h3>
              <p className="text-white text-opacity-80">{feature.description}</p>
            </motion.div>
          ))}
        </div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.4 }}
          className="glass rounded-2xl p-8 text-center"
        >
          <h2 className="text-3xl font-bold text-white mb-6">Our Mission</h2>
          <p className="text-xl text-white text-opacity-80 max-w-4xl mx-auto">
            To democratize healthcare by making high-quality medical insights, consultations, 
            and treatments accessible to everyone through cutting-edge technology and compassionate care.
          </p>
        </motion.div>
      </div>
    </div>
  );
};

export default About;