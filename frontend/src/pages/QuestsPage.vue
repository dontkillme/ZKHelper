<script setup lang="ts">
	import PinComponent from 'components/PinComponent.vue';
	import { computed } from 'vue';
	import { storeToRefs } from 'pinia';
	import { useAuthStore } from 'stores/AuthStore';
	import EmptyComponent from 'components/EmptyComponent.vue';
	import InfoPointQuests from 'components/InfoPointQuests.vue';

	const { hasPermission } = useAuthStore();
	const { isAuthenticated } = storeToRefs(useAuthStore());

	const isAllowed = computed(
		() => hasPermission('infopoint') || hasPermission('bar')
	);
</script>

<template>
	<q-page>
		<PinComponent
			v-if="!isAuthenticated"
			label="Obsługa questów potrzebuje użyć osobistego PINu, by móc obsługiwać questy uczestników."
		/>

		<EmptyComponent
			v-if="isAuthenticated && !isAllowed"
			icon="block"
			primary="Brak uprawnień!"
			secondary="Nie masz dostępu do części questowej aplikacji."
		/>

		<InfoPointQuests v-if="isAuthenticated && isAllowed" />
	</q-page>
</template>
