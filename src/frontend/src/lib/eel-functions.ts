declare global {
	interface Window {
		update_status: (newStatus: string) => void
	}
}

// JavaScript 함수를 전역 스코프에 먼저 정의
export function update_status(newStatus: string) {
	console.log('Status updated:', newStatus)
}
