import axios from 'axios';
import { useAuthStore } from '../store/authStore';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const { tokens } = useAuthStore.getState();
    if (tokens?.access) {
      config.headers.Authorization = `Bearer ${tokens.access}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      const { tokens, logout, setTokens } = useAuthStore.getState();
      
      if (tokens?.refresh) {
        try {
          const response = await axios.post(`${API_BASE_URL}/auth/token/refresh/`, {
            refresh: tokens.refresh,
          });
          
          const newTokens = {
            access: response.data.access,
            refresh: tokens.refresh,
          };
          
          setTokens(newTokens);
          originalRequest.headers.Authorization = `Bearer ${newTokens.access}`;
          
          return api(originalRequest);
        } catch (refreshError) {
          logout();
          window.location.href = '/login';
        }
      } else {
        logout();
        window.location.href = '/login';
      }
    }
    
    return Promise.reject(error);
  }
);

export default api;

// Auth API endpoints
export const authAPI = {
  login: (credentials: { username: string; password: string }) =>
    api.post('/auth/login/', credentials),
  
  register: (userData: any) =>
    api.post('/auth/register/', userData),
  
  logout: (refreshToken: string) =>
    api.post('/auth/logout/', { refresh_token: refreshToken }),
  
  getProfile: () =>
    api.get('/auth/profile/'),
  
  updateProfile: (data: any) =>
    api.put('/auth/profile/', data),
};

// Symptom Checker API
export const symptomAPI = {
  getSymptoms: (params?: any) =>
    api.get('/symptoms/', { params }),
  
  getCategories: () =>
    api.get('/symptoms/categories/'),
  
  submitCheck: (data: any) =>
    api.post('/symptoms/check/', data),
  
  getHistory: () =>
    api.get('/symptoms/history/'),
  
  getCheckDetail: (id: number) =>
    api.get(`/symptoms/check/${id}/`),
};

// Disease Prediction API
export const diseaseAPI = {
  predict: (symptoms: any) =>
    api.post('/disease/predict/', symptoms),
  
  getConditionInfo: (condition: string) =>
    api.get(`/disease/condition/${condition}/`),
};

// Medicine API
export const medicineAPI = {
  getRecommendations: (data: any) =>
    api.post('/medicine/recommend/', data),
  
  checkInteractions: (medicines: string[]) =>
    api.post('/medicine/interactions/', { medicines }),
  
  searchMedicines: (query: string) =>
    api.get('/medicine/search/', { params: { q: query } }),
};

// Pharmacy API
export const pharmacyAPI = {
  getMedicines: (params?: any) =>
    api.get('/pharmacy/medicines/', { params }),
  
  getMedicine: (id: number) =>
    api.get(`/pharmacy/medicines/${id}/`),
  
  getCart: () =>
    api.get('/pharmacy/cart/'),
  
  addToCart: (medicineId: number, quantity: number) =>
    api.post('/pharmacy/cart/add/', { medicine_id: medicineId, quantity }),
  
  updateCartItem: (itemId: number, quantity: number) =>
    api.put(`/pharmacy/cart/items/${itemId}/`, { quantity }),
  
  removeFromCart: (itemId: number) =>
    api.delete(`/pharmacy/cart/items/${itemId}/`),
  
  checkout: (data: any) =>
    api.post('/pharmacy/checkout/', data),
  
  getOrders: () =>
    api.get('/pharmacy/orders/'),
  
  getOrder: (id: number) =>
    api.get(`/pharmacy/orders/${id}/`),
};

// Chat API
export const chatAPI = {
  getConsultations: () =>
    api.get('/chat/consultations/'),
  
  getConsultation: (id: number) =>
    api.get(`/chat/consultations/${id}/`),
  
  createConsultation: (data: any) =>
    api.post('/chat/consultations/', data),
  
  endConsultation: (id: number) =>
    api.post(`/chat/consultations/${id}/end/`),
  
  submitFeedback: (consultationId: number, feedback: any) =>
    api.post(`/chat/consultations/${consultationId}/feedback/`, feedback),
};

// Dashboard API
export const dashboardAPI = {
  getStats: () =>
    api.get('/dashboard/stats/'),
  
  getRecentActivity: () =>
    api.get('/dashboard/activity/'),
  
  getHealthMetrics: () =>
    api.get('/dashboard/health-metrics/'),
};