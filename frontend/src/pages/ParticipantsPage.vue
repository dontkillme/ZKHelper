<script setup lang="ts">
	import PinComponent from 'components/PinComponent.vue';
	import { computed } from 'vue';
	import { storeToRefs } from 'pinia';
	import { useAuthStore } from 'stores/AuthStore';
	import EmptyComponent from 'components/EmptyComponent.vue';
	import InfoPointParticipants from 'components/InfoPointParticipants.vue';

	const { hasPermission } = useAuthStore();
	const { isAuthenticated } = storeToRefs(useAuthStore());

	const isAllowed = computed(() => hasPermission('infopoint'));
</script>

<template>
	<q-page>
		<PinComponent
			v-if="!isAuthenticated"
			label="Obsługa uczestników potrzebuje użyć osobistego PINu, by móc ich akredytować."
		/>

		<EmptyComponent
			v-if="isAuthenticated && !isAllowed"
			icon="block"
			primary="Brak uprawnień!"
			secondary="Nie masz dostępu do części info pointowej aplikacji."
		/>

		<InfoPointParticipants v-if="isAuthenticated && isAllowed" />
	</q-page>
</template>
