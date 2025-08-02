import React from 'react';
import { Link } from 'react-router-dom';
import { Heart, Mail, Phone, MapPin } from 'lucide-react';

const Footer: React.FC = () => {
  return (
    <footer className="glass-dark border-t border-white border-opacity-20 mt-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand */}
          <div className="col-span-1 md:col-span-2">
            <div className="flex items-center space-x-2 mb-4">
              <div className="p-2 rounded-lg bg-gradient-to-r from-primary-500 to-secondary-500">
                <Heart className="h-6 w-6 text-white" />
              </div>
              <span className="text-xl font-bold text-white">HealthCare+</span>
            </div>
            <p className="text-white text-opacity-80 mb-4 max-w-md">
              Your comprehensive healthcare platform providing AI-powered symptom checking, 
              disease prediction, medicine recommendations, and 24/7 doctor consultations.
            </p>
            <div className="flex space-x-4">
              <div className="flex items-center space-x-2 text-white text-opacity-80">
                <Mail className="h-4 w-4" />
                <span>support@healthcare.com</span>
              </div>
              <div className="flex items-center space-x-2 text-white text-opacity-80">
                <Phone className="h-4 w-4" />
                <span>+1 (555) 123-4567</span>
              </div>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="text-white font-semibold mb-4">Quick Links</h3>
            <ul className="space-y-2">
              <li>
                <Link to="/symptom-checker" className="text-white text-opacity-80 hover:text-white transition-colors">
                  Symptom Checker
                </Link>
              </li>
              <li>
                <Link to="/pharmacy" className="text-white text-opacity-80 hover:text-white transition-colors">
                  Pharmacy
                </Link>
              </li>
              <li>
                <Link to="/doctor-chat" className="text-white text-opacity-80 hover:text-white transition-colors">
                  Doctor Chat
                </Link>
              </li>
              <li>
                <Link to="/about" className="text-white text-opacity-80 hover:text-white transition-colors">
                  About Us
                </Link>
              </li>
            </ul>
          </div>

          {/* Support */}
          <div>
            <h3 className="text-white font-semibold mb-4">Support</h3>
            <ul className="space-y-2">
              <li>
                <Link to="/contact" className="text-white text-opacity-80 hover:text-white transition-colors">
                  Contact Us
                </Link>
              </li>
              <li>
                <a href="#" className="text-white text-opacity-80 hover:text-white transition-colors">
                  Help Center
                </a>
              </li>
              <li>
                <a href="#" className="text-white text-opacity-80 hover:text-white transition-colors">
                  Privacy Policy
                </a>
              </li>
              <li>
                <a href="#" className="text-white text-opacity-80 hover:text-white transition-colors">
                  Terms of Service
                </a>
              </li>
            </ul>
          </div>
        </div>

        <div className="border-t border-white border-opacity-20 mt-8 pt-8 text-center">
          <p className="text-white text-opacity-60">
            © 2024 HealthCare+. All rights reserved. Built with ❤️ for better healthcare.
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;