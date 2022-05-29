import { defineStore } from 'pinia';

import axios from 'axios';
import type {BarItemCategory} from "@/models/bar";
import {useBarAuthStore} from "@/stores/BarAuth";

type RootState = {
  categories: BarItemCategory[];
  selectedCategoryId: number | null;
  loading: boolean;
  error: any | null;
};

export const useBarItemCategoriesStore = defineStore({
  id: 'BarItemCategories',
  state: () => ({
    categories: [],
    selectedCategoryId: null,
    loading: false,
    error: null,
  } as RootState),
  getters: {
    categoryCatalog(state) {
      return state.categories.reduce((acc: {[key: number]: BarItemCategory}, element: BarItemCategory) => {
        acc[element.id] = element;
        return acc;
      }, {});
    }
  },
  actions: {
    async fetchBarItemCategories() {
      this.loading = true;
      const {token} = useBarAuthStore();
      try {
        const response = await axios.get('http://192.168.1.64:8000/bar/item_category/', {
          headers: {
            'Authorization': 'token ' + token,
          }
        })
        this.categories = response.data;
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
