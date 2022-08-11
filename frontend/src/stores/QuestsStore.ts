import { defineStore } from 'pinia';

import api from 'src/api';
import { ParticipantQuest, Quest } from 'models/infopoint';

type AccountOptionListApiResponse = {
	nick: string;
	id: number;
}[];

type SelectedParticipantQuestsApiResponse = {
	id: number;
	participant_id: number;
	quest_id: number;
	notes: string | null;
	started_at: string;
	end_at: string | null;
	done: boolean;
}[];

type RootState = {
	quests: Quest[];
	questLoading: boolean;
	selectedParticipant: { label: string; value: number } | null;
	selectedParticipantQuests: ParticipantQuest[];
	selectedParticipantQuestsLoading: boolean;
	filteredAccountOptionList: { label: string; value: number }[];
	filteredAccountOptionListLoading: boolean;
};

export const useQuestsStore = defineStore({
	id: 'Quests',
	state: () =>
		({
			quests: [],
			questLoading: false,
			selectedParticipant: null,
			selectedParticipantQuests: [],
			selectedParticipantQuestsLoading: false,
			filteredAccountOptionList: [],
			filteredAccountOptionListLoading: false,
		} as RootState),
	getters: {
		questCatalog(state) {
			return state.quests.reduce(
				(acc: { [key: number]: Quest }, element: Quest) => {
					acc[element.id] = element;
					return acc;
				},
				{}
			);
		},
	},
	actions: {
		async fetchQuests() {
			this.questLoading = true;
			this.quests = [];

			try {
				const { data } = await api.get<Quest[]>('/event/quest/');

				this.quests = data;
			} catch (error) {}

			this.questLoading = false;
		},
		async fetchFilteredAccountOptionList(searchValue: string) {
			this.filteredAccountOptionListLoading = true;
			this.filteredAccountOptionList = [];

			try {
				const { data } = await api.get<AccountOptionListApiResponse>(
					`/bar/search/?search=${searchValue}`
				);

				this.filteredAccountOptionList = data.map((v) => ({
					label: `${v.nick} (#${v.id})`,
					value: v.id,
				}));
			} catch (error) {}

			this.filteredAccountOptionListLoading = false;
		},
		async fetchSelectedParticipantQuests() {
			this.selectedParticipantQuestsLoading = true;
			this.selectedParticipantQuests = [];

			if (!this.quests.length) {
				await this.fetchQuests();
			}

			try {
				const { data } =
					await api.get<SelectedParticipantQuestsApiResponse>(
						`/event/participant_quest/?participant_id=${this.selectedParticipant.value}`
					);

				this.selectedParticipantQuests = data.map((v) => ({
					id: v.id,
					participantId: v.participant_id,
					questId: v.quest_id,
					notes: v.notes,
					startedAt: v.started_at,
					doneAt: v.end_at,
					done: v.done,
				})).reverse();
			} catch (error) {}

			this.selectedParticipantQuestsLoading = false;
		},
		async giveOutParticipantQuest(questId: number) {
			await api.post('/event/participant_quest/', {
				participant_id: this.selectedParticipant.value,
				quest_id: questId,
			});

			await this.fetchSelectedParticipantQuests();
		},
		async markParticipantQuestDone(participantQuestId: number, notes: string | null) {
			await api.put(`/event/participant_quest/${participantQuestId}/`, {
				done: true,
				notes,
			});

			await this.fetchSelectedParticipantQuests();
		}
	},
});
