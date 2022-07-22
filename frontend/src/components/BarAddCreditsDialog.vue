<script setup lang="ts">
	import { computed, ref } from 'vue';
	import { useBarReceiptsStore } from 'stores/BarReceipts';
	import { useQuasar } from 'quasar';

	const props = defineProps({
		modelValue: {
			type: Boolean,
			required: true,
		},
	});
	const emit = defineEmits(['update:modelValue'])

	const dialogState = computed({
		get: () => props.modelValue,
		set: (dialogState) => emit('update:modelValue', dialogState)
	});

	const amount = ref(10);
	const sending = ref(false);

	const { addCredits, fetchAccountBasicInfo } = useBarReceiptsStore();
	const $q = useQuasar();

	async function onSubmit() {
		sending.value = true;

		try {
			await addCredits(amount.value);
		}
		catch (error) {
			$q.notify({
				type: 'negative',
				caption: error.message.replace(/\n/, '<br>'),
				html: true,
				message: 'Błąd wpłacania środków!',
				actions: [
					{icon: 'close', color: 'white'}
				]
			})

			sending.value = false;
			return;
		}

		$q.notify({
			type: 'positive',
			caption: 'Kwota wpłacona na rachunek.',
			message: 'Sukces!',
			actions: [
				{icon: 'close', color: 'white'}
			]
		})

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
					<div class="text-h6">Podaj kwotę do wpłacenia</div>
				</q-card-section>

				<q-card-section class="q-pt-none">
					<q-input
						v-model="amount"
						type="number"
						min="1"
						dense
						autofocus
						lazy-rules
						:rules="[
							val => val !== null && val !== '' && !isNaN(val) || 'Podaj poprawną kwotę',
						]"
					/>
				</q-card-section>

				<q-card-actions align="right" class="text-primary">
					<q-btn flat label="Anuluj" v-close-popup />
					<q-btn
						flat
						label="Wpłać środki"
						type="submit"
						:loading="sending"
						:disable="!amount"
					/>
				</q-card-actions>
			</q-form>
		</q-card>
	</q-dialog>
</template>
