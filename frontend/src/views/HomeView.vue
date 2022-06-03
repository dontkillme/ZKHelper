<script setup lang="ts">
	import BarPin from '@/components/BarPin.vue';
	import BarCategories from '@/components/BarCategories.vue';
	import BarItems from '@/components/BarItems.vue';
	import BarReceiptOrder from '@/components/BarReceiptOrder.vue';
	import { useBarAuthStore } from '@/stores/BarAuth';
	import { storeToRefs } from 'pinia';

	const { isAuthenticated } = storeToRefs(useBarAuthStore());
</script>

<template>
	<main>
		<BarPin />
		<BarCategories v-if="isAuthenticated" />
		<BarItems v-if="isAuthenticated" />
		<BarReceiptOrder v-if="isAuthenticated" />
	</main>
</template>
