<script setup lang="ts">
	import { storeToRefs } from 'pinia';
	import { useBarItemCategoriesStore } from 'stores/BarItemCategories';
	import { computed } from 'vue';

	const { categories, loading, error, selectedCategoryId } = storeToRefs(useBarItemCategoriesStore());
	const { fetchBarItemCategories } = useBarItemCategoriesStore();

	const options = computed(() => {
		const sharedOptions = {
			class: 'outlined col-6 col-sm-4 col-md',
			style: {
				height: '3rem',
			},
		};

		return [
			{
				label: 'Wszystkie',
				value: null,
				...sharedOptions,
			},
			...categories.value.map((category) => ({
				label: category.name,
				value: category.id,
				...sharedOptions,
			})),
		];
	});

	fetchBarItemCategories();
</script>

<template>
	<q-skeleton
		v-if="loading"
		type="QBtn"
		animation="fade"
		height="3em"
		width="100%"
	/>
	<q-btn-toggle
		v-if="!loading && !error"
		v-model="selectedCategoryId"
		no-wrap
		no-caps
		unelevated
		stretch
		toggle-color="primary"
		color="dark-page"
		style="width: 100%; flex-wrap: wrap;"
		:options="options"
	/>
</template>

<style lang="scss">
	.outlined {
		border-bottom: 1px solid $grey-9;
		border-right: 1px solid $grey-9;

		&:first-child {
			border-left: 1px solid $grey-9;
		}
	}
</style>
