<script lang="ts">
	import * as Card from '@ui/card/index.js'
	import { Label } from '@ui/label/index.js'
	import { Button } from '@ui/button/index.js'
	import { Input } from '@ui/input/index.js'
	import * as Alert from '@ui/alert/index.js'
	import * as AlertDialog from '$lib/components/ui/alert-dialog/index.js'

	import { cn } from '$lib/utils.js'

	import { Eye, EyeOff, Info } from 'lucide-svelte'

	import { onMount } from 'svelte'
	import { authService } from '$lib/services/authService'

	type LoginType = 'telno' | 'email' | 'membership'
	type TrainType = 'ktx' | 'srt'

	interface LoginCardProps {
		train: TrainType
		title: string
		titleColor?: string
		action?: () => void | undefined
	}

	//👉 - alert 관련 변수
	let isAlertDialogOpen: boolean = $state(false)
	let alertTitle: string = ''
	let alertDescription: string = ''

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

	//👉 - 로그인 타입 클릭
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

	//👉 - 로그인 확인 클릭 이벤트
	async function loginCheckClick(train: TrainType) {
		let response: any
		if (train === 'ktx') {
			response = await authService.loginCheck(train, ktxInfo.id, ktxInfo.pass)
		} else {
			response = await authService.loginCheck(train, srtInfo.id, srtInfo.pass)
		}

		if (response.status === 'success') {
			console.log('로그인 성공:', response)
			isAlertDialogOpen = true
			alertTitle = '로그인 성공'
			alertDescription = '로그인 성공하였습니다.'
			srtInfo = await getLoginInfo('srt')
			ktxInfo = await getLoginInfo('ktx')
		} else {
			console.error('로그인 실패:', response)
			isAlertDialogOpen = true
			alertTitle = '로그인 실패'
			alertDescription = '로그인 실패하였습니다.'
		}
	}

	//👉 - 마운트되면 이전 계정정보 가져오기
	let ktxInfo: any = $state({ id: '', pass: '', last_login_at: '', last_login_type: '' })
	let srtInfo: any = $state({ id: '', pass: '', last_login_at: '', last_login_type: '' })
	onMount(async () => {
		srtInfo = await getLoginInfo('srt')
		ktxInfo = await getLoginInfo('ktx')
	})

	//👉 - 로컬에 저장된 로그인 정보 가져오기
	async function getLoginInfo(train: TrainType) {
		try {
			let trainUpper: string = train.toUpperCase()
			// @ts-ignore (eel 타입 무시)
			const response = await window.eel.get_login(trainUpper)()
			console.log(trainUpper, 'Login Info:', response)
			return response
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
				<span class="ms-1 text-xs font-medium text-black">
					마지막 계정확인 :
					{#if loginCardProps.train === 'ktx'}
						{ktxInfo.last_login_at}
					{:else}
						{srtInfo.last_login_at}
					{/if}
				</span>
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
					<!-- 👉 - ID input -->
					<div class="flex flex-col space-y-1.5">
						<Label for="id">아이디</Label>
						{#if loginCardProps.train === 'ktx'}
							<Input
								id={loginCardProps.train + 'id'}
								placeholder={ktxPlaceholderText}
								bind:value={ktxInfo.id}
							/>
						{:else}
							<Input
								id={loginCardProps.train + 'id'}
								placeholder={srtPlaceholderText}
								bind:value={srtInfo.id}
							/>
						{/if}
					</div>
					<!-- 👉 - Password input -->
					<div class="flex flex-col space-y-1.5">
						<Label for="password">비밀번호</Label>
						<div class="flex space-x-2">
							{#if loginCardProps.train === 'ktx'}
								<Input
									id={loginCardProps.train + 'password'}
									type={isKtxPasswordVisible ? '' : 'password'}
									bind:value={ktxInfo.pass}
								/>
							{:else}
								<Input
									id={loginCardProps.train + 'password'}
									type={isSrtPasswordVisible ? '' : 'password'}
									bind:value={srtInfo.pass}
								/>
							{/if}
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
			<Button onclick={() => loginCheckClick(loginCardProps.train)} class="px-4">계정확인</Button>
		</Card.Footer>
	</Card.Root>
{/snippet}

<Alert.Root class="border bg-neutral-100 py-2">
	<Alert.Title class="flex align-middle">
		<Info class="mr-2" />
		<span class="self-center">알림</span>
	</Alert.Title>
	<Alert.Description class="self-center">
		예매시 아래의 계정으로 자동로그인 됩니다.
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
