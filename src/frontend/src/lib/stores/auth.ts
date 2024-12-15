import { writable } from 'svelte/store'

export interface AuthState {
	srtId: string
	srtPw: string
	srtLastLoginAt: string
	ktxId: string
	ktxPw: string
	ktxLastLoginAt: string
}

const defaultAuthState: AuthState = {
	srtId: '',
	srtPw: '',
	srtLastLoginAt: '',
	ktxId: '',
	ktxPw: '',
	ktxLastLoginAt: ''
}

export function createAuthStore() {
	const { subscribe, set, update } = writable<AuthState>(defaultAuthState)

	return {
		subscribe,

		// Update entire auth state
		update: (newState: Partial<AuthState>) => {
			update((currentState) => ({
				...currentState,
				...newState
			}))
		},

		// Update specific properties
		updateSrt: (srtData: Partial<Pick<AuthState, 'srtId' | 'srtPw' | 'srtLastLoginAt'>>) => {
			update((currentState) => ({
				...currentState,
				...srtData
			}))
		},

		// Update specific KTX properties
		updateKtx: (ktxData: Partial<Pick<AuthState, 'ktxId' | 'ktxPw' | 'ktxLastLoginAt'>>) => {
			update((currentState) => ({
				...currentState,
				...ktxData
			}))
		},

		// Reset to default state
		reset: () => {
			set(defaultAuthState)
		},

		// Check if any login is currently active
		isLoggedIn: () => {
			return (state: AuthState) => !!state.srtId || !!state.ktxId
		}
	}
}
