<script setup lang="ts">
	import { storeToRefs } from 'pinia';
	import { useBarReceiptsStore } from 'stores/BarReceipts';

	const {
		orderAccount,
		basicInfoLoading,
		basicInfo,
		basicInfoError,
	} = storeToRefs(useBarReceiptsStore());
	const { fetchAccountBasicInfo } = useBarReceiptsStore();

</script>

<template>
	<q-input
		clearable
		rounded
		outlined
		dense
		v-model="orderAccount"
		label="Rachunek Uczestnika"
		placeholder="ID Uczestnika"
		:loading="basicInfoLoading"
		@update:model-value="fetchAccountBasicInfo"
		debounce="500"
		class="q-mx-md q-mt-md"
		:class="{'q-mb-md': !basicInfoError  && !basicInfo, 'q-mb-sm': !!basicInfoError}"
		hide-bottom-space
		:error="!!basicInfoError"
		error-message="Nie znaleziono uczestnika!"
	>
		<template #prepend>
			<q-icon name="badge" />
		</template>
	</q-input>
	<div v-if="basicInfo" class="row flex-center text-center">
		<div class="col">Uczestnik: {{ basicInfo.nick }}</div>
		<q-separator vertical inset />
		<div class="col">{{ basicInfo.balance }} zl / {{ basicInfo.credits }} zl</div>
		<q-separator vertical inset />
		<div class="col">Ceny obsługi: <q-icon :name="basicInfo.isStaff ? 'check_circle' : 'clear'" /></div>
	</div>
	<q-separator />
</template>
