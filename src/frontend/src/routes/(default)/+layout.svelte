<style>
</style>

<script lang="ts">
	import * as Sidebar from '$lib/components/ui/sidebar/index.js'
	import AppSidebar from '@/routes/(default)/components/app-sidebar.svelte'
	import * as Breadcrumb from '$lib/components/ui/breadcrumb/index.js'
	import { Separator } from '$lib/components/ui/separator/index.js'

	import '@/app.css'

	let { children } = $props()

	//👉 - 네비게이션 데이터
	const data = {
		navMain: [
			{
				title: '기차예매',
				items: [
					{
						title: 'KTX',
						url: 'ktx-reservation'
					},
					{
						title: 'SRT',
						url: 'srt-reservation'
					}
				]
			},
			{
				title: '예매 확인',
				url: 'my-reservation'
			},
			{
				title: '계정 설정',
				url: 'account-setting'
			},
			{
				title: '기차역 설정',
				url: 'station-setting'
			},
			{
				title: '알림 설정',
				url: 'alarm-setting'
			},
			{
				title: '예매 옵션 설정',
				url: 'reservation-option-setting'
			},
			{
				title: '카드 설정',
				url: 'card-setting'
			}
		],
		navPathMap: {
			'ktx-reservation': ['기차예매', 'KTX'],
			'srt-reservation': ['기차예매', 'SRT'],
			'my-reservation': ['예매 확인'],
			'account-setting': ['계정 설정'],
			'station-setting': ['기차역 설정'],
			'alarm-setting': ['알림 설정'],
			'reservation-option-setting': ['예매 옵션 설정'],
			'card-setting': ['카드 설정']
		}
	}

	//👉 - 현재 Url 정보
	import { page } from '$app/stores'
	import { derived } from 'svelte/store'
	// const currentPath = $derived($page.url)
	// const currentPath = $derived(page, ($page) => $page.url.pathname)

	// console.log('currentPath', currentPath)
	$effect(() => console.log($page))
	let currentPath = $derived.by(() => {
		return $page.url.pathname.split('/').pop()
	})
	// const currentPath = derived(page, ($page) => {
	// 	console.log('currentPath', $page.url.pathname)
	// 	$page.url.pathname
	// })
</script>

<div class="app">
	<Sidebar.Provider style="--sidebar-width: 13rem;">
		<AppSidebar title="Tomas Macro" subtitle="by hyeonwoo" navData={data} />
		<Sidebar.Inset>
			<!-- 👉 Top Nav bar -->
			<header class="flex h-16 shrink-0 items-center gap-2 px-4">
				<Sidebar.Trigger class="-ml-1" />
				<Separator orientation="vertical" class="mr-2 h-4" />
				<!-- 👉 - Displays the path  -->
				<Breadcrumb.Root>
					<Breadcrumb.List>
						<Breadcrumb.Item class="hidden md:block">
							<Breadcrumb.Link href="#">{currentPath}</Breadcrumb.Link>
						</Breadcrumb.Item>
						<Breadcrumb.Separator class="hidden md:block" />
						<Breadcrumb.Item>
							<Breadcrumb.Page>Data Fetching</Breadcrumb.Page>
						</Breadcrumb.Item>
					</Breadcrumb.List>
				</Breadcrumb.Root>
			</header>
			<main>
				<div class="flex flex-1 flex-col gap-4 p-4 pt-0">
					<!-- children에서 type error가 발생해서 옵셔널체이닝 처리 -->
					{@render children?.()}
				</div>
			</main>
		</Sidebar.Inset>
	</Sidebar.Provider>
</div>
