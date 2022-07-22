<script setup lang="ts">
	import HeaderLoginState from 'components/HeaderLoginState.vue';
	import { useQuasar } from 'quasar';

	import { ref, getCurrentInstance } from 'vue';
	import { storeToRefs } from 'pinia';
	import { useBarAuthStore } from 'stores/BarAuth';

	const { isAuthenticated } = storeToRefs(useBarAuthStore());

	const $q = useQuasar()

	const tab = ref('bar');

    const app = getCurrentInstance();
    const $window = app?.appContext.config.globalProperties.$window;

	function shouldHideFullscreenMode() {
		return ($window.navigator.standalone == true) || $window.matchMedia('(display-mode: standalone)').matches || $q.platform.is.iphone;
	}
</script>

<template>
	<q-layout view="hhh LpR fFf">
		<q-header bordered>
			<div class="row">
				<q-toolbar class="col-12 col-sm bg-grey-10">
					<q-toolbar-title shrink>Zakonki App</q-toolbar-title>
					<q-separator vertical inset spaced />
					<q-tabs v-model="tab" shrink>
						<q-tab name="bar" label="Bar" />
					</q-tabs>
					<q-space />
					<q-btn
						v-if="!shouldHideFullscreenMode()"
						flat
						@click="$q.fullscreen.toggle()"
						:icon="$q.fullscreen.isActive ? 'fullscreen_exit' : 'fullscreen'"
					/>
				</q-toolbar>
				<q-toolbar
					v-if="isAuthenticated"
					class="col-12 col-sm-auto bg-grey-10"
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

	html, body, #q-app, .q-layout, .q-page-container, .q-page {
		height: 100%;
	}

	.q-field--dense .q-field__label, .q-item__label--header {
		font-size: $body-font-size;
	}
</style>
