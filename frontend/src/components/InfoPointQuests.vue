<script setup lang="ts">
	import { ref } from 'vue';
	import { useQuestsStore } from 'stores/QuestsStore';
	import { storeToRefs } from 'pinia';
	import { date } from 'quasar';
	import EmptyComponent from 'components/EmptyComponent.vue';
	import InfoPointQuestMarkDoneDialog from 'components/InfoPointQuestMarkDoneDialog.vue';
	import InfoPointQuestGiveOutDialog from 'components/InfoPointQuestGiveOutDialog.vue';

	const options = ref([]);
	const questMarkDoneDialog = ref(false);
	const questGiveOutDialog = ref(false);
	const selectedParticipantQuest = ref(null);
	const {
		fetchFilteredAccountOptionList,
		fetchSelectedParticipantQuests,
		fetchQuests,
	} = useQuestsStore();
	const {
		selectedParticipant,
		selectedParticipantQuests,
		filteredAccountOptionList,
		filteredAccountOptionListLoading,
		questCatalog,
		selectedParticipantQuestsLoading,
	} = storeToRefs(useQuestsStore());

	async function fetchParticipantListFilter(val, update, abort) {
		if (!val.length) {
			abort();
			return;
		}

		await fetchFilteredAccountOptionList(val);

		update(() => {
			options.value = filteredAccountOptionList.value;
		});
	}

	selectedParticipant.value = null;
	fetchQuests();
</script>

<template>
	<div class="row justify-center q-py-lg">
		<div class="q-px-md" style="width: 30rem; max-width: 100vw">
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
				v-model="selectedParticipant"
				label="Uczestnik"
				placeholder="ID lub nazwa Uczestnika"
				:loading="filteredAccountOptionListLoading"
				:options="options"
				@filter="fetchParticipantListFilter"
				@update:model-value="fetchSelectedParticipantQuests"
				input-debounce="500"
			>
				<template #prepend>
					<q-icon name="badge" />
				</template>
				<template #no-option>
					<q-item>
						<q-item-section class="text-grey">
							Brak uczestników do wyświetlenia
						</q-item-section>
					</q-item>
				</template>
			</q-select>
		</div>
	</div>
	<div class="row justify-center">
		<div v-if="selectedParticipant" style="width: 30rem; max-width: 100vw">
			<div class="row">
				<q-btn class="col-12" @click="questGiveOutDialog = true">
					Wydaj questa
				</q-btn>
			</div>

			<q-list separator>
				<q-item-label header>Questy</q-item-label>
				<q-separator />
			</q-list>

			<q-list v-if="selectedParticipantQuestsLoading"  separator>
				<q-item
					v-for="n in 3"
					:key="n"
				>
					<q-item-section>
						<q-skeleton
							animation="fade"
							height="3rem"
							width="100%"
						/>
						<q-separator class="q-ma-sm"/>
						<q-skeleton
							animation="fade"
							height="3rem"
							width="100%"
						/>
					</q-item-section>
				</q-item>
			</q-list>
			<q-list
				v-else
				separator
			>
				<EmptyComponent
					v-if="!selectedParticipantQuestsLoading &&!selectedParticipantQuests.length"
					icon="task_alt"
					primary="Brak questów!"
					secondary="Uczestnik nie otrzymał jeszcze żadnego questa."
					class="q-my-md"
				/>
				<q-item
					v-for="participantQuest in selectedParticipantQuests"
					:key="participantQuest.id"
				>
					<q-item-section>
						<q-item-label>
							<div class="row justify-between text-body1">
								<div>{{ questCatalog[participantQuest.questId]?.name }} (#{{ participantQuest.questId }})</div>
								<div class="text-grey-5 text-body2">
									{{ questCatalog[participantQuest.questId]?.reward }} mariuszków
								</div>
							</div>
						</q-item-label>
						<q-item-label>
							<div class="text-secondary text-center">
								{{ questCatalog[participantQuest.questId]?.description }}
							</div>
						</q-item-label>
						<q-item-label>
							<div class="row justify-between text-body2 q-mt-sm">
								<div>
									<div>Wydany: {{ date.formatDate(participantQuest.startedAt, 'YYYY.MM.DD HH:mm') }}</div>
									<div>Zakończony: <span v-if="participantQuest.done">{{ date.formatDate(participantQuest.doneAt, 'YYYY.MM.DD HH:mm') }}</span><span v-else>-</span></div>
								</div>
								<q-btn
									:disable="participantQuest.done"
									@click="selectedParticipantQuest = participantQuest; questMarkDoneDialog = true;"
								>
									{{ participantQuest.done ? 'Zakończony' : 'Zakończ' }}
								</q-btn>
							</div>
							<div class="row justify-between text-body2">
								<div v-if="participantQuest.notes">Uwagi: {{ participantQuest.notes }}</div>
							</div>
						</q-item-label>
					</q-item-section>
				</q-item>
			</q-list>
		</div>
		<EmptyComponent
			v-else
			icon="info"
			primary="Wybierz uczestnika"
			secondary="Wybierz uczestnika, aby obsługiwać jego questy."
			class="q-my-md"
		/>
	</div>

	<InfoPointQuestMarkDoneDialog
		v-model="questMarkDoneDialog"
		:participant-quest="selectedParticipantQuest"
	/>

	<InfoPointQuestGiveOutDialog
		v-model="questGiveOutDialog"
	/>
</template>
