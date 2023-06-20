<script setup lang="ts">
	import { computed, ref } from 'vue';
	import { useBarReceiptsStore } from 'stores/BarReceipts';
	import { useQuasar } from 'quasar';

	const props = defineProps({
		modelValue: {
			type: Boolean,
			required: true,
		},
    action: {type: String, required: true}
	});

	const emit = defineEmits(['update:modelValue']);

	const dialogState = computed({
		get: () => props.modelValue,
		set: (dialogState) => emit('update:modelValue', dialogState),
	});

  const inferring = ref();
	const sending = ref(false);

	const { changeAccountState, fetchAccountBasicInfo } = useBarReceiptsStore();
	const $q = useQuasar();

	async function onSubmit() {
		sending.value = true;

		try {
			await changeAccountState(props.action, inferring.value);
		} catch (error) {
			$q.notify({
				type: 'negative',
				caption: error.message.replace(/\n/, '<br>'),
				html: true,
				message: 'Błąd przy zmianie stanu rachunku!',
				actions: [{ icon: 'close', color: 'white' }],
			});

			sending.value = false;
			return;
		}

		$q.notify({
			type: 'positive',
			caption: 'Aktualizowano.',
			message: 'Sukces!',
			actions: [{ icon: 'close', color: 'white' }],
		});

		await fetchAccountBasicInfo();

		sending.value = false;
		dialogState.value = false;
	}
</script>

<template>
	<q-dialog v-model="dialogState">
		<q-card style="min-width: 350px">
			<q-form
				@submit="onSubmit"
				autocorrect="off"
				autocapitalize="off"
				autocomplete="off"
				spellcheck="false"
			>
				<q-card-section>
					<div class="text-h6">Podaj swój ID</div>
				  <q-input
						v-model="inferring"
						type="number"
            label="ID wprowadzającego"
						dense
						autofocus
						lazy-rules
						:rules="[
							(val) =>
								(val !== null && val !== '' && !isNaN(val)) ||
								'Podaj poprawny ID',
						]"/>
				</q-card-section>
				<q-card-actions align="right" class="text-primary">
					<q-btn flat label="Anuluj" v-close-popup />
					<q-btn
						flat
						type="submit"
						:label="[action=='open' ? 'Otworz ponownie' : 'Zamknij rachunek']"
            :loading="sending"
						:disable="!inferring"
					/>
				</q-card-actions>
			</q-form>
		</q-card>
	</q-dialog>
</template>
