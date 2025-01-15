<style>
</style>

<script lang="ts">
	import * as Card from '$lib/components/ui/card/index.js'
	import * as Select from '$lib/components/ui/select/index.js'
	import { SquareArrowRight, ArrowRight } from 'lucide-svelte'
	import CalendarIcon from 'lucide-svelte/icons/calendar'
	import { DateFormatter, type DateValue, getLocalTimeZone, today } from '@internationalized/date'
	import { cn } from '$lib/utils.js'
	import { buttonVariants } from '$lib/components/ui/button/index.js'
	import { Calendar } from '$lib/components/ui/calendar/index.js'
	import * as Popover from '$lib/components/ui/popover/index.js'
	import { Button } from '$lib/components/ui/button/index.js'
	import { Search } from 'lucide-svelte'

	//👉 - 날짜 선택 기능
	const df = new DateFormatter('ko-KR', {
		dateStyle: 'long'
	})

	let value2 = $state(today(getLocalTimeZone()))
	let contentRef = $state<HTMLElement | null>(null)

	//👉 - 역 선택 기능
	//ℹ️ - 추천 역 리스트 기능구현시 사용
	// const recommend = [
	// 	{ value: 'mandarin', label: 'Mandarin' },
	// 	{ value: 'orange', label: 'Orange' },
	// 	{ value: 'strawberry', label: 'Strawberry' },
	// 	{ value: 'watermelon', label: 'Watermelon' }
	// ]

	const startStations = [
		{ value: '1', label: '대구(통도사)' },
		{ value: '2', label: '부산' },
		{ value: '3', label: '서울' },
		{ value: '4', label: '대전' },
		{ value: '5', label: '광주' }
	]

	const arrivalStations = [
		{ value: '1', label: '대구' },
		{ value: '2', label: '부산' },
		{ value: '3', label: '서울' },
		{ value: '4', label: '대전' },
		{ value: '5', label: '광주' }
	]

	let startStation = $state('')
	let arrivalStation = $state('')

	//ℹ️ - 출발역 선택시 해당 역명으로 변경
	const startTriggerContent = $derived(
		startStations.find((f) => f.value === startStation)?.label ?? '출발역'
	)
	const arrivalTriggerContent = $derived(
		arrivalStations.find((f) => f.value === arrivalStation)?.label ?? '도착역'
	)

	//👉 - 시간 선택 기능
	const startTimes = [
		{ value: '01', label: '01시' },
		{ value: '02', label: '02시' },
		{ value: '03', label: '03시' },
		{ value: '04', label: '04시' },
		{ value: '05', label: '05시' }
	]

	let value = $state('')

	const triggerContent = $derived(startTimes.find((f) => f.value === value)?.label ?? '시각')

	//👉 - 인원수 선택 기능
	const personCounts = [
		{ value: '1', label: '1명' },
		{ value: '2', label: '2명' },
		{ value: '3', label: '3명' },
		{ value: '4', label: '4명' },
		{ value: '5', label: '5명' }
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
		<Select.Root type="single" name="favoriteFruit" bind:value={startStation}>
			<Select.Trigger class="mr-1 w-[120px]">
				{startTriggerContent}
			</Select.Trigger>
			<Select.Content>
				<!-- <Select.Group>
					<Select.GroupHeading>Fruits</Select.GroupHeading>
					{#each recommend as fruit}
						<Select.Item value={fruit.value} label={fruit.label}>{fruit.label}</Select.Item>
					{/each}
				</Select.Group> -->
				<Select.Group>
					<Select.GroupHeading>출발역</Select.GroupHeading>
					{#each startStations as station}
						<Select.Item value={station.value} label={station.label}>{station.label}</Select.Item>
					{/each}
				</Select.Group>
			</Select.Content>
		</Select.Root>

		<!-- 👉 - 역선택 사이 화살표 기호 -->
		<ArrowRight size={32} color="#8267b4" class="mr-1 justify-center align-middle" />

		<!-- 👉 - 도착역 선택 Select 박스 -->
		<Select.Root type="single" name="favoriteFruit" bind:value={arrivalStation}>
			<Select.Trigger class="mr-5 w-[120px]">
				{arrivalTriggerContent}
			</Select.Trigger>
			<Select.Content>
				<!-- <Select.Group>
					<Select.GroupHeading>Fruits</Select.GroupHeading>
					{#each recommend as fruit}
						<Select.Item value={fruit.value} label={fruit.label}>{fruit.label}</Select.Item>
					{/each}
				</Select.Group> -->
				<Select.Group>
					<Select.GroupHeading>도착역</Select.GroupHeading>
					{#each arrivalStations as station}
						<Select.Item value={station.value} label={station.label}>{station.label}</Select.Item>
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
						class: 'mr-2 w-[160px] justify-start text-left font-normal'
					}),
					!value2 && 'text-muted-foreground'
				)}
			>
				<CalendarIcon />
				{value2 ? df.format(value2.toDate(getLocalTimeZone())) : '출발 날짜 선택'}
			</Popover.Trigger>
			<Popover.Content bind:ref={contentRef} class="w-auto p-0">
				<Calendar type="single" bind:value={value2} />
			</Popover.Content>
		</Popover.Root>

		<!-- 👉 - 출발시각 선택하는 Select -->
		<Select.Root type="single" name="favoriteFruit" bind:value>
			<Select.Trigger class="mr-1 w-[80px]">
				{triggerContent}
			</Select.Trigger>
			<Select.Content class="w-[70px]">
				<Select.Group class="">
					{#each startTimes as fruit}
						<Select.Item value={fruit.value} label={fruit.label}>{fruit.label}</Select.Item>
					{/each}
				</Select.Group>
			</Select.Content>
		</Select.Root>

		<!-- 👉 - 사람 수 선택하는 Select -->
		<Select.Root type="single" name="favoriteFruit" bind:value={person_value}>
			<Select.Trigger class="mr-5 w-[80px]">
				{triggerContent2}
			</Select.Trigger>
			<Select.Content class="w-[70px]">
				<Select.Group class="">
					{#each personCounts as fruit}
						<Select.Item value={fruit.value} label={fruit.label}>{fruit.label}</Select.Item>
					{/each}
				</Select.Group>
			</Select.Content>
		</Select.Root>

		<!-- 👉 - 검색버튼 -->
		<Button class="bg-purple-900 px-5">
			<Search class="size-4" />
		</Button>
	</Card.Content>
</Card.Root>

<Card.Root>
	<Card.Content>
		<p>Card Content</p>
	</Card.Content>
</Card.Root>
