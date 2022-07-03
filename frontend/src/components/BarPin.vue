<script setup lang="ts">
	import { storeToRefs } from 'pinia';
	import { useBarAuthStore } from 'stores/BarAuth';
	import { ref } from 'vue';
	import { useQuasar } from 'quasar';

	const { sending, error } = storeToRefs(useBarAuthStore());
	const { login } = useBarAuthStore();
	const $q = useQuasar();

	const pin = ref<string | null>(null);

	async function loginAction() {
		if (pin.value) {
			await login(Number(pin.value));

			if (error.value) {
				$q.notify({
					type: 'negative',
					caption: error.value,
					message: 'Błąd logowania!',
					actions: [
						{icon: 'close', color: 'white'}
					]
				})
			}
		}
	}
</script>

<template>
	<q-form
		class="absolute-center text-center q-gutter-md"
		autocorrect="off"
		autocapitalize="off"
		autocomplete="off"
		spellcheck="false"
		@submit="loginAction"
	>
		<q-icon name="lock" size="100px" color="gray-5" />
		<div class="text-h3">Podaj PIN</div>
		<div class="text-secondary q-mb-lg">Obsługa baru potrzebuje użyć osobistego PINu, by móc składać zamówienia.</div>
		<q-input
			v-model="pin"
			placeholder="PIN będzie zagwiazdkowany"
			rounded
			outlined
			dense
			clearable
			:disable="sending"
			type="password"
			input-class="text-center"
			inputmode="numeric"
			:rules="[ val => val && 0 < val.length || 'Pin jest wymagany!']"
		>
			<template #prepend>
				<q-icon name="lock" />
			</template>
		</q-input>
		<q-btn
			type="submit"
			label="Zaloguj"
			outline
			no-caps
			class="text-grey-5"
			:loading="sending"
			:disable="!pin"
		/>
	</q-form>
</template>
