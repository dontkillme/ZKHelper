<script setup lang="ts">
	import EmptyComponent from 'components/EmptyComponent.vue'
	import { storeToRefs } from 'pinia';
	import { useBarReceiptsStore } from 'stores/BarReceipts';
	import { useBarItemsStore } from 'stores/BarItems';

	const {
		orderItems,
		sending,
		hasAnyItemsInOrder,
		orderStaffPrices,
		orderTotal,
		basicInfo,
	} = storeToRefs(useBarReceiptsStore());
	const { getItemPrice } = useBarItemsStore();
	const { itemCatalog } = storeToRefs(useBarItemsStore());
	const { addItemQuantityToOrder, takeItemQuantityToOrder, createBarReceipt } = useBarReceiptsStore();
</script>

<template>
	<q-list separator>
		<q-item-label header>
			<div class="row flex-center">
				<div class="col">
					Produkty
				</div>
				<div class="col-auto">
					<q-toggle
						v-model="orderStaffPrices"
						:disable="basicInfo?.isStaff"
						checked-icon="check"
						color="green"
						unchecked-icon="clear"
						label="Ceny obsługi"
					/>
				</div>
			</div>
		</q-item-label>
	</q-list>
	<q-separator />
	<EmptyComponent
		v-if="!hasAnyItemsInOrder"
		icon="shopping_cart"
		primary="Brak produktów!"
		secondary="Dodaj produkty klikając na kafelki obok."
	/>
	<q-scroll-area
		v-if="hasAnyItemsInOrder"
		visible
		class="col"
	>
		<q-list separator>
			<q-item v-for="orderItem in orderItems" :key="orderItem.itemId">
				<q-item-section class="col-auto">{{ orderItem.quantity }}</q-item-section>
				<q-item-section class="col-auto">x</q-item-section>
				<q-item-section no-wrap>{{ itemCatalog[orderItem.itemId].name }}</q-item-section>
				<q-item-section no-wrap class="text-secondary col-auto">{{ orderItem.quantity }} x {{ $currency(getItemPrice(itemCatalog[orderItem.itemId])) }} = </q-item-section>
				<q-item-section class="col-auto">{{ $currency(getItemPrice(itemCatalog[orderItem.itemId]) * orderItem.quantity) }}</q-item-section>
				<q-item-section side>
					<div class="text-grey-8 q-gutter-xs">
						<q-btn size="1.25rem" flat dense round icon="remove" @click="takeItemQuantityToOrder(orderItem.itemId)" />
						<q-btn size="1.25rem" flat dense round icon="add" @click="addItemQuantityToOrder(orderItem.itemId)" />
					</div>
				</q-item-section>
			</q-item>
			<q-separator />
		</q-list>
	</q-scroll-area>
	<div class="col-auto">
		<q-btn
			v-if="hasAnyItemsInOrder"
			color="primary"
			size="lg"
			class="full-width"
			@click="createBarReceipt"
			:loading="sending"
		>
			<template v-if="basicInfo">
				Zamów na {{ $currency(orderTotal) }} zł na rachunek
			</template>
			<template v-else>
				Zamów na {{ $currency(orderTotal) }} zł w gotówce
			</template>
		</q-btn>
	</div>
</template>

<style lang="scss">
	.q-list--dark.q-list--separator > .q-item-type + .q-item-type {
		border-top-color: #424242;
	}
</style>
