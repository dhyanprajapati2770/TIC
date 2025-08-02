import React from 'react';
import { motion } from 'framer-motion';
import { Mail, Phone, MapPin, MessageCircle } from 'lucide-react';

const Contact: React.FC = () => {
  const contactInfo = [
    {
      icon: Mail,
      title: 'Email Us',
      info: 'support@healthcare.com',
      description: 'Send us an email anytime',
    },
    {
      icon: Phone,
      title: 'Call Us',
      info: '+1 (555) 123-4567',
      description: '24/7 support hotline',
    },
    {
      icon: MapPin,
      title: 'Visit Us',
      info: '123 Healthcare Ave, Medical District',
      description: 'Our headquarters',
    },
    {
      icon: MessageCircle,
      title: 'Live Chat',
      info: 'Available 24/7',
      description: 'Instant support chat',
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
            Contact <span className="text-lamborghini">Us</span>
          </h1>
          <p className="text-xl text-white text-opacity-80 max-w-3xl mx-auto">
            Get in touch with our team. We're here to help you with any questions about your health journey.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-16">
          {contactInfo.map((contact, index) => (
            <motion.div
              key={contact.title}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
              className="glass rounded-2xl p-6 text-center hover:scale-105 transition-all duration-300"
            >
              <div className="inline-flex p-4 rounded-xl bg-gradient-to-r from-primary-500 to-secondary-500 mb-4">
                <contact.icon className="h-6 w-6 text-white" />
              </div>
              <h3 className="text-lg font-bold text-white mb-2">{contact.title}</h3>
              <p className="text-white font-medium mb-1">{contact.info}</p>
              <p className="text-white text-opacity-60 text-sm">{contact.description}</p>
            </motion.div>
          ))}
        </div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.4 }}
          className="glass rounded-2xl p-8"
        >
          <div className="max-w-2xl mx-auto">
            <h2 className="text-3xl font-bold text-white mb-6 text-center">Send us a Message</h2>
            <form className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-white font-medium mb-2">Name</label>
                  <input
                    type="text"
                    className="input-glass w-full px-4 py-3"
                    placeholder="Your full name"
                  />
                </div>
                <div>
                  <label className="block text-white font-medium mb-2">Email</label>
                  <input
                    type="email"
                    className="input-glass w-full px-4 py-3"
                    placeholder="your@email.com"
                  />
                </div>
              </div>
              <div>
                <label className="block text-white font-medium mb-2">Subject</label>
                <input
                  type="text"
                  className="input-glass w-full px-4 py-3"
                  placeholder="How can we help you?"
                />
              </div>
              <div>
                <label className="block text-white font-medium mb-2">Message</label>
                <textarea
                  rows={6}
                  className="input-glass w-full px-4 py-3 resize-none"
                  placeholder="Tell us more about your inquiry..."
                ></textarea>
              </div>
              <button
                type="submit"
                className="w-full bg-gradient-to-r from-primary-500 to-secondary-500 text-white font-semibold py-3 px-6 rounded-lg shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200"
              >
                Send Message
              </button>
            </form>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default Contact;