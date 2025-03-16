<script lang="ts">
	import * as Sidebar from '$lib/components/ui/sidebar/index.js'
	import * as Collapsible from '$lib/components/ui/collapsible/index.js'
	import GalleryVerticalEnd from 'lucide-svelte/icons/gallery-vertical-end'
	import ChevronRight from 'lucide-svelte/icons/chevron-right'
	import type { ComponentProps } from 'svelte'

	// 타입 정의
	type NavItem = {
		title: string
		url?: string
		isActive?: boolean
		items?: NavItem[]
	}

	type Items = {
		navMain: NavItem[]
	}

	// export let subtitle: string;
	let {
		ref = $bindable(null),
		title,
		subtitle,
		navData,
		...restProps
	}: ComponentProps<typeof Sidebar.Root> & {
		title: string
		subtitle: string
		navData: any
	} = $props()
</script>

<Sidebar.Root variant="floating" {...restProps}>
	<Sidebar.Header>
		<Sidebar.Menu>
			<Sidebar.MenuItem>
				<!-- 👉 타이틀 -->
				<Sidebar.MenuButton size="lg">
					{#snippet child({ props })}
						<a href="/" {...props}>
							<div
								class="bg-sidebar-primary text-sidebar-primary-foreground flex aspect-square size-8 items-center justify-center rounded-lg"
							>
								<GalleryVerticalEnd class="size-4" />
							</div>
							<div class="flex flex-col gap-0.5 leading-none">
								<span class="font-semibold">{title}</span>
								<span class="">{subtitle}</span>
							</div>
						</a>
					{/snippet}
				</Sidebar.MenuButton>
			</Sidebar.MenuItem>
		</Sidebar.Menu>
	</Sidebar.Header>
	<Sidebar.Content>
		<!-- 👉 - 네비게이션 contents -->
		<Sidebar.Group>
			<Sidebar.Menu class="gap-2">
				<!-- 👉 - props전달 받은 데이터 반복문 -->
				{#each navData.navMain as mainItem (mainItem.title)}
					<!-- 👉 - 하위메뉴가 있는경우 Collapse로 렌더링 -->
					{#if mainItem.items?.length}
						<Collapsible.Root open class="group/collapsible">
							<Sidebar.MenuItem>
								<Collapsible.Trigger class="w-full">
									<Sidebar.MenuButton class="flex font-bold">
										{#snippet child()}
											<div class="flex p-2 text-left text-sm font-bold">
												<span>
													{mainItem.title}
												</span>
												<ChevronRight
													class="ml-auto transition-transform group-data-[state=open]/collapsible:rotate-90"
												/>
											</div>
										{/snippet}
									</Sidebar.MenuButton>
								</Collapsible.Trigger>
								<Collapsible.Content>
									{#if mainItem.items?.length}
										<Sidebar.MenuSub class="ml-0 border-l-0 px-1.5">
											{#each mainItem.items as item (item.title)}
												<Sidebar.MenuSubItem>
													<Sidebar.MenuSubButton isActive={item.isActive}>
														{#snippet child({ props })}
															<a href={item.url} {...props}>{item.title}</a>
														{/snippet}
													</Sidebar.MenuSubButton>
												</Sidebar.MenuSubItem>
											{/each}
										</Sidebar.MenuSub>
									{/if}
								</Collapsible.Content>
							</Sidebar.MenuItem>
						</Collapsible.Root>
					{:else}
						<Sidebar.MenuItem>
							<Sidebar.MenuButton class="flex font-bold">
								{#snippet child({ props })}
									<a href={mainItem.url} {...props}>
										{mainItem.title}
									</a>
								{/snippet}
							</Sidebar.MenuButton>
						</Sidebar.MenuItem>
					{/if}
				{/each}
			</Sidebar.Menu>
		</Sidebar.Group>
	</Sidebar.Content>
</Sidebar.Root>
