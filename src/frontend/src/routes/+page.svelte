<script lang="ts">
	import Counter from './Counter.svelte';
	import { onMount } from 'svelte';
	import { Button } from '$lib/components/ui/button';

	let count = 0;

	function test() {
		count++;
		console.log('test');
	}

	let systemInfo: any = null;
	// eel 함수 호출
	async function getSystemInfo() {
		console.log('getSystemInfo'); // @ts-ignore (eel 타입 무시)
		// @ts-ignore (eel 타입 무시)
		console.log(window.eel);
		try {
			// @ts-ignore (eel 타입 무시)
			const info = await window.eel.get_system_info()();
			systemInfo = info;
			console.log('System Info:', info);
		} catch (error) {
			console.error('Error:', error);
		}
	}
</script>

<svelte:head>
	<title>Home</title>
	<meta name="description" content="Svelte demo app" />
</svelte:head>

<section>
	<Button on:click={test}>Click me</Button>
	<p>click count: {count}</p>

	<Button on:click={getSystemInfo}>Get System Info</Button>
	<p>System Info: {JSON.stringify(systemInfo)}</p>

	<Counter />
</section>

<style>
	section {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		flex: 0.6;
	}
</style>
