<script setup lang="ts">
	import { storeToRefs } from 'pinia/dist/pinia';
	import { useBarAuthStore } from '../stores/BarAuth';

	const { participantNick, isAuthenticated } = storeToRefs(useBarAuthStore());
	const { logout } = useBarAuthStore();
</script>

<template>
	<div v-if="isAuthenticated">
		<span class="q-mr-md">Zalogowano jako {{ participantNick }}</span>
		<q-btn @click="logout">Wyloguj</q-btn>
	</div>
</template>
