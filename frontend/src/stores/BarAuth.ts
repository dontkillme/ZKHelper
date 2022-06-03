import { defineStore } from 'pinia';

import api from '@/api';

type RootState = {
	participantId: string | null;
	participantNick: string | null;
	groups: string[] | null;
	token: string | null;
	sending: boolean;
	error: string | null;
};

function resetState(state: RootState) {
	state.participantId = null;
	state.participantNick = null;
	state.groups = null;
	state.token = null;
}

export const useBarAuthStore = defineStore({
	id: 'BarAuth',
	state: () =>
		({
			participantId: null,
			participantNick: null,
			groups: null,
			token: null,
			sending: false,
			error: null,
		} as RootState),
	getters: {
		isAuthenticated(state) {
			return state.participantId !== null;
		},
	},
	actions: {
		async login(pin: number) {
			this.sending = true;
			this.error = null;

			try {
				const { data } = await api.post('/pin/', {
					pin: pin,
				});

				this.participantId = data.participant_id;
				this.participantNick = data.participant_nick;
				this.groups = data.groups;
				this.token = data.token;
			} catch (error) {
				resetState(this);
				this.error = `${error}`;
			}

			this.sending = false;
		},
		logout() {
			resetState(this);
		},
	},
});
