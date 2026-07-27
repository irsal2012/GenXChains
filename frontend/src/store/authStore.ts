import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import { authService } from '@/services/authService'
import type { User } from '@/types'
import toast from 'react-hot-toast'
import { ACCESS_TOKEN_KEY, AUTH_STORAGE_KEY, clearSession } from '@/store/authStorage'

interface AuthState {
  user: User | null
  token: string | null
  isAuthenticated: boolean
  isLoading: boolean

  login: (email: string, password: string) => Promise<void>
  logout: () => void
  fetchMe: () => Promise<void>
  setUser: (user: User) => void
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      isAuthenticated: false,
      isLoading: false,

      login: async (email, password) => {
        set({ isLoading: true })
        try {
          const res = await authService.login({ username: email, password })
          localStorage.setItem(ACCESS_TOKEN_KEY, res.access_token)
          set({
            token: res.access_token,
            user: res.user,
            isAuthenticated: true,
            isLoading: false,
          })
          toast.success(`Welcome back, ${res.user.full_name}!`)
        } catch {
          set({ isLoading: false })
          throw new Error('Login failed')
        }
      },

      logout: () => {
        clearSession()
        set({ user: null, token: null, isAuthenticated: false })
        toast.success('Logged out successfully')
      },

      fetchMe: async () => {
        const token = localStorage.getItem(ACCESS_TOKEN_KEY)
        if (!token) return
        try {
          const user = await authService.getMe()
          set({ user, isAuthenticated: true, token })
        } catch {
          get().logout()
        }
      },

      setUser: (user) => set({ user }),
    }),
    {
      name: AUTH_STORAGE_KEY,
      partialize: (state) => ({ token: state.token, user: state.user, isAuthenticated: state.isAuthenticated }),
    },
  ),
)
