import { describe, expect, it, beforeEach } from 'vitest'
import { AUTH_STORAGE_KEY, ACCESS_TOKEN_KEY, clearSession } from '@/store/authStorage'

// The suite runs in vitest's node environment (no jsdom installed), so provide
// the minimum of localStorage that authStorage touches.
class MemoryStorage {
  private store = new Map<string, string>()
  getItem(k: string) {
    return this.store.has(k) ? this.store.get(k)! : null
  }
  setItem(k: string, v: string) {
    this.store.set(k, String(v))
  }
  removeItem(k: string) {
    this.store.delete(k)
  }
  clear() {
    this.store.clear()
  }
}

beforeEach(() => {
  Object.defineProperty(globalThis, 'localStorage', {
    value: new MemoryStorage(),
    writable: true,
    configurable: true,
  })
})

describe('clearSession', () => {
  it('removes the persisted auth store as well as the raw token', () => {
    // Regression: the 401 handler removed only the access token. The persisted
    // store kept isAuthenticated:true, so on reload the router treated the user
    // as signed in, rendered the app, fired another unauthenticated request,
    // got a 401, redirected to /login — which bounced straight back. With a
    // 30-minute token lifetime this looped for every user on expiry.
    localStorage.setItem(ACCESS_TOKEN_KEY, 'stale.jwt.value')
    localStorage.setItem(
      AUTH_STORAGE_KEY,
      JSON.stringify({ state: { isAuthenticated: true, user: { id: 1 } }, version: 0 }),
    )

    clearSession()

    expect(localStorage.getItem(ACCESS_TOKEN_KEY)).toBeNull()
    expect(localStorage.getItem(AUTH_STORAGE_KEY)).toBeNull()
  })

  it('is safe to call when nothing is stored', () => {
    expect(() => clearSession()).not.toThrow()
    expect(localStorage.getItem(AUTH_STORAGE_KEY)).toBeNull()
    expect(localStorage.getItem(ACCESS_TOKEN_KEY)).toBeNull()
  })

  it('leaves the theme preference untouched', () => {
    // The UI store is not part of the session; logging out must not reset it.
    localStorage.setItem('genxchains-ui', JSON.stringify({ state: { theme: 'dark' } }))
    localStorage.setItem(ACCESS_TOKEN_KEY, 'x')

    clearSession()

    expect(localStorage.getItem('genxchains-ui')).not.toBeNull()
  })

  it('uses storage keys that match the auth store', () => {
    // If these drift from the persist `name`, the 401 handler silently stops
    // clearing the store and the redirect loop returns.
    expect(AUTH_STORAGE_KEY).toBe('genxchains-auth')
    expect(ACCESS_TOKEN_KEY).toBe('access_token')
  })
})
