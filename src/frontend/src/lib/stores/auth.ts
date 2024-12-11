import { writable } from 'svelte/store'

interface AuthState {
	isAuthenticated: boolean
}

const createAuthStore = () => {
	// eslint-disable-next-line @typescript-eslint/no-unused-vars
	const { subscribe, set, update } = writable<AuthState>({
		isAuthenticated: false
	})

	return {
		subscribe,
		login: () => {
			set({ isAuthenticated: true })
		},
		logout: () => {
			set({ isAuthenticated: false })
		}
	}
}

export const auth = createAuthStore()

//ℹ️ 페이지에서 api 호출 store 업데이트 (store에서는 상태관리에 집중)
//ℹ️ auth.ts - 스토어
// const createAuthStore = () => {
//   const { subscribe, set } = writable<AuthState>({
//     isAuthenticated: false,
//   });

//   return {
//     subscribe,
//     setAuth: (isAuthenticated: boolean) => {
//       set({ isAuthenticated });
//     }
//   };
// };

//ℹ️ page.svelte
// async function handleLogin(credentials: Credentials) {
//   try {
//     await api.login(credentials);
//     auth.setAuth(true);
//   } catch (error) {
//     // 에러 처리
//   }
// }

//ℹ️ - 인증관련 로직은 서비스레이어로 구분하여 재사용?
// services/authService.ts
// import { auth } from '../stores/auth';
// import type { Credentials } from '../types';

// class AuthService {
//   async login(credentials: Credentials) {
//     try {
//       const response = await api.login(credentials);
//       auth.setAuth(true);
//       return response;
//     } catch (error) {
//       // 에러 처리
//       throw error;
//     }
//   }

//   async logout() {
//     try {
//       await api.logout();
//       auth.setAuth(false);
//     } catch (error) {
//       throw error;
//     }
//   }
// }

// // 싱글톤 인스턴스로 export
// export const authService = new AuthService();
