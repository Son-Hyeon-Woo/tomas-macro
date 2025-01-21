<style>
</style>

<script lang="ts">
	import { onMount } from 'svelte'

	import * as Card from '$lib/components/ui/card/index.js'
	import * as Select from '$lib/components/ui/select/index.js'
	import * as AlertDialog from '$lib/components/ui/alert-dialog'
	import * as Popover from '$lib/components/ui/popover/index.js'
	import { Calendar } from '$lib/components/ui/calendar/index.js'
	import { buttonVariants } from '$lib/components/ui/button/index.js'
	import { Button } from '$lib/components/ui/button/index.js'

	import { ArrowRight } from 'lucide-svelte'
	import CalendarIcon from 'lucide-svelte/icons/calendar'
	import { CircleX } from 'lucide-svelte'
	import { Search } from 'lucide-svelte'

	import { DateFormatter, getLocalTimeZone, today } from '@internationalized/date'
	import { cn } from '$lib/utils.js'

	onMount(async () => {
		//ℹ️ - 기차역 값 받아오기 & 정렬
		const response = await getStation()
		ALLSTATIONS = response[0]
		selectedStationIds = response[1]
		selectedStations = selectedStationIds.map((index) => {
			return {
				id: index.toString(),
				name: ALLSTATIONS[index]
			}
		})
		selectedStations.sort((a, b) => a.name.localeCompare(b.name))
	})

	//👉 - alert 여는 함수
	let isAlertDialogOpen: boolean = $state(false)
	let alertTitle: string = $state('')
	function openAlertDialog(title: string) {
		isAlertDialogOpen = true
		alertTitle = title
	}

	//👉 - 검색버튼 클릭 이벤트
	async function trainSearch() {
		if (startStation === '' || arrivalStation === '') {
			openAlertDialog('출발역과 도착역을 선택해주세요.')
			return
		}

		if (startStation === arrivalStation) {
			openAlertDialog('출발역과 도착역이 같습니다.')
			return
		}

		console.log(ALLSTATIONS[Number(startStation)])
		console.log(ALLSTATIONS[Number(arrivalStation)])
		console.log(pickedDate.toString())
	}

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

	//👉 - 날짜 선택 기능
	const df = new DateFormatter('ko-KR', {
		dateStyle: 'medium'
	})

	let currentDateTime = today(getLocalTimeZone())
	let maxDateTime = currentDateTime.add({ months: 1 })
	let pickedDate = $state(currentDateTime)
	let contentRef = $state<HTMLElement | null>(null)

	//👉 - 역 선택 기능
	let ALLSTATIONS: string[] = []
	let selectedStationIds: number[] = []
	let selectedStations: { id: string; name: string }[] = $state([])
	let startStation = $state('')
	let arrivalStation = $state('')

	//ℹ️ - 출발역 선택시 해당 역명으로 변경
	const startTriggerContent = $derived(
		selectedStations.find((f) => f.id === startStation)?.name ?? '출발역'
	)
	const arrivalTriggerContent = $derived(
		selectedStations.find((f) => f.id === arrivalStation)?.name ?? '도착역'
	)

	//👉 - 시간 선택 기능
	const timeChoices: [string, string][] = Array.from({ length: 24 }, (_, h) => {
		const hour = h.toString().padStart(2, '0')
		return [hour, `${hour}0000`]
	})
	let timeValue = $state('')

	const tiemTriggerContent = $derived(timeChoices.find((f) => f[0] === timeValue) ?? '시각')

	//👉 - 인원수 선택 기능
	const personCounts = [
		{ value: '1', label: '1명' },
		{ value: '2', label: '2명' },
		{ value: '3', label: '3명' },
		{ value: '4', label: '4명' },
		{ value: '5', label: '5명' },
		{ value: '6', label: '6명' },
		{ value: '7', label: '7명' },
		{ value: '8', label: '8명' },
		{ value: '9', label: '9명' }
	]

	let person_value = $state('')

	const triggerContent2 = $derived(
		personCounts.find((f) => f.value === person_value)?.label ?? '인원'
	)
</script>

