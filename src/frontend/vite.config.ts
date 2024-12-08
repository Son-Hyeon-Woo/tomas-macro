import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig(({ mode }) => {
	// mode가 'development'일 때만 proxy 설정
	const devProxy = mode === 'development' ? {
	  '/eel.js': {
		target: 'http://localhost:8000',
		changeOrigin: true,
	  }
	} : undefined;
  
	return {
	  plugins: [sveltekit()],
	  server: {
		proxy: devProxy
	  }
	};
  });
