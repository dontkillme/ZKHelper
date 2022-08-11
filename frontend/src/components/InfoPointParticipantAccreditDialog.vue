<script setup lang="ts">
	import { computed, ref } from 'vue';
	import { useQuasar } from 'quasar';

	const props = defineProps({
		modelValue: {
			type: Boolean,
			required: true,
		},
		participant: {
			type: Object,
		},
	});
	const emit = defineEmits(['update:modelValue']);

	const dialogState = computed({
		get: () => props.modelValue,
		set: (dialogState) => emit('update:modelValue', dialogState),
	});

	const $q = useQuasar();

	import { useParticipantsStore } from 'stores/ParticipantsStore';
	const { accreditParticipant } = useParticipantsStore();

	const sending = ref(false);

	async function onSubmit() {
		sending.value = true;

		try {
			await accreditParticipant(props.participant.id);
		} catch (error) {
			$q.notify({
				type: 'negative',
				caption: error.message.replace(/\n/, '<br>'),
				html: true,
				message: 'Błąd akredytowania uczestnika!',
				actions: [{ icon: 'close', color: 'white' }],
			});

			sending.value = false;
			dialogState.value = false;
			return;
		}

		$q.notify({
			type: 'positive',
			caption: 'Uczestnik zaakredytowany.',
			message: 'Sukces!',
			actions: [{ icon: 'close', color: 'white' }],
		});

		sending.value = false;
		dialogState.value = false;
	}
</script>

<template>
	<q-dialog v-model="dialogState">
		<q-card>
			<q-card-section>
				<div class="text-h6">
					Czy na pewno chcesz zaakredytować
					{{ participant.nick }} (#{{ participant.id }})?
				</div>
			</q-card-section>

			<q-card-actions align="right">
				<q-btn flat label="Anuluj" color="primary" v-close-popup />
				<q-btn
					flat
					label="Zaakredytuj"
					color="primary"
					:loading="sending"
					@click="onSubmit"
				/>
			</q-card-actions>
		</q-card>
	</q-dialog>
</template>
