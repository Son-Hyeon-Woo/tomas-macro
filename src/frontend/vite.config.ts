import { sveltekit } from '@sveltejs/kit/vite'
import { defineConfig } from 'vite'

export default defineConfig(({ mode }) => {
	// mode가 'development'일 때만 proxy 설정
	const devProxy =
		mode === 'development'
			? {
					'/eel.js': {
						target: 'http://localhost:8000',
						changeOrigin: true
					},
					'/eel': {
						// WebSocket 프록시 추가
						target: 'ws://localhost:8000',
						ws: true, // WebSocket 지원 활성화
						changeOrigin: true
					}
				}
			: undefined

	return {
		plugins: [sveltekit()],
		base: './',
		server: {
			proxy: devProxy
		}
	}
})
