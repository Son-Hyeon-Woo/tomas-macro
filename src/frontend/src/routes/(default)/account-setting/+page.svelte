<script lang="ts">
	import * as Card from '@ui/card/index.js'
	import { Label } from '@ui/label/index.js'
	import { Button } from '@ui/button/index.js'
	import { Input } from '@ui/input/index.js'
	import * as Alert from '@ui/alert/index.js'

	import { cn } from '$lib/utils.js'

	import { Eye, EyeOff, Info } from 'lucide-svelte'

	import { onMount } from 'svelte'

	type LoginType = 'telno' | 'email' | 'membership'
	type TrainType = 'ktx' | 'srt'

	interface LoginCardProps {
		train: TrainType
		title: string
		titleColor?: string
		action?: () => void | undefined
	}

	//👉 - 로그인 유형 관련
	let ktxLoginType: LoginType = $state('telno')
	let srtLoginType: string = $state('telno')

	let ktxPlaceholderText: string = $derived.by(() => {
		if (ktxLoginType === 'telno') {
			return '전화번호를 입력하세요 (숫자만 입력)'
		} else if (ktxLoginType === 'email') {
			return '이메일을 입력하세요'
		} else {
			return '멤버십 번호를 입력하세요 (숫자만 입력)'
		}
	})
	let srtPlaceholderText: string = $derived.by(() => {
		if (srtLoginType === 'telno') {
			return '전화번호를 입력하세요 (숫자만 입력)'
		} else if (srtLoginType === 'email') {
			return '이메일을 입력하세요'
		} else {
			return '멤버십 번호를 입력하세요 (숫자만 입력)'
		}
	})

	function loginTypeClick(type: LoginType, train: TrainType) {
		if (train === 'ktx') {
			ktxLoginType = type
		} else {
			srtLoginType = type
		}
	}

	//👉 - 비밀번호 숨김 / 보이기
	let isKtxPasswordVisible: boolean = $state(false)
	let isSrtPasswordVisible: boolean = $state(false)
	function togglePasswordVisibility(train: TrainType) {
		if (train === 'ktx') {
			isKtxPasswordVisible = !isKtxPasswordVisible
		} else {
			isSrtPasswordVisible = !isSrtPasswordVisible
		}
	}

	//👉 - 마운트되면 이전 계정정보 가져오기
	let loginInfo: any = null
	onMount(() => {
		getLoginInfo('srt')
		getLoginInfo('ktx')
	})

	async function getLoginInfo(train: TrainType) {
		try {
			let trainUpper: string = train.toUpperCase()
			// @ts-ignore (eel 타입 무시)
			const response = await window.eel.get_login(trainUpper)()
			loginInfo = response
			console.log(trainUpper, 'Login Info:', response)
		} catch (error) {
			console.error('Error:', error)
		}
	}
</script>

{#snippet loginCard(loginCardProps: LoginCardProps)}
	<!-- 👉 로그인 유형 선택하는 버튼 -->
	{#snippet loginTypeBtn(type: LoginType, train: TrainType)}
		<Button
			value={type}
			onclick={() => loginTypeClick(type, train)}
			variant="outline"
			class={train === 'ktx'
				? cn('flex-1', 'text-sm', { ' !bg-neutral-200': ktxLoginType === type })
				: cn('flex-1', 'text-sm', { ' !bg-neutral-200': srtLoginType === type })}
			>{type === 'membership' ? '멤버십 번호' : type === 'email' ? '이메일' : '전화번호'}
		</Button>
	{/snippet}

	<Card.Root class="w-full border bg-neutral-50 shadow-none">
		<Card.Header>
			<Card.Title class={cn('text-xl font-extrabold', loginCardProps.titleColor)}
				>{loginCardProps.title}
			</Card.Title>
			<div class="!mt-4 flex space-x-3 px-1">
				{@render loginTypeBtn('telno', loginCardProps.train)}
				{@render loginTypeBtn('email', loginCardProps.train)}
				{@render loginTypeBtn('membership', loginCardProps.train)}
			</div>
		</Card.Header>
		<Card.Content class="">
			<form>
				<div class="grid w-full items-center gap-4">
					<div class="flex flex-col space-y-1.5">
						<Label for="id">아이디</Label>
						<Input
							id={loginCardProps.train + 'id'}
							placeholder={loginCardProps.train === 'ktx' ? ktxPlaceholderText : srtPlaceholderText}
						/>
					</div>

					<div class="flex flex-col space-y-1.5">
						<Label for="password">비밀번호</Label>
						<div class="flex space-x-2">
							<Input
								id={loginCardProps.train + 'password'}
								type={loginCardProps.train === 'ktx'
									? isKtxPasswordVisible
										? ''
										: 'password'
									: isSrtPasswordVisible
										? ''
										: 'password'}
							></Input>
							<!-- 👉 - 보이기/숨김 버튼 활성화 -->
							<Button
								size="icon"
								variant="ghost"
								onclick={() =>
									loginCardProps.train === 'ktx'
										? togglePasswordVisibility('ktx')
										: togglePasswordVisibility('srt')}
							>
								{#if loginCardProps.train === 'ktx'}
									{#if isKtxPasswordVisible}
										<EyeOff />
									{:else}
										<Eye />
									{/if}
								{:else if isSrtPasswordVisible}
									<EyeOff />
								{:else}
									<Eye />
								{/if}
							</Button>
						</div>
					</div>
				</div>
			</form>
		</Card.Content>
		<Card.Footer class="flex flex-row-reverse">
			<Button class="px-4">계정확인</Button>
		</Card.Footer>
	</Card.Root>
{/snippet}

<Alert.Root class="border bg-neutral-100 py-2">
	<Alert.Title class="flex align-middle">
		<Info class="mr-2" />
		<span class="self-center">알림</span>
	</Alert.Title>
	<Alert.Description class="self-center">
		아래의 계정으로 예매시 자동로그인 됩니다.
	</Alert.Description>
</Alert.Root>

<div class="flex space-x-4">
	<div class="flex-1">
		{@render loginCard({ train: 'ktx', title: 'KTX 계정', titleColor: 'text-blue-800' })}
	</div>
	<!-- <Separator class="" orientation="vertical" /> -->
	<div class="flex-1">
		{@render loginCard({ train: 'srt', title: 'SRT 계정', titleColor: 'text-purple-900' })}
	</div>
</div>
