<script setup lang="ts">
	import { storeToRefs } from 'pinia';
	import { useBarReceiptsStore } from 'stores/BarReceipts';
	import { ref } from 'vue';
	import BarReceiptHistoryDialog from 'components/BarReceiptHistoryDialog.vue';
	import BarAddCreditsDialog from 'components/BarAddCreditsDialog.vue';

	const {
		orderAccount,
		basicInfoLoading,
		basicInfo,
		basicInfoError,
		accountList,
	} = storeToRefs(useBarReceiptsStore());
	const { fetchAccountBasicInfo, fetchFilteredAccountList } = useBarReceiptsStore();

	const options = ref([]);
	const receiptHistoryDialog = ref(false);
	const addCreaditsDialog = ref(false);

	async function fetchAccountListFilter(val, update, abort) {
		if (!val.length) {
			abort();
			return;
		}

		await fetchFilteredAccountList(val);

		update(() => {
			options.value = accountList.value;
		})
	}
</script>

<template>
	<q-select
		clearable
		rounded
		outlined
		dense
		use-input
		hide-selected
		fill-input
		hide-bottom-space
		hide-dropdown-icon
		v-model="orderAccount"
		label="Rachunek Uczestnika"
		placeholder="ID lub nazwa Uczestnika"
		:loading="basicInfoLoading"
		:options="options"
		@filter="fetchAccountListFilter"
		@update:model-value="fetchAccountBasicInfo"
		input-debounce="500"
		class="q-mx-md q-mt-md"
		:class="{'q-mb-md': !basicInfoError  && !basicInfo, 'q-mb-sm': !!basicInfoError}"
		:error="!!basicInfoError"
	>
		<template #prepend>
			<q-icon name="badge" />
		</template>
		<template #no-option>
			<q-item>
				<q-item-section class="text-grey">
					Brak uczestników do wyświetlenia
				</q-item-section>
			</q-item>
		</template>
	</q-select>
	<div v-if="basicInfoError" class="text-center q-mb-sm text-red">
		<div>Uczestnik nie ma otwartego rachunku!</div>
		<q-btn text-color="grey-5" @click="addCreaditsDialog = true">Otwórz rachunek</q-btn>
	</div>
	<div v-if="basicInfo" class="row flex-center text-center vertical-middle">
		<div class="col-7">Stan rachunku: {{ $currency(basicInfo.balance) }} / {{ $currency(basicInfo.credits) }}</div>
		<q-separator vertical inset />
		<div class="col">Ceny obsługi: <q-icon :name="basicInfo.isStaff ? 'check_circle' : 'clear'" /></div>
		<q-separator vertical inset />
		<div class="col-auto q-pa-sm">
			<q-btn
				@click="receiptHistoryDialog = true"
				icon="manage_accounts"
				no-caps
				round
				flat
				color="grey-5"
				size="1.25rem"
			>
			</q-btn>
		</div>
	</div>
	<q-separator />

	<BarReceiptHistoryDialog v-model="receiptHistoryDialog" @add-credits-dialog-request="addCreaditsDialog = true"/>
	<BarAddCreditsDialog v-model="addCreaditsDialog" />
</template>
