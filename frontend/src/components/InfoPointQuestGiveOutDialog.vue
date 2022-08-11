<script setup lang="ts">
	import { computed, ref } from 'vue';
	import { useQuasar } from 'quasar';
	import { storeToRefs } from 'pinia';
	import removeAccents from 'remove-accents';

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
	const { giveOutParticipantQuest } = useQuestsStore();
	const { quests } = storeToRefs(useQuestsStore());

	const sending = ref(false);
	const quest = ref(null);
	const options = ref([]);

	async function onSubmit() {
		sending.value = true;

		try {
			await giveOutParticipantQuest(quest.value.id);
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

	function questsFilter(val, update) {
		if (!val.length) {
			update(() => {
				options.value = quests.value;
			});

			return;
		}

		if (isNaN(val)) {
			update(() => {
				const words = removeAccents(val)
					.toLowerCase()
					.split(' ');

				options.value = quests.value.filter((element) => {
					const normalizedName = removeAccents(
						element.name
					).toLowerCase();
					return words.every(
						(word) => normalizedName.indexOf(word) !== -1
					);
				});
			});
		}
		else {
			update(() => {
				options.value = quests.value.filter((element) => {
					return element.id == val;
				})
			});
		}
	}
</script>

<template>
	<q-dialog v-model="dialogState" @before-show="quest = null">
		<q-card>
			<q-card-section>
				<div class="text-h6">
					Wybierz questa do wydania
				</div>
			</q-card-section>

			<q-card-section class="q-pt-none">
				<q-select
					clearable
					rounded
					outlined
					dense
					use-input
					hide-selected
					fill-input
					hide-bottom-space
					hide-dropdown-icon
					v-model="quest"
					label="Quest"
					placeholder="ID lub nazwa questa"
					:options="options"
					:option-label="(item) => `${item.name} (#${item.id})`"
					@filter="questsFilter"
				>
					<template #prepend>
						<q-icon name="done_outline" />
					</template>
					<template #no-option>
						<q-item>
							<q-item-section class="text-grey">
								Brak questów do wyświetlenia
							</q-item-section>
						</q-item>
					</template>
					<template #option="scope">
						<q-item v-bind="scope.itemProps">
							<q-item-section>
								<q-item-label>{{ scope.opt.name }} (#{{ scope.opt.id }})</q-item-label>
								<q-item-label caption>{{ scope.opt.description }}</q-item-label>
							</q-item-section>
						</q-item>
					</template>
				</q-select>
			</q-card-section>

			<q-card-actions align="right">
				<q-btn flat label="Anuluj" color="primary" v-close-popup />
				<q-btn
					flat
					label="Wydaj"
					color="primary"
					:loading="sending"
					@click="onSubmit"
				/>
			</q-card-actions>
		</q-card>
	</q-dialog>
</template>
