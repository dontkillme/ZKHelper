<script setup lang="ts">
	import { ref } from 'vue';
	import EmptyComponent from 'components/EmptyComponent.vue'
	import { storeToRefs } from 'pinia';
	import { useBarReceiptsStore } from 'stores/BarReceipts';
	import { useBarItemsStore } from 'stores/BarItems';
	import { useQuasar } from 'quasar';

	const {
		orderItems,
		hasAnyItemsInOrder,
		orderStaffPrices,
		orderTotal,
		basicInfo,
	} = storeToRefs(useBarReceiptsStore());
	const $q = useQuasar();
	const { getItemPrice } = useBarItemsStore();
	const { itemCatalog } = storeToRefs(useBarItemsStore());
	const { addItemQuantityToOrder, takeItemQuantityToOrder, createBarReceipt } = useBarReceiptsStore();

	const sending = ref(false);

	async function onSubmit() {
		sending.value = true;

		try {
			await createBarReceipt();
		}
		catch (error) {
			$q.notify({
				type: 'negative',
				caption: error.message.replace(/\n/, '<br>'),
				html: true,
				message: 'Błąd składania zamówienia!',
				actions: [
					{icon: 'close', color: 'white'}
				]
			})

			sending.value = false;
			return;
		}

		$q.notify({
			type: 'positive',
			caption: 'Zamówienie złożone.',
			message: 'Sukces!',
			actions: [
				{icon: 'close', color: 'white'}
			]
		})

		sending.value = false;
	}
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
		class="q-my-md gt-sm"
	/>
	<EmptyComponent
		v-if="!hasAnyItemsInOrder"
		icon="shopping_cart"
		primary="Brak produktów!"
		secondary="Dodaj produkty klikając na kafelki powyżej."
		class="q-my-md lt-md"
	/>
	<q-scroll-area
		v-if="hasAnyItemsInOrder"
		visible
		class="col"
		style="min-height: 18rem;"
	>
		<q-list separator>
			<q-item v-for="orderItem in orderItems" :key="orderItem.itemId">
				<q-item-section class="col-auto">{{ orderItem.quantity }}</q-item-section>
				<q-item-section class="col-auto">x</q-item-section>
				<q-item-section no-wrap>{{ itemCatalog[orderItem.itemId].name }}</q-item-section>
				<q-item-section no-wrap class="text-secondary col-auto">{{ orderItem.quantity }} x {{ $currency(getItemPrice(itemCatalog[orderItem.itemId])) }} = </q-item-section>
				<q-item-section class="col-auto">{{ $currency(getItemPrice(itemCatalog[orderItem.itemId]) * orderItem.quantity) }}</q-item-section>
				<q-item-section side>
					<div class="text-grey-5 q-gutter-xs">
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
			@click="onSubmit"
			:loading="sending"
		>
			<template v-if="basicInfo">
				Zamów za {{ $currency(orderTotal) }} na rachunek
			</template>
			<template v-else>
				Zamów za {{ $currency(orderTotal) }} w gotówce
			</template>
		</q-btn>
	</div>
</template>

<style lang="scss">
	.q-list--dark.q-list--separator > .q-item-type + .q-item-type {
		border-top-color: #424242;
	}
</style>
