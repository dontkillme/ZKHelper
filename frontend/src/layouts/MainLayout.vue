<template>
	<q-layout view="hHh LpR fFf">
		<q-header bordered>
			<q-toolbar class="bg-grey-10">
				<q-toolbar-title shrink>Zakonki App</q-toolbar-title>
				<q-separator vertical inset spaced />
				<span class="q-ml-sm q-mt-xs">Bar</span>
				<q-space />
				<HeaderLoginState />
			</q-toolbar>
		</q-header>

		<q-page-container>
			<router-view />
		</q-page-container>
	</q-layout>
</template>

<script setup lang="ts">
	import HeaderLoginState from 'components/HeaderLoginState.vue';
</script>

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
</style>
