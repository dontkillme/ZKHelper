import { defineStore, storeToRefs } from 'pinia';

import api from 'src/api';
import type { BarItem } from 'models/bar';
import { useBarItemCategoriesStore } from 'stores/BarItemCategories';
import { useBarReceiptsStore } from 'stores/BarReceipts';
import removeAccents from 'remove-accents';

type ApiResponse = {
	id: number;
	name: string;
	price: string;
	staff_price: string;
	category_id: number;
	modify_date: string;
	available: boolean;
}[];

type RootState = {
	items: BarItem[];
	searchFilter: string;
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
			searchFilter: '',
			loading: false,
			error: null,
		} as RootState),
	getters: {
		itemCatalog(state) {
			return state.items.reduce(
				(acc: { [key: number]: BarItem }, element: BarItem) => {
					acc[element.id] = element;
					return acc;
				},
				{}
			);
		},
		filteredItems(state): BarItem[] {
			const { selectedCategoryId } = useBarItemCategoriesStore();
			let items = state.items;

			if (selectedCategoryId !== null) {
				items = items.filter(
					(element) => element.categoryId == selectedCategoryId
				);
			}

			if (state.searchFilter) {
				const words = removeAccents(state.searchFilter)
					.toLowerCase()
					.split(' ');
				items = items.filter((element) => {
					const normalizedName = removeAccents(
						element.name
					).toLowerCase();
					return words.every(
						(word) => normalizedName.indexOf(word) !== -1
					);
				});
			}

			return items;
		},
		getItemPrice() {
			const { orderStaffPrices } = storeToRefs(useBarReceiptsStore());

			return (item: BarItem) =>
				orderStaffPrices.value ? item.staffPrice : item.price;
		},
	},
	actions: {
		async fetchBarItems() {
			this.loading = true;
			this.error = null;

			try {
				const { data } = await api.get<ApiResponse>('/bar/item/');

				this.items = data
					.map((v) => ({
						id: v.id,
						name: v.name,
						price: parseFloat(v.price),
						staffPrice: parseFloat(v.staff_price),
						categoryId: v.category_id,
						modifyDate: v.modify_date,
						available: v.available,
            position: v.position
					}))
					.sort((a, b) => {
            if (!a.position && !b.position)
              return (a.name < b.name ? -1 : 1)
            return (a.position > b.position ? -1 : 1)
          });
			} catch (error) {
				resetState(this);
				this.error = error.message;
			}

			this.loading = false;
		},
	},
});
