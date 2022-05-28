import { defineStore } from 'pinia';

import axios from 'axios';
import type {BarAccountBasicInfo, BarReceiptOrder} from "@/models/bar";
import {useBarItemsStore} from "@/stores/BarItems";

type RootState = {
  order: BarReceiptOrder;
  sending: boolean;
  error: any | null;
  basic_info_loading: boolean;
  basic_info_error: any | null;
  basic_info: BarAccountBasicInfo | null;
};

export const useBarReceiptsStore = defineStore({
  id: 'BarReceipts',
  state: () => ({
    order: {
      account: null,
      seller: 1,
      items: [],
    },
    sending: false,
    error: null,
    basic_info_loading: false,
    basic_info_error: null,
    basic_info: null,
  } as RootState),
  getters: {
    itemCatalog(state) {
      const barItemsStore = useBarItemsStore();
      return barItemsStore.itemCatalog;
    },
    hasAnyItemsInOrder(state) {
      return 0 < Object.keys(state.order.items).length;
    },
    orderTotal(state) {
      return state.order.items.reduce((acc, element) => acc + (state.itemCatalog[element.item_id].price * element.quantity), 0);
    }
  },
  actions: {
    addItemQuantityToOrder(barItemId: number) {
      let orderItemIndex = this.order.items.findIndex(element => element.item_id === barItemId);
      if (orderItemIndex === -1) {
        this.order.items.push({
          item_id: barItemId,
          quantity: 1,
        })
      }
      else {
        this.order.items[orderItemIndex].quantity += 1;
      }
    },
    takeItemQuantityToOrder(barItemId: number) {
      let orderItemIndex = this.order.items.findIndex(element => element.item_id === barItemId);
      if (orderItemIndex !== -1) {
        this.order.items[orderItemIndex].quantity -= 1;

        if (this.order.items[orderItemIndex].quantity <= 0) {
          this.order.items.splice(orderItemIndex, 1);
        }
      }
    },
    async fetchAccountBasicInfo() {
      if (this.order.account === null) {
        this.basic_info = null;
        this.basic_info_error = null;
        this.basic_info_loading = false;
        return;
      }

      this.basic_info_loading = true;
      let response;

      try {
        response = await axios.get('http://192.168.1.64:8000/bar/account_basics/' + this.order.account);
      }
      catch (error) {
        this.basic_info_loading = false;
        this.basic_info = null;

        if (axios.isAxiosError(error)) {
          this.basic_info_error = error.response.data;
        }
        else{
          this.basic_info_error = '' + error;
        }
        return;
      }

      this.basic_info = response.data;
      this.basic_info_error = null;

      this.basic_info_loading = false;
    },
    async createBarReceipt() {
      this.sending = true;
      let response;

      try {
        response = await axios.post('http://192.168.1.64:8000/bar/receipt/', this.order);
      }
      catch(error) {
        this.sending = false;
        if (axios.isAxiosError(error)) {
          this.error = error.response.data;
        }
        else{
          this.error = '' + error;
        }
        return;
      }

      this.order.account = null;
      this.order.items = [];
      this.error = null;

      this.sending = false;
    },
  },
});
