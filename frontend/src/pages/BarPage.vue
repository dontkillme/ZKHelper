<script setup lang="ts">
	import BarPin from 'components/BarPin.vue';
	import BarCategories from 'components/BarCategories.vue';
	import BarItems from 'components/BarItems.vue';
	import BarReceiptItems from 'components/BarReceiptItems.vue';
	import BarReceiptAccount from 'components/BarReceiptAccount.vue';
	import BarItemsSearch from 'components/BarItemsSearch.vue';

	import { ref } from 'vue';
	import { storeToRefs } from 'pinia';
	import { useBarAuthStore } from 'stores/BarAuth';
	import { useBarReceiptsStore } from 'stores/BarReceipts';

	const { isAuthenticated } = storeToRefs(useBarAuthStore());
	const { hasAnyItemsInOrder } = storeToRefs(useBarReceiptsStore());
	const { clearOrder } = useBarReceiptsStore();

	const orderClearConfirm = ref(false);
</script>

<template>
	<q-page>
		<BarPin v-if="!isAuthenticated"/>

		<div class="column" style="height: 100%;">
			<div v-if="isAuthenticated" class="col-12 row">
				<div class="col">
					<div class="column" style="height: 100%">
						<BarCategories />
						<BarItemsSearch />
						<BarItems />
					</div>
				</div>
				<q-separator vertical />
				<div class="col-4">
					<div class="column" style="height: 100%;">
						<q-list separator>
							<q-item-label header>
								<div class="row flex-center">
									<div class="col">
										Zamówienie
									</div>
									<div class="col-auto">
										<q-btn
											:class="{'hide-button': !hasAnyItemsInOrder}"
											@click="orderClearConfirm = true"
										>
											Wyczyść zamówienie
										</q-btn>
									</div>
								</div>
							</q-item-label>
						</q-list>
						<q-separator />
						<BarReceiptAccount />
						<BarReceiptItems />
					</div>
				</div>
			</div>
		</div>
	</q-page>

	<q-dialog v-model="orderClearConfirm">
		<q-card>
			<q-card-section>
				<div class="text-h6">Czy na pewno chcesz wyczyścić zamówienie?</div>
			</q-card-section>

			<q-card-actions align="right">
				<q-btn flat label="Anuluj" color="primary" v-close-popup />
				<q-btn flat label="Wyczyść zamówienie" color="primary" v-close-popup @click="clearOrder" />
			</q-card-actions>
		</q-card>
	</q-dialog>
</template>

<style lang="scss">
	.hide-button {
		visibility: hidden;
	}
</style>
