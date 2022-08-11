<script setup lang="ts">
	import { computed } from 'vue';
	import { storeToRefs } from 'pinia';
	import { useBarReceiptsStore } from 'stores/BarReceipts';
	import { useAuthStore } from 'stores/AuthStore';
	import { date } from 'quasar';
	import EmptyComponent from 'components/EmptyComponent.vue';

	const props = defineProps({
		modelValue: {
			type: Boolean,
			required: true,
		},
	});
	const emit = defineEmits(['addCreditsDialogRequest', 'update:modelValue']);

	const dialogState = computed({
		get: () => props.modelValue,
		set: (dialogState) => emit('update:modelValue', dialogState),
	});

	const {
		basicInfo,
		receiptHistoryListLoading,
		receiptHistoryList,
		orderAccount,
	} = storeToRefs(useBarReceiptsStore());
	const { hasPermission } = useAuthStore();

	const { fetchReceiptHistory } = useBarReceiptsStore();
	const isAllowed = computed(() => hasPermission('logistyka'));
</script>

<template>
	<q-dialog v-model="dialogState" @before-show="fetchReceiptHistory">
		<q-card style="width: 30rem; max-width: 80vw">
			<q-card-section class="row items-center">
				<div class="text-h6">
					Rachunek Uczestnika: {{ orderAccount.label }}
				</div>
				<q-space />
				<q-btn icon="close" flat round dense v-close-popup />
			</q-card-section>

			<q-separator />

			<q-card-section>
				<div class="row justify-between text-center">
					<div class="col-12 col-sm">
						Stan rachunku: {{ $currency(basicInfo.balance) }}
					</div>
					<q-separator vertical class="gt-xs" />
					<div class="col-12 col-sm">
						Wpłacone: {{ $currency(basicInfo.credits) }}
					</div>
				</div>
			</q-card-section>

			<q-separator />

			<q-card-actions vertical>
				<q-btn
					v-if="isAllowed"
					flat
					@click="emit('addCreditsDialogRequest')"
					>Wpłać środki</q-btn
				>
				<div v-else class="text-center q-my-sm text-red">
					Nie masz uprawnień do wpłacania środków!
				</div>
			</q-card-actions>

			<q-separator />

			<q-card-section class="q-pa-none">
				<q-list separator>
					<q-item-label header>Zamówienia</q-item-label>
					<q-separator />
				</q-list>
				<q-list
					v-if="receiptHistoryListLoading"
					separator
					class="scroll"
					style="max-height: 50vh"
				>
					<q-item v-for="n in 3" :key="n">
						<q-skeleton
							animation="fade"
							height="6rem"
							width="100%"
						/>
					</q-item>
				</q-list>
				<q-list
					v-if="!receiptHistoryListLoading"
					separator
					class="scroll"
					style="max-height: 50vh"
				>
					<EmptyComponent
						v-if="
							!receiptHistoryListLoading &&
							!receiptHistoryList.length
						"
						icon="receipt_long"
						primary="Brak zamówień!"
						secondary="Uczestnik nie posiada zamówień na swoim rachunku."
						class="q-my-md"
					/>
					<q-item
						v-for="receipt in receiptHistoryList"
						:key="receipt.id"
					>
						<q-item-section>
							<q-item-label>
								<div class="row justify-between text-body1">
									<div>{{ $currency(receipt.sum) }}</div>
									<div class="text-grey-5">
										{{
											date.formatDate(
												receipt.createdAt,
												'YYYY.MM.DD HH:mm'
											)
										}}
									</div>
								</div>
							</q-item-label>
							<q-item-label
								v-for="item in receipt.items"
								:key="item.id"
							>
								<div class="row justify-between text-body2">
									<div class="col-auto">
										{{ item.quantity }} x {{ item.name }}
									</div>
									<div class="col-auto">
										<span class="text-secondary"
											>{{ item.quantity }} x
											{{ $currency(item.price) }} =</span
										>
										{{
											$currency(
												item.quantity * item.price
											)
										}}
									</div>
								</div>
							</q-item-label>
						</q-item-section>
					</q-item>
				</q-list>
			</q-card-section>
		</q-card>
	</q-dialog>
</template>
