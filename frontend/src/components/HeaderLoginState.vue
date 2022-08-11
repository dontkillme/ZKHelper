<script setup lang="ts">
	import { storeToRefs } from 'pinia/dist/pinia';
	import { useAuthStore } from 'stores/AuthStore';

	const { participantNick, isAuthenticated } = storeToRefs(useAuthStore());
	const { logout } = useAuthStore();
</script>

<template>
	<div v-if="isAuthenticated">
		<span class="q-mr-lg">Zalogowano jako {{ participantNick }}</span>
		<q-btn flat @click="logout">Wyloguj</q-btn>
	</div>
</template>
