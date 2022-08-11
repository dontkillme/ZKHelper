import { defineStore } from 'pinia';

import api from 'src/api';
import { useBarReceiptsStore } from 'stores/BarReceipts';

type RootState = {
	participantId: string | null;
	participantNick: string | null;
	groups: string[] | null;
	token: string | null;
};

function resetState(state: RootState) {
	state.participantId = null;
	state.participantNick = null;
	state.groups = null;
	state.token = null;
}

export const useAuthStore = defineStore({
	id: 'Auth',
	state: () =>
		({
			participantId: null,
			participantNick: null,
			groups: null,
			token: null,
		} as RootState),
	getters: {
		isAuthenticated(state) {
			return state.participantId !== null;
		},
	},
	actions: {
		async login(pin: number) {
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

				let message = error.message;

				if (error.status === 401) {
					message = 'Podany PIN nie został odnaleziony w bazie!';
				}

				throw Error(message);
			}
		},
		logout() {
			const { clearOrder } = useBarReceiptsStore();

			resetState(this);
			clearOrder();
		},
		hasPermission(group: string) {
			return this.groups?.includes(group);
		},
	},
});
