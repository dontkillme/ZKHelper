import { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
	{
		path: '/',
		redirect: () => {
			return {
				path: '/bar',
			};
		},
	},
	{
		path: '/bar',
		component: () => import('layouts/MainLayout.vue'),
		children: [{ path: '', component: () => import('pages/BarPage.vue') }],
	},
	{
		path: '/participants',
		component: () => import('layouts/MainLayout.vue'),
		children: [
			{ path: '', component: () => import('pages/ParticipantsPage.vue') },
		],
	},
	{
		path: '/quests',
		component: () => import('layouts/MainLayout.vue'),
		children: [
			{ path: '', component: () => import('pages/QuestsPage.vue') },
		],
	},
	// Always leave this as last one,
	// but you can also remove it
	{
		path: '/:catchAll(.*)*',
		component: () => import('pages/ErrorNotFound.vue'),
	},
];

export default routes;
