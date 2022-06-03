<script setup lang="ts">
	import { storeToRefs } from 'pinia';
	import { useBarItemCategoriesStore } from '@/stores/BarItemCategories';
	import { useBarItemsStore } from '@/stores/BarItems';
	import { useBarReceiptsStore } from '@/stores/BarReceiptss';

	const { loading, error, filteredItems } = storeToRefs(useBarItemsStore());
	const { categoryCatalog } = storeToRefs(useBarItemCategoriesStore());
	const { fetchBarItems } = useBarItemsStore();
	const { addItemQuantityToOrder } = useBarReceiptsStore();

	fetchBarItems();
</script>

<template>
	Produkty:
	<div v-if="loading">Ładuję produky...</div>
	<div v-if="error">Błąd ładowania produktów!<br />{{ error }}</div>
	<ul v-if="filteredItems && categoryCatalog" class="bar-items">
		<li v-for="item in filteredItems" :key="item.id">
			<span>{{ item.name }} ({{ categoryCatalog[item.categoryId].name }}) {{ item.price }} zł</span>
			<span v-if="!item.available" class="error">NIEDOSTĘPNY</span>
			<button v-if="item.available" @click="addItemQuantityToOrder(item.id)">Dodaj</button>
		</li>
	</ul>
</template>

<style scoped>
	ul li span.error {
		font-weight: bold;
		color: red;
	}
</style>
