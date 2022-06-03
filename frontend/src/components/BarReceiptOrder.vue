<script setup lang="ts">
	import { storeToRefs } from 'pinia';
	import { useBarReceiptsStore } from '@/stores/BarReceiptss';
	import { debounce } from 'lodash';
	import { useBarItemsStore } from '@/stores/BarItems';

	const {
		orderAccount,
		orderItems,
		sending,
		error,
		hasAnyItemsInOrder,
		orderTotal,
		basicInfoLoading,
		basicInfoError,
		basicInfo,
	} = storeToRefs(useBarReceiptsStore());
	const { itemCatalog } = storeToRefs(useBarItemsStore());
	const { addItemQuantityToOrder, takeItemQuantityToOrder, createBarReceipt, fetchAccountBasicInfo } =
		useBarReceiptsStore();

	const fetchAccountBasicInfoDebounced = debounce(() => fetchAccountBasicInfo(), 500);
</script>

<template>
	Zamówienie:<br />Krecha na usera:<input v-model="orderAccount" @input="fetchAccountBasicInfoDebounced" />
	<span v-if="basicInfoLoading">Wczytuję podsumowanie usera...</span>
	<span v-if="basicInfoError">Błąd wczytywania podsumowanie usera!<br />{{ basicInfoError }}</span>
	<span v-if="basicInfo">
		promocyjne ceny: {{ basicInfo.isStaff }} stan konta: {{ basicInfo.balance }} suma wpłat na krechę:
		{{ basicInfo.credits }}
	</span>
	<br />
	<ul v-if="hasAnyItemsInOrder" class="bar-items">
		<li v-for="orderItem in orderItems" :key="orderItem.itemId">
			<span>
				x{{ orderItem.quantity }}
				{{ itemCatalog[orderItem.itemId].name }}
				{{ itemCatalog[orderItem.itemId].price * orderItem.quantity }} zł
			</span>
			<button @click="addItemQuantityToOrder(orderItem.itemId)">+</button>
			<button @click="takeItemQuantityToOrder(orderItem.itemId)">-</button>
		</li>
	</ul>
	<div v-else>Brak produktów w zamówieniu!</div>
	<div v-if="hasAnyItemsInOrder">SUMA: {{ orderTotal }} zł</div>
	<button v-if="hasAnyItemsInOrder" @click="createBarReceipt()">Zamów!</button>
	<span v-if="sending">Zamawiam...</span> <span v-if="error">Błąd w zamiawaniu!<br />{{ error }}</span>
</template>
