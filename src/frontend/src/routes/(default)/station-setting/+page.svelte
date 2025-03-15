<style>
</style>

<script lang="ts">
	import { onMount } from 'svelte'
	import { Toggle } from '$lib/components/ui/toggle/index.js'
	import * as Card from '$lib/components/ui/card/index.js'
	import { Button } from '$lib/components/ui/button/index.js'
	import * as Alert from '@ui/alert/index.js'
	import { Info } from 'lucide-svelte'
	import * as AlertDialog from '$lib/components/ui/alert-dialog/index.js'

	//👉 - alert 관련 변수
	let isAlertDialogOpen: boolean = $state(false)
	let alertTitle: string = $state('')
	let alertDescription: string = $state('')

	//👉 - 로컬에 저장된 즐겨찾는 역 가져오기
	async function getStation() {
		try {
			// @ts-ignore (eel 타입 무시)
			const response = await window.eel.get_station('SRT')()
			console.log('get_station:', response)
			return response
		} catch (error) {
			console.error('Error:', error)
		}
	}

	async function setStation() {
		try {
			// @ts-ignore (eel 타입 무시)
			const response = await window.eel.set_station('SRT', allStations)()
			console.log('setStation:', response)

			if (response) {
				isAlertDialogOpen = true
				alertTitle = '알림'
				alertDescription = '기차역이 저장되었습니다.'
			} else {
				isAlertDialogOpen = true
				alertTitle = '알림'
				alertDescription = '기차역 저장에 실패했습니다.'
			}

			//ℹ️ - 기차역 값 받아오기
			const response2 = await getStation()
			console.log('response2:', response2)

			//ℹ️ - page 내에서 사용가능하도록 객체 수정
			station = response2[0]
			allStations = Object.entries(station).map(([index, name]) => ({
				id: parseInt(index),
				name: name,
				selected: false
			}))

			//ℹ️ - name 값대로 정렬해주기
			allStations.sort((a, b) => a.name.localeCompare(b.name))

			//ℹ️ - 선택되어 있는 값은 selected 수정
			allStations.forEach((station) => {
				station.selected = response2[1].includes(station.name)
			})

			return response
		} catch (error) {
			console.error('Error:', error)
		}
	}

	let allStations = $state<{ id: number; name: string; selected: boolean }[]>([])

	let station = $state([])
	onMount(async () => {
		//ℹ️ - 기차역 값 받아오기
		const response = await getStation()

		//ℹ️ - page 내에서 사용가능하도록 객체 수정
		station = response[0]
		allStations = Object.entries(station).map(([index, name]) => ({
			id: parseInt(index),
			name: name,
			selected: false
		}))

		//ℹ️ - name 값대로 정렬해주기
		allStations.sort((a, b) => a.name.localeCompare(b.name))

		//ℹ️ - 선택되어 있는 값은 selected 수정
		allStations.forEach((station) => {
			station.selected = response[1].includes(station.name)
		})
	})
</script>

<Alert.Root class="border bg-neutral-100 py-2">
	<Alert.Title class="flex align-middle">
		<Info class="mr-2" />
		<span class="self-center">알림</span>
	</Alert.Title>
	<Alert.Description class="self-center">예매시 사용할 기차역을 선택해주세요.</Alert.Description>
</Alert.Root>

<Card.Root>
	<Card.Header>
		<Card.Title>SRT</Card.Title>
	</Card.Header>
	<Card.Content class="flex flex-wrap items-center justify-center gap-2">
		<div class="flex flex-wrap gap-2">
			{#each allStations as station}
				<Toggle
					aria-label="toggle"
					value={station.id}
					bind:pressed={station.selected}
					class="data-[state=on]:text-background w-[110px] px-4 font-bold text-neutral-700 data-[state=off]:bg-neutral-50 data-[state=on]:bg-neutral-700"
					>{station['name']}</Toggle
				>
			{/each}
		</div>
	</Card.Content>
	<Card.Footer class="flex justify-center">
		<Button class="w-1/3 bg-neutral-300 font-black text-slate-950" onclick={() => setStation()}
			>기차역 저장</Button
		>
	</Card.Footer>
</Card.Root>

<AlertDialog.Root bind:open={isAlertDialogOpen}>
	<AlertDialog.Content>
		<AlertDialog.Header>
			<AlertDialog.Title>{alertTitle}</AlertDialog.Title>
			<AlertDialog.Description>
				{alertDescription}
			</AlertDialog.Description>
		</AlertDialog.Header>
		<AlertDialog.Footer>
			<AlertDialog.Action onclick={() => (isAlertDialogOpen = false)}>Continue</AlertDialog.Action>
		</AlertDialog.Footer>
	</AlertDialog.Content>
</AlertDialog.Root>
