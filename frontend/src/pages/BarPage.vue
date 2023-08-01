<script setup lang="ts">
	import PinComponent from 'components/PinComponent.vue';
	import BarCategories from 'components/BarCategories.vue';
	import BarItems from 'components/BarItems.vue';
	import BarReceiptItems from 'components/BarReceiptItems.vue';
	import BarReceiptAccount from 'components/BarReceiptAccount.vue';
	import BarItemsSearch from 'components/BarItemsSearch.vue';
  import BarOrderDialog from 'components/BarOrderDialog.vue';

	import { computed, ref } from 'vue';
	import { storeToRefs } from 'pinia';
	import { useAuthStore } from 'stores/AuthStore';
	import { useBarReceiptsStore } from 'stores/BarReceipts';
	import EmptyComponent from 'components/EmptyComponent.vue';
import BarLatestReceiptList from 'src/components/BarLatestReceiptList.vue';
  

	const { hasPermission } = useAuthStore();
	const { isAuthenticated } = storeToRefs(useAuthStore());
	const { hasAnyItemsInOrder } = storeToRefs(useBarReceiptsStore());
	const { clearOrder } = useBarReceiptsStore();

	const orderClearConfirm = ref(false);
  const showOrderDialog = ref(false);
  const showLatestReceiptDialog = ref(false);
	const isAllowed = computed(
		() => hasPermission('bar') || hasPermission('logistyka')
	);
</script>

<template>
	<q-page>
		<PinComponent
			v-if="!isAuthenticated"
			label="Obsługa baru potrzebuje użyć osobistego PINu, by móc składać zamówienia."
		/>

		<EmptyComponent
			v-if="isAuthenticated && !isAllowed"
			icon="block"
			primary="Brak uprawnień!"
			secondary="Nie masz dostępu do części barowej aplikacji."
		/>

		<div
			v-if="isAuthenticated && isAllowed"
			class="column"
			style="height: 100%"
		>
    <q-page-container>
			<div class="col-12 row">
				<div class="col-12 col-md-6">					
          <div>
            <q-page-sticky position="top" style="zIndex: 100; background:#121212; paddingTop:1rem; paddingBottom:1rem;">
              <div class="row" >
                <div class="col-auto">
                  <q-btn
                    color="primary"
                    size="lg"
                    @click="showOrderDialog=true"
                    :disabled="!hasAnyItemsInOrder"
                  >Zamówienie</q-btn>
                </div>
                <div class="col-auto">
                  <q-btn
                    color="warning"
                    size="lg"
                    @click="orderClearConfirm = true"
                    :disabled="!hasAnyItemsInOrder"
                  >
                    Wyczyść zamówienie
                  </q-btn>
                </div>
                <div class="col-auto">
                  <q-btn
                    color="primary"
                    size="lg"
                    @click="showLatestReceiptDialog = true"
                  >
                    Ostatnie zamówienia
                  </q-btn>
                </div>
              </div>
            </q-page-sticky>
						<BarItems />
					</div>
				</div>
				<q-separator vertical class="gt-sm" />
				<div class="col-12 col-md">
					<div class="column" style="height: 100%">
						<BarReceiptAccount />
					</div>
				</div>
			</div>
    </q-page-container>
		</div>
	</q-page>

  <BarOrderDialog v-model="showOrderDialog" />
  <BarLatestReceiptList v-model="showLatestReceiptDialog" />
	<q-dialog v-model="orderClearConfirm">
		<q-card>
			<q-card-section>
				<div class="text-h6">
					Czy na pewno chcesz wyczyścić zamówienie?
				</div>
			</q-card-section>

			<q-card-actions align="right">
				<q-btn flat label="Anuluj" color="primary" v-close-popup />
				<q-btn
					flat
					label="Wyczyść zamówienie"
					color="primary"
					v-close-popup
					@click="clearOrder"
				/>
			</q-card-actions>
		</q-card>
	</q-dialog>
</template>
