import { writable } from 'svelte/store';

interface AuthState {
  isAuthenticated: boolean;
}

const createAuthStore = () => {
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const { subscribe, set, update } = writable<AuthState>({
      isAuthenticated: false,
    });
  
    return {
      subscribe,
      login: () => {
        set({ isAuthenticated: true});
      },
      logout: () => {
        set({ isAuthenticated: false});
      }
    };
  };
  
  export const auth = createAuthStore();