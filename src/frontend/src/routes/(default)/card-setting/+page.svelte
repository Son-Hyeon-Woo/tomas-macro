<style>
</style>

<script lang="ts">
	import { onMount } from 'svelte'

	let status = {
		current_step: 0,
		message: '',
		is_completed: false
	}

	// JavaScript 함수를 전역 스코프에 먼저 정의
	function update_status(newStatus) {
		console.log('Status updated:', newStatus)
		status = newStatus
	}

	onMount(() => {
		// expose를 onMount에서 실행
		if (eel) {
			try {
				window.eel.expose(update_status, 'update_status')
				console.log('update_status exposed to Python')
			} catch (error) {
				console.error('Error exposing function:', error)
			}
		}
	})

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
