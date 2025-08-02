import React from 'react';
import { motion } from 'framer-motion';
import { Pill, AlertCircle } from 'lucide-react';

const MedicineSuggestion: React.FC = () => {
  return (
    <div className="min-h-screen pt-20 px-4">
      <div className="max-w-4xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-center mb-12"
        >
          <div className="inline-flex p-4 rounded-xl bg-gradient-to-r from-green-500 to-emerald-500 mb-6">
            <Pill className="h-12 w-12 text-white" />
          </div>
          <h1 className="text-4xl md:text-5xl font-bold text-white mb-4">
            Medicine Recommendations
          </h1>
          <p className="text-xl text-white text-opacity-80 max-w-2xl mx-auto">
            Get personalized medicine suggestions based on your symptoms and conditions.
          </p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="glass rounded-2xl p-8 shadow-2xl"
        >
          <div className="text-center py-20">
            <Pill className="h-16 w-16 text-white text-opacity-50 mx-auto mb-4" />
            <h3 className="text-2xl font-bold text-white mb-4">Coming Soon</h3>
            <p className="text-white text-opacity-80 mb-8">
              Our AI-powered medicine recommendation system is being developed to provide safe and effective treatment suggestions.
            </p>
            <div className="flex items-center justify-center space-x-2 text-warning-400">
              <AlertCircle className="h-5 w-5" />
              <span className="text-sm">This feature will be available soon</span>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default MedicineSuggestion;