import { defineStore } from 'pinia';

import axios from 'axios';
import type {BarItem, BarItemCategory} from "@/models/bar";
import {useBarItemCategoriesStore} from "@/stores/BarItemCategories";

type RootState = {
  items: BarItem[];
  loading: boolean;
  error: any | null;
};

export const useBarItemsStore = defineStore({
  id: 'BarItems',
  state: () => ({
    items: [],
    loading: false,
    error: null,
  } as RootState),
  getters: {
    itemCatalog(state) {
      return state.items.reduce((acc: object, element: BarItem) => {
        acc[element.id] = element;
        return acc;
      }, {});
    },
    categoryCatalog(state) {
      const barItemCategoriesStore = useBarItemCategoriesStore();
      return barItemCategoriesStore.categoryCatalog;
    },
    filteredItems(state) {
      const {selectedCategoryId} = useBarItemCategoriesStore();
      if (selectedCategoryId === null) {
        return state.items;
      }
      else {
        return state.items.filter(element => element.category_id == selectedCategoryId);
      }
    }
  },
  actions: {
    async fetchBarItems() {
      this.loading = true;
      try {
        const response = await axios.get('http://192.168.1.64:8000/bar/item/');
        this.items = response.data;
      }
      catch(error) {
        this.error = error;
        this.loading = false;
        return error;
      }
      this.loading = false;
    },
  },
});
