<script setup lang="ts">
	import { computed, ref } from 'vue';
	import { useQuasar } from 'quasar';
	import { storeToRefs } from 'pinia';

	const props = defineProps({
		modelValue: {
			type: Boolean,
			required: true,
		},
		participantQuest: {
			type: Object,
		},
	});
	const emit = defineEmits(['update:modelValue']);

	const dialogState = computed({
		get: () => props.modelValue,
		set: (dialogState) => emit('update:modelValue', dialogState),
	});

	const $q = useQuasar();

	import { useQuestsStore } from 'stores/QuestsStore';
	const { markParticipantQuestDone } = useQuestsStore();
	const { questCatalog } = storeToRefs(useQuestsStore());

	const sending = ref(false);
	const notes = ref(null);

	async function onSubmit() {
		sending.value = true;

		try {
			await markParticipantQuestDone(props.participantQuest.id, notes.value);
		} catch (error) {
			$q.notify({
				type: 'negative',
				caption: error.message.replace(/\n/, '<br>'),
				html: true,
				message: 'Błąd zamykania questa!',
				actions: [{ icon: 'close', color: 'white' }],
			});

			sending.value = false;
			dialogState.value = false;
			return;
		}

		$q.notify({
			type: 'positive',
			caption: 'Quest zamknięty!.',
			message: 'Sukces!',
			actions: [{ icon: 'close', color: 'white' }],
		});

		sending.value = false;
		dialogState.value = false;
	}
</script>

<template>
	<q-dialog v-model="dialogState" @before-show="notes = null">
		<q-card>
			<q-card-section>
				<div class="text-h6">
					Czy na pewno chcesz zakończyć questa {{ questCatalog[participantQuest.questId].name }} (#{{ participantQuest.questId }})?
				</div>
			</q-card-section>

			<q-card-section class="q-pt-none">
				<q-input
					dense
					v-model="notes"
					@keyup.enter="onSubmit"
					label="Opcjonalne uwagi"
				/>
			</q-card-section>

			<q-card-actions align="right">
				<q-btn flat label="Anuluj" color="primary" v-close-popup />
				<q-btn
					flat
					label="Zakończ"
					color="primary"
					:loading="sending"
					@click="onSubmit"
				/>
			</q-card-actions>
		</q-card>
	</q-dialog>
</template>
