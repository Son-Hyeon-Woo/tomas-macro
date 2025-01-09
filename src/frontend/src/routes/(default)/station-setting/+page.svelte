<style>
</style>

<script lang="ts">
	import { onMount } from 'svelte'

	//👉 - 로컬에 저장된 로그인 정보 가져오기
	async function getLoginInfo() {
		try {
			// @ts-ignore (eel 타입 무시)
			const response = await window.eel.get_station('SRT')()
			console.log('get_station:', response)
			return response
		} catch (error) {
			console.error('Error:', error)
		}
	}

	let station = ''
	onMount(async () => {
		station = await getLoginInfo()
	})
</script>

<h1>기차역설정</h1>
{{ station }}
