import { createAuthStore } from '$lib/stores/auth'
import { get } from 'svelte/store'

interface LoginResponse {
	success: boolean
	message?: string
	token?: string
}

class AuthService {
	private authStore = createAuthStore()

	/**
	 * Generic login method that can be used for different login types
	 * @param type - Type of login (srt or ktx)
	 * @param credentials - Login credentials
	 * @param options - Additional login options
	 * @returns Promise with login result
	 */
	async login(type: 'srt' | 'ktx'): Promise<LoginResponse> {
		try {
			const srtId = get(this.authStore).srtId
			const srtPw = get(this.authStore).srtPw
			const ktxId = get(this.authStore).ktxId
			const ktxPw = get(this.authStore).ktxPw

			// Validate input
			if (type === 'srt') {
				if (srtId || srtPw) {
					return {
						success: false,
						message: 'ID and password are required'
					}
				}
			} else {
				if (ktxId || ktxPw) {
					return {
						success: false,
						message: 'ID and password are required'
					}
				}
			}

			let response
			if (type === 'srt') {
				// @ts-expect-error (eel 타입 무시)
				response = await window.eel.set_login(type.toUpperCase(), srtId, srtPw)()
			} else {
				// @ts-expect-error (eel 타입 무시)
				response = await window.eel.set_login(type.toUpperCase(), ktxId, ktxPw)()
			}
			console.log(response)

			if (response.success) {
				// Update store based on login type
				// if (type === 'srt') {
				// 	this.authStore.updateSrt({
				// 		srtId: credentials.id,
				// 		srtPw: credentials.password,
				// 		srtLastLoginAt: new Date().toISOString()
				// 	})
				// } else {
				// 	this.authStore.updateKtx({
				// 		ktxId: credentials.id,
				// 		ktxPw: credentials.password,
				// 		ktxLastLoginAt: new Date().toISOString()
				// 	})
				// }
				console.log(response)
				return response
			}

			return response
		} catch (error) {
			console.error(`${type.toUpperCase()} Login error:`, error)
			return {
				success: false,
				message: 'An unexpected error occurred during login'
			}
		}
	}

	/**
	 * Logout method
	 */
	logout(type: 'srt' | 'ktx'): void {
		// Remove stored token
		localStorage.removeItem(`${type}_auth_token`)

		// Update store to remove credentials
		if (type === 'srt') {
			this.authStore.updateSrt({
				srtId: '',
				srtPw: '',
				srtLastLoginAt: ''
			})
		} else {
			this.authStore.updateKtx({
				ktxId: '',
				ktxPw: '',
				ktxLastLoginAt: ''
			})
		}
	}

	/**
	 * Check if user is logged in for a specific type
	 */
	isLoggedIn(type: 'srt' | 'ktx'): boolean {
		let isLoggedIn = false
		this.authStore.subscribe((state) => {
			isLoggedIn = type === 'srt' ? !!state.srtId : !!state.ktxId
		})()
		return isLoggedIn
	}
}

// Export a singleton instance
export const authService = new AuthService()
