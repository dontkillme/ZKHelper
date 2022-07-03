<script setup lang="ts">
	import { storeToRefs } from 'pinia';
	import { useBarItemCategoriesStore } from 'stores/BarItemCategories';
	import { computed } from 'vue';

	const { categories, loading, error, selectedCategoryId } = storeToRefs(useBarItemCategoriesStore());
	const { fetchBarItemCategories } = useBarItemCategoriesStore();

	const options = computed(() => {
		return [
			{
				label: 'Wszystkie',
				value: null,
				class: 'outlined',
			},
			...categories.value.map((category) => ({
				label: category.name,
				value: category.id,
				class: 'outlined',
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
		spread
		no-caps
		unelevated
		toggle-color="primary"
		color="dark-page"
		style="height: 3em"
		:options="options"
	/>
</template>

<style lang="scss">
	.outlined {
		border-bottom: 1px solid $grey-9;

		& + & {
			border-left: 1px solid $grey-9;
		}
	}
</style>
