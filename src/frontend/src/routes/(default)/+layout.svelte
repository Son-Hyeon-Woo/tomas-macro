<script lang="ts">
	import * as Sidebar from '$lib/components/ui/sidebar/index.js';
	import AppSidebar from '$lib/components/app-sidebar.svelte';
	import * as Breadcrumb from '$lib/components/ui/breadcrumb/index.js';
	import { Separator } from '$lib/components/ui/separator/index.js';

	import '@/app.css';

	let { children } = $props();

	const data = {
		navMain: [
			{
				title: '기차예매',

				items: [
					{
						title: 'KTX',
						url: '#'
					},
					{
						title: 'SRT',
						url: '#'
					}
				]
			},
			{
				title: '예매 확인',
				url: '#'
			},
			{
				title: '계정 설정',
				url: '#'
			},
			{
				title: '기차역 설정',
				url: '#'
			},
			{
				title: '알림 설정',
				url: '#'
			},
			{
				title: '예매 옵션 설정',
				url: '#'
			},
			{
				title: '카드 설정',
				url: '#'
			}
		]
	};
</script>

<div class="app">
	<Sidebar.Provider style="--sidebar-width: 13rem;">
		<AppSidebar title="Tomas Macro" subtitle="by hyeonwoo" navData={data} />
		<Sidebar.Inset>
			<!-- 👉 Top Nav bar -->
			<header class="flex h-16 shrink-0 items-center gap-2 px-4">
				<Sidebar.Trigger class="-ml-1" />
				<Separator orientation="vertical" class="mr-2 h-4" />
				<Breadcrumb.Root>
					<Breadcrumb.List>
						<Breadcrumb.Item class="hidden md:block">
							<Breadcrumb.Link href="#">Building Your Application</Breadcrumb.Link>
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

<style>
</style>
