/**
 * Storage keys for the persisted session.
 *
 * Kept in a dependency-free module because both the auth store and the axios
 * interceptor need them. Importing the store into the interceptor would create
 * a cycle (authStore -> authService -> api -> authStore).
 */
export const AUTH_STORAGE_KEY = 'genxchains-auth'
export const ACCESS_TOKEN_KEY = 'access_token'

/**
 * Clear every trace of the session.
 *
 * Removing only the access token is not enough: the persisted store also holds
 * `isAuthenticated: true`, and on the next load the router would treat the user
 * as signed in, render the app, fire an unauthenticated request, get a 401 and
 * redirect back to /login — which bounces straight back again. Both must go.
 */
export function clearSession(): void {
  localStorage.removeItem(ACCESS_TOKEN_KEY)
  localStorage.removeItem(AUTH_STORAGE_KEY)
}
