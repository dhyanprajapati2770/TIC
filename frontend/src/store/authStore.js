import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import axios from 'axios';
import toast from 'react-hot-toast';

const useAuthStore = create(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      isAuthenticated: false,
      isLoading: false,

      // Login
      login: async (username, password) => {
        set({ isLoading: true });
        try {
          const response = await axios.post('/api/token/', {
            username,
            password,
          });

          const { access, refresh } = response.data;
          
          // Set token in axios headers
          axios.defaults.headers.common['Authorization'] = `Bearer ${access}`;
          
          // Get user profile
          const userResponse = await axios.get('/api/users/profile/');
          
          set({
            user: userResponse.data,
            token: access,
            isAuthenticated: true,
            isLoading: false,
          });

          toast.success('Login successful!');
          return true;
        } catch (error) {
          set({ isLoading: false });
          toast.error(error.response?.data?.detail || 'Login failed');
          return false;
        }
      },

      // Register
      register: async (userData) => {
        set({ isLoading: true });
        try {
          const response = await axios.post('/api/users/register/', userData);
          
          const { tokens } = response.data;
          
          // Set token in axios headers
          axios.defaults.headers.common['Authorization'] = `Bearer ${tokens.access}`;
          
          set({
            user: response.data.user,
            token: tokens.access,
            isAuthenticated: true,
            isLoading: false,
          });

          toast.success('Registration successful!');
          return true;
        } catch (error) {
          set({ isLoading: false });
          toast.error(error.response?.data?.error || 'Registration failed');
          return false;
        }
      },

      // Logout
      logout: () => {
        // Remove token from axios headers
        delete axios.defaults.headers.common['Authorization'];
        
        set({
          user: null,
          token: null,
          isAuthenticated: false,
          isLoading: false,
        });

        toast.success('Logged out successfully');
      },

      // Update user profile
      updateProfile: async (profileData) => {
        try {
          const response = await axios.put('/api/users/profile/', profileData);
          
          set({
            user: response.data,
          });

          toast.success('Profile updated successfully');
          return true;
        } catch (error) {
          toast.error(error.response?.data?.error || 'Profile update failed');
          return false;
        }
      },

      // Initialize auth state
      initializeAuth: async () => {
        const { token } = get();
        if (token) {
          try {
            // Set token in axios headers
            axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
            
            // Verify token and get user profile
            const response = await axios.get('/api/users/profile/');
            
            set({
              user: response.data,
              isAuthenticated: true,
            });
          } catch (error) {
            // Token is invalid, clear auth state
            get().logout();
          }
        }
      },

      // Refresh token
      refreshToken: async () => {
        const { token } = get();
        if (token) {
          try {
            const response = await axios.post('/api/token/refresh/', {
              refresh: token,
            });

            const { access } = response.data;
            
            // Set new token in axios headers
            axios.defaults.headers.common['Authorization'] = `Bearer ${access}`;
            
            set({
              token: access,
            });
          } catch (error) {
            // Refresh failed, logout user
            get().logout();
          }
        }
      },
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({
        user: state.user,
        token: state.token,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
);

export { useAuthStore };