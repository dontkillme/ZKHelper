import { defineStore } from 'pinia';

import api from 'src/api';
import type { Participant } from 'models/infopoint';

type ApiResponseObject = {
	id: number;
	name: string;
	surname: string;
	nick: string;
	phone: string;
	ice_phone: string;
	ice_name: string;
	ice_extra: string;
	is_staff: boolean;
	accredited: boolean;
	tshirt: {
		id: number;
		size: string;
		given_out: boolean;
		extra: string | null;
		event_participant: number;
	}[];
};

type ApiResponse = ApiResponseObject[];

type RootState = {
	participants: Participant[];
	loading: boolean;
	error: string | null;
};

function resetState(state: RootState) {
	state.participants = [];
}

export const useParticipantsStore = defineStore({
	id: 'Participants',
	state: () =>
		({
			participants: [],
			loading: false,
			error: null,
		} as RootState),
	actions: {
		async fetchParticipants() {
			this.loading = true;
			this.error = null;
			resetState(this);

			try {
				const { data } = await api.get<ApiResponse>(
					'/event/fulleventparticipant/'
				);

				this.participants = data
					.map((v) => ({
						id: v.id,
						name: v.name,
						surname: v.surname,
						nick: v.nick,
						phone: v.phone,
						icePhone: v.ice_phone,
						iceName: v.ice_name,
						iceExtra: v.ice_extra,
						isStaff: v.is_staff,
						accredited: v.accredited,
						tshirt: v.tshirt.map((t) => ({
							id: t.id,
							size: t.size,
							givenOut: t.given_out,
							extra: t.extra,
						})),
					}))
					.sort((a, b) => (a.id < b.id ? -1 : 1));
			} catch (error) {
				this.error = error.message;
			}

			this.loading = false;
		},
		async updateParticipant(participantId: number) {
			const { data } = await api.get<ApiResponseObject>(
				`/event/fulleventparticipant/${participantId}/`
			);

			const participant = this.participants.find(
				(element) => element.id === participantId
			);

			if (participant) {
				participant.id = data.id;
				participant.name = data.name;
				participant.surname = data.surname;
				participant.nick = data.nick;
				participant.phone = data.phone;
				participant.icePhone = data.ice_phone;
				participant.iceName = data.ice_name;
				participant.iceExtra = data.ice_extra;
				participant.isStaff = data.is_staff;
				participant.accredited = data.accredited;
				participant.tshirt = data.tshirt.map((t) => ({
					id: t.id,
					size: t.size,
					givenOut: t.given_out,
					extra: t.extra,
				}));
			}
		},
		async accreditParticipant(participantId: number) {
			await api.post(`/event/accredited_state/${participantId}/`, {
				accredited: 1,
			});

			await this.updateParticipant(participantId);
		},
		async giveOutParticipantTshirt(
			participantId: number,
			tshirtId: number
		) {
			await api.post(`/event/tshirt_state/${tshirtId}/`, {
				given_out: 1,
			});

			await this.updateParticipant(participantId);
		},
	},
});
