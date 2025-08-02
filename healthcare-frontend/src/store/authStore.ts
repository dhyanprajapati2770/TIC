import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  user_type: 'patient' | 'doctor' | 'admin' | 'pharmacist';
  phone_number?: string;
  date_of_birth?: string;
  address?: string;
  profile_picture?: string;
  is_verified: boolean;
}

interface AuthState {
  user: User | null;
  tokens: {
    access: string;
    refresh: string;
  } | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  
  // Actions
  setUser: (user: User) => void;
  setTokens: (tokens: { access: string; refresh: string }) => void;
  login: (user: User, tokens: { access: string; refresh: string }) => void;
  logout: () => void;
  setLoading: (loading: boolean) => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      tokens: null,
      isAuthenticated: false,
      isLoading: false,

      setUser: (user: User) =>
        set((state) => ({
          user,
          isAuthenticated: !!user,
        })),

      setTokens: (tokens: { access: string; refresh: string }) =>
        set((state) => ({
          tokens,
          isAuthenticated: !!tokens.access,
        })),

      login: (user: User, tokens: { access: string; refresh: string }) =>
        set((state) => ({
          user,
          tokens,
          isAuthenticated: true,
          isLoading: false,
        })),

      logout: () =>
        set((state) => ({
          user: null,
          tokens: null,
          isAuthenticated: false,
          isLoading: false,
        })),

      setLoading: (loading: boolean) =>
        set((state) => ({
          isLoading: loading,
        })),
    }),
    {
      name: 'healthcare-auth',
      partialize: (state) => ({
        user: state.user,
        tokens: state.tokens,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
);