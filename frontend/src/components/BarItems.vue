<script setup lang="ts">
	import EmptyComponent from 'components/EmptyComponent.vue';
	import { storeToRefs } from 'pinia';
	import { useBarItemsStore } from 'stores/BarItems';
	import { useBarReceiptsStore } from 'stores/BarReceipts';

	const { loading, error, filteredItems } = storeToRefs(useBarItemsStore());
	const { orderItemCatalog } = storeToRefs(useBarReceiptsStore());
	const { fetchBarItems, getItemPrice } = useBarItemsStore();
	const { addItemQuantityToOrder } = useBarReceiptsStore();

	fetchBarItems();
</script>

<template>
	<div v-if="loading" class="col-auto row q-pa-md q-col-gutter-md">
		<div
			class="col-6 col-md-3 col-lg-2"
			v-for="n in 10"
			v-bind:key="n"
		>
			<q-skeleton
				type="QBtn"
				animation="fade"
				height="10em"
				width="100%"
			/>
		</div>
	</div>
	<div v-if="!loading && !error && filteredItems.length" class="col-auto row q-pa-md q-col-gutter-md">
		<div v-for="item in filteredItems" :key="item.id" class="col-6 col-md-3 col-lg-2">
			<q-btn
				outline
				no-caps
				:class="{'bar-item': true, 'unavailable': !item.available, 'in-order': orderItemCatalog[item.id]}"
				:disable="!item.available"
				@click="addItemQuantityToOrder(item.id)"
			>
				<div class="col">
					<div v-if="!item.available">(Niedostępne)</div>
					<div>{{ item.name }}</div>
					<div><span v-if="orderItemCatalog[item.id]">{{ orderItemCatalog[item.id] }} x </span>{{ $currency(getItemPrice(item)) }}</div>
				</div>
			</q-btn>
		</div>
	</div>
	<EmptyComponent
		v-if="!loading && !error && !filteredItems.length"
		icon="search"
		primary="Brak produktów!"
		secondary="W podanym filtrze nie znaleziono żadnych produktów."
	/>
</template>

<style lang="scss">
	.bar-item {
		width: 100%;
		height: 10em;
		color: $grey-9;

		& .q-btn__content {
			color: white;
		}

		&.q-btn--outline.in-order::before {
			border-color: $primary;
		}
	}
</style>
