<script setup lang="ts">
	import { storeToRefs } from 'pinia';
	import { useBarReceiptsStore } from 'stores/BarReceipts';
	import { computed, ref } from 'vue';
	import BarReceiptHistoryDialog from 'components/BarReceiptHistoryDialog.vue';
	import BarAddCreditsDialog from 'components/BarAddCreditsDialog.vue';
  import BarAccountStateDialog from 'components/BarAccountStateDialog.vue';
	import { useAuthStore } from 'stores/AuthStore';

	
  const props = defineProps({
		basicView: {
			type: Boolean,
			required: false,
		},
	});

  const {
		orderAccount,
		basicInfoLoading,
		basicInfo,
		basicInfoError,
		accountList,
	} = storeToRefs(useBarReceiptsStore());
	const { fetchAccountBasicInfo, fetchFilteredAccountList } =
		useBarReceiptsStore();
	const { hasPermission } = useAuthStore();

	const options = ref([]);
	const receiptHistoryDialog = ref(false);
	const addCreditsDialog = ref(false);
  const addAccountStateDialog = ref(false);
  const valAccountStateDialog = ref("");
	const isAllowed = computed(() => hasPermission('logistyka'));

	async function fetchAccountListFilter(val, update, abort) {
		if (!val.length) {
			abort();
			return;
		}

		await fetchFilteredAccountList(val);

		update(() => {
			options.value = accountList.value;
		});
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
		:class="{
			'q-mb-md': !basicInfoError && !basicInfo,
			'q-mb-sm': !!basicInfoError,
		}"
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
	<div v-if="basicInfoError||basicInfo?.state===0" class="text-center q-mb-sm text-red">
		<div>Uczestnik nie ma otwartego rachunku!</div>
		<q-btn
			v-if="isAllowed"
			text-color="grey-5"
			@click="addCreditsDialog = true"
			>Otwórz rachunek</q-btn
		>
		<div v-else class="text-center q-my-sm text-red">
			Nie masz uprawnień do otwarcia rachunku!
		</div>
	</div>
  <div v-if="basicInfo?.state==2" class="text-center q-mb-sm text-red">
    <div>Uczestnik ma zamkniety rachunku!</div>
		<q-btn
			v-if="isAllowed"
			text-color="grey-5"
			@click="valAccountStateDialog = 'open'; addAccountStateDialog = true;"
			>Otwórz ponownie rachunek</q-btn
		>
		<div v-else class="text-center q-my-sm text-red">
			Nie masz uprawnień do otwarcia rachunku!
		</div>
  </div>
	<div v-if="basicInfo?.state==1" class="row text-center">
		<div class="col row flex-center" style="height: 100%">
			<div class="col-12 col-sm-7">
				Stan rachunku: {{ $currency(basicInfo.balance) }} /
				{{ $currency(basicInfo.credits) }}
			</div>
			<q-separator vertical inset class="gt-xs" v-if="!basicView"/>
			<div class="col-12 col-sm" v-if="!basicView">
				Ceny obsługi:
				<q-icon :name="basicInfo.isStaff ? 'check_circle' : 'clear'" />
			</div>
		</div>
		<q-separator vertical inset v-if="!basicView"/>
		<div class="col-auto q-pa-sm" v-if="!basicView">
			<q-btn
				@click="receiptHistoryDialog = true"
				icon="auto_stories"
				no-caps
				round
				flat
				color="grey-5"
				size="1rem"
			/>
		</div>
    <div v-if="!basicView">
      <q-btn
			  v-if="isAllowed"
			  text-color="grey-5"
			  @click="valAccountStateDialog = 'close'; addAccountStateDialog = true;"
      >Zamknij rachunek</q-btn>
  </div>
	</div>

	<BarReceiptHistoryDialog
		v-model="receiptHistoryDialog"
		@add-credits-dialog-request="addCreditsDialog = true"
	/>
	<BarAddCreditsDialog v-model="addCreditsDialog" />
  <BarAccountStateDialog v-model="addAccountStateDialog" :action="valAccountStateDialog" />
</template>
