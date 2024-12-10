<script lang="ts">
	import * as Card from '@ui/card/index.js'
	import { Label } from '@ui/label/index.js'
	import { Button } from '@ui/button/index.js'
	import { Input } from '@ui/input/index.js'
	import * as Select from '@ui/select/index.js'
	import { cn } from '$lib/utils.js'

	interface LoginCardProps {
		title: string
		titleColor?: string
		action?: () => void
	}
</script>

{#snippet loginCard(loginCardProps: LoginCardProps)}
	<Card.Root class="w-full  border shadow-none">
		<Card.Header>
			<Card.Title class={cn('text-lg font-extrabold', loginCardProps.titleColor)}
				>{loginCardProps.title}
			</Card.Title>
		</Card.Header>
		<Card.Content class="w-8/12">
			<form>
				<div class="grid w-full items-center gap-4">
					<div class="flex flex-col space-y-1.5">
						<Label for="name">Name</Label>
						<Input id="name" placeholder="Name of your project" />
					</div>
					<div class="flex flex-col space-y-1.5">
						<Label for="name">Name</Label>
						<Input id="name" placeholder="Name of your project" />
					</div>
				</div>
			</form>
		</Card.Content>
		<Card.Footer class="flex w-8/12 justify-between">
			<Button variant="outline">Cancel</Button>
			<Button>Deploy</Button>
		</Card.Footer>
	</Card.Root>
{/snippet}

{@render loginCard({ title: 'KTX 계정', titleColor: 'text-blue-700' })}
{@render loginCard({ title: 'SRT 계정', titleColor: 'text-purple-800' })}
