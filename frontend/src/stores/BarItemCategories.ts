import { defineStore } from 'pinia';

import type { BarItemCategory } from 'models/bar';
import api from 'src/api';

type ApiResponse = {
	id: number;
	name: string;
}[];

type RootState = {
	categories: BarItemCategory[];
	selectedCategoryId: number | null;
	loading: boolean;
	error: string | null;
};

function resetState(state: RootState) {
	state.categories = [];
}

export const useBarItemCategoriesStore = defineStore({
	id: 'BarItemCategories',
	state: () =>
		({
			categories: [],
			selectedCategoryId: null,
			loading: false,
			error: null,
		} as RootState),
	getters: {
		categoryCatalog(state) {
			return state.categories.reduce(
				(
					acc: { [key: number]: BarItemCategory },
					element: BarItemCategory
				) => {
					acc[element.id] = element;
					return acc;
				},
				{}
			);
		},
	},
	actions: {
		async fetchBarItemCategories() {
			this.loading = true;
			this.error = null;

			try {
				const { data } = await api.get<ApiResponse>(
					'/bar/item_category/'
				);

				this.categories = data.map((v) => ({
					id: v.id,
					name: v.name,
				}));
			} catch (error) {
				resetState(this);
				this.error = error.message;
			}

			this.loading = false;
		},
	},
});
