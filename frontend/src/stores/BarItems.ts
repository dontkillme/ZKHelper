import { defineStore } from 'pinia';

import type { BarItem } from '@/models/bar';
import { useBarItemCategoriesStore } from '@/stores/BarItemCategories';
import api from '@/api';

type ApiResponse = {
	id: number;
	name: string;
	price: number;
	staff_price: number;
	category_id: number;
	modify_date: string;
	available: boolean;
}[];

type RootState = {
	items: BarItem[];
	loading: boolean;
	error: string | null;
};

function resetState(state: RootState) {
	state.items = [];
}

export const useBarItemsStore = defineStore({
	id: 'BarItems',
	state: () =>
		({
			items: [],
			loading: false,
			error: null,
		} as RootState),
	getters: {
		itemCatalog(state) {
			return state.items.reduce((acc: { [key: number]: BarItem }, element: BarItem) => {
				acc[element.id] = element;
				return acc;
			}, {});
		},
		filteredItems(state) {
			const { selectedCategoryId } = useBarItemCategoriesStore();
			if (selectedCategoryId === null) {
				return state.items;
			} else {
				return state.items.filter((element) => element.categoryId == selectedCategoryId);
			}
		},
	},
	actions: {
		async fetchBarItems() {
			this.loading = true;
			this.error = null;

			try {
				const { data } = await api.get<ApiResponse>('/bar/item/');

				this.items = data.map((v) => ({
					id: v.id,
					name: v.name,
					price: v.price,
					staffPrice: v.staff_price,
					categoryId: v.category_id,
					modifyDate: v.modify_date,
					available: v.available,
				}));
			} catch (error) {
				resetState(this);
				this.error = `${error}`;
			}

			this.loading = false;
		},
	},
});