<Card.Root>
	<Card.Header>
		<Card.Title class="text-xl text-violet-950">승차권 조회</Card.Title>
	</Card.Header>
	<Card.Content class="flex flex-wrap items-center justify-center">
		<!-- 👉 - 출발역 선택 Select 박스 -->
		<Select.Root type="single" name="startStation" bind:value={startStation}>
			<!-- 👉 - selectbox 트리거 ( 값 바꾸면 텍스트 변경 )-->
			<Select.Trigger class="w-[120px]">
				{startTriggerContent}
			</Select.Trigger>
			<Select.Content>
				<Select.Group>
					<Select.GroupHeading>출발역</Select.GroupHeading>
					{#each selectedStations as station}
						<Select.Item value={station.id} label={station.name}>{station.name}</Select.Item>
					{/each}
				</Select.Group>
			</Select.Content>
		</Select.Root>

		<!-- 👉 - 역선택 사이 화살표 기호 -->
		<ArrowRight size={32} color="#4f4f4f" class="justify-center align-middle" />

		<!-- 👉 - 도착역 선택 Select 박스 -->
		<Select.Root type="single" name="arrivalStation" bind:value={arrivalStation}>
			<!-- 👉 - selectbox 트리거 ( 값 바꾸면 텍스트 변경 )-->
			<Select.Trigger class="mr-3 w-[120px]">
				{arrivalTriggerContent}
			</Select.Trigger>
			<Select.Content>
				<Select.Group>
					<Select.GroupHeading>도착역</Select.GroupHeading>
					{#each selectedStations as station}
						<Select.Item value={station.id} label={station.name}>{station.name}</Select.Item>
					{/each}
				</Select.Group>
			</Select.Content>
		</Select.Root>

		<!-- 👉 - 출발날짜 선택하는 Date Picker -->
		<Popover.Root>
			<Popover.Trigger
				class={cn(
					buttonVariants({
						variant: 'outline',
						class: 'mr-3 w-[140px] justify-start text-left font-normal'
					}),
					!currentDateTime && 'text-muted-foreground'
				)}
			>
				<CalendarIcon />
				{pickedDate ? df.format(pickedDate.toDate(getLocalTimeZone())) : '출발 날짜 선택'}
			</Popover.Trigger>
			<Popover.Content bind:ref={contentRef} class="w-auto p-0">
				<Calendar
					type="single"
					bind:value={pickedDate}
					minValue={currentDateTime}
					maxValue={maxDateTime}
					locale="ko-KR"
				/>
			</Popover.Content>
		</Popover.Root>

		<!-- 👉 - 출발시각 선택하는 Select -->
		<Select.Root type="single" name="startTime" bind:value={timeValue}>
			<Select.Trigger class="mr-3 w-[80px]">
				{tiemTriggerContent}
			</Select.Trigger>
			<Select.Content class="min-w-[var(--bits-select-anchor-width)]">
				{#each timeChoices as time}
					<Select.Item value={time[1]} label={time[0]}>{time[0]}</Select.Item>
				{/each}
			</Select.Content>
		</Select.Root>

		<!-- 👉 - 사람 수 선택하는 Select -->
		<Select.Root type="single" name="favoriteFruit" bind:value={person_value}>
			<Select.Trigger class="w-[80px]">
				{triggerContent2}
			</Select.Trigger>
			<Select.Content class="min-w-[var(--bits-select-anchor-width)]">
				<Select.Group class="">
					{#each personCounts as fruit}
						<Select.Item value={fruit.value} label={fruit.label}>{fruit.label}</Select.Item>
					{/each}
				</Select.Group>
			</Select.Content>
		</Select.Root>

		<!-- 👉 - 검색버튼 -->
		<Button class="ms-auto w-[90px] bg-purple-900" onclick={() => trainSearch()}>
			<Search class="size-4" />
		</Button>
	</Card.Content>
</Card.Root>

<Card.Root>
	<Card.Content>
		<p>Card Content</p>
	</Card.Content>
</Card.Root>

<AlertDialog.Root bind:open={isAlertDialogOpen}>
	<AlertDialog.Content>
		<AlertDialog.Header>
			<AlertDialog.Title class="flex justify-center">
				<CircleX class="size-20 text-red-500" />
			</AlertDialog.Title>
			<AlertDialog.Description class="mt-4 text-center text-xl font-medium text-neutral-600">
				{alertTitle}
			</AlertDialog.Description>
		</AlertDialog.Header>
		<AlertDialog.Footer class="flex !justify-center">
			<AlertDialog.Cancel class="mt-6 bg-neutral-100 px-8">닫기</AlertDialog.Cancel>
		</AlertDialog.Footer>
	</AlertDialog.Content>
</AlertDialog.Root>
