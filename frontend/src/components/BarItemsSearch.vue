<script setup lang="ts">
	import { storeToRefs } from 'pinia';
	import { useBarItemsStore } from 'stores/BarItems';

	const { searchFilter } = storeToRefs(useBarItemsStore());
</script>

<template>
	<q-input
		v-model="searchFilter"
		placeholder="Szukaj po nazwie produktów"
		class="q-mx-md q-mt-md"
		clearable
		rounded
		outlined
		dense
	>
		<template #prepend>
			<q-icon name="search" />
		</template>
	</q-input>
</template>

<style lang="scss">
	.outlined {
		border-bottom: 1px solid $grey-9;

		& + & {
			border-left: 1px solid $grey-9;
		}
	}
</style>
