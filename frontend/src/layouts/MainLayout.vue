<script setup lang="ts">
	import HeaderLoginState from 'components/HeaderLoginState.vue';
	import { useQuasar } from 'quasar';

	import { getCurrentInstance } from 'vue';
	import { storeToRefs } from 'pinia';
	import { useAuthStore } from 'stores/AuthStore';

	const { isAuthenticated } = storeToRefs(useAuthStore());

	const $q = useQuasar();

	const app = getCurrentInstance();
	const $window = app?.appContext.config.globalProperties.$window;

	function shouldHideFullscreenMode() {
		return (
			$window.navigator.standalone == true ||
			$window.matchMedia('(display-mode: standalone)').matches ||
			$q.platform.is.iphone
		);
	}
</script>

<template>
	<q-layout view="hhh LpR fFf">
		<q-header bordered>
			<div class="row">
				<q-toolbar
					class="col-12 col-sm bg-grey-10"
					style="flex-wrap: wrap"
				>
					<q-toolbar-title
						shrink
						class="q-my-sm q-my-md-none col-auto"
						>Zakonki App</q-toolbar-title
					>
					<q-space class="lt-sm col" />
					<q-btn
						v-if="!shouldHideFullscreenMode()"
						flat
						@click="$q.fullscreen.toggle()"
						:icon="
							$q.fullscreen.isActive
								? 'fullscreen_exit'
								: 'fullscreen'
						"
						class="lt-sm col-auto"
					/>
					<q-separator vertical inset spaced class="gt-xs" />
					<q-tabs shrink class="col-12 col-sm-auto">
						<q-route-tab to="/bar" label="Bar" exact />
						<q-route-tab
							to="/participants"
							label="Uczestnicy"
							exact
						/>
						<q-route-tab to="/quests" label="Questy" exact />
					</q-tabs>
					<q-space class="gt-xs col" />
					<q-btn
						v-if="!shouldHideFullscreenMode()"
						flat
						@click="$q.fullscreen.toggle()"
						:icon="
							$q.fullscreen.isActive
								? 'fullscreen_exit'
								: 'fullscreen'
						"
						class="gt-xs col-auto"
					/>
				</q-toolbar>
				<q-toolbar
					v-if="isAuthenticated"
					class="col-12 col-md-auto bg-grey-10"
				>
					<q-space />
					<HeaderLoginState />
				</q-toolbar>
			</div>
		</q-header>

		<q-page-container>
			<router-view />
		</q-page-container>
	</q-layout>
</template>

<style lang="scss">
	.q-layout__section--marginal {
		background-color: $dark;
	}

	.q-header--bordered {
		border-color: $grey-9 !important;
	}

	.q-header {
		color: $grey-5;
	}

	.q-separator {
		background-color: $grey-9;
	}

	html,
	body,
	#q-app,
	.q-layout,
	.q-page-container,
	.q-page {
		height: 100%;
	}

	.q-field--dense .q-field__label,
	.q-item__label--header {
		font-size: $body-font-size;
	}
</style>
