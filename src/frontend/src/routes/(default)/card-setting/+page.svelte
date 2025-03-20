<style>
</style>

<script lang="ts">
	import { onMount } from 'svelte'
	// import { update_status } from '$lib/eel-functions'

	let status = {
		current_step: 0,
		message: '',
		is_completed: false
	}

	// onMount(() => {
	// 	// expose를 onMount에서 실행
	// 	window.update_status = update_status
	// })

	function startReservation() {
		if (window.eel) {
			window.eel.start_reservation()()
		}
	}
</script>

<main>
	<h1>예약 시스템</h1>

	<button on:click={startReservation} disabled={status.is_completed}> 예약 시작 </button>

	<div class="status">
		<p>현재 단계: {status.current_step}</p>
		<p>상태: {status.message}</p>

		<div class="progress-bar">
			<div class="progress" style="width: {(status.current_step / 4) * 100}%"></div>
		</div>
	</div>
</main>
