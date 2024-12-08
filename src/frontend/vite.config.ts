import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [sveltekit()],
	server: {
		proxy: {
		  '/eel.js': {
			target: 'http://localhost:8000', // Python Eel 서버 주소
			changeOrigin: true,
		  },
		},
	  },
});
