import { redirect } from '@sveltejs/kit'
import type { PageServerLoad } from './$types'

export const load: PageServerLoad = async () => {
	throw redirect(302, '/ktx-reservation') // 302: 임시 리디렉션
}
