import React from 'react';
import { motion } from 'framer-motion';
import { MessageCircle, AlertCircle } from 'lucide-react';

const DoctorChat: React.FC = () => {
  return (
    <div className="min-h-screen pt-20 px-4">
      <div className="max-w-4xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-center mb-12"
        >
          <div className="inline-flex p-4 rounded-xl bg-gradient-to-r from-purple-500 to-violet-500 mb-6">
            <MessageCircle className="h-12 w-12 text-white" />
          </div>
          <h1 className="text-4xl md:text-5xl font-bold text-white mb-4">
            Doctor Chat
          </h1>
          <p className="text-xl text-white text-opacity-80 max-w-2xl mx-auto">
            Connect with AI doctors and real physicians for instant health consultations.
          </p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="glass rounded-2xl p-8 shadow-2xl"
        >
          <div className="text-center py-20">
            <MessageCircle className="h-16 w-16 text-white text-opacity-50 mx-auto mb-4" />
            <h3 className="text-2xl font-bold text-white mb-4">Coming Soon</h3>
            <p className="text-white text-opacity-80 mb-8">
              Our 24/7 doctor chat feature with WebSocket support is being finalized for real-time consultations.
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

export default DoctorChat;