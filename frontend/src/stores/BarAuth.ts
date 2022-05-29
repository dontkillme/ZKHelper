import { defineStore } from 'pinia';

import axios from 'axios';
import type {BarAccountBasicInfo, BarReceiptOrder} from "@/models/bar";
import {useBarItemsStore} from "@/stores/BarItems";

type RootState = {
  participant: {
    id: string,
    nick: string,
  } | null;
  token: string | null;
  groups: string[];
  sending: boolean;
  error: any | null;
};

export const useBarAuthStore = defineStore({
  id: 'BarAuth',
  state: () => ({
    participant: null,
    token: null,
    groups: [],
    sending: false,
    error: null,
  } as RootState),
  getters: {
    isAuthenticated(state) {
      return state.participant !== null;
    }
  },
  actions: {
    async login(pin: number) {
      this.sending = true;
      this.error = null;
      let response;

      try {
        response = await axios.post('http://192.168.1.64:8000/pin/', {
          pin: pin,
        });
      } catch (error) {
        this.sending = false;
        this.participant = null;
        this.token = null;
        this.groups = [];

        if (axios.isAxiosError(error)) {
          this.error = error.response.data;
        } else {
          this.error = '' + error;
        }

        return;
      }

      if (response.data.login === 'success') {
        this.participant = {
          id: response.data.participant_id,
          nick: response.data.participant_nick,
        }
        this.groups = response.data.groups;
        this.token = response.data.token;
      }
      else {
        this.participant = null;
        this.groups = [];
        this.token = null;
        this.error = 'Błąd logowania!'
      }

      this.sending = false;
    },
    logout() {
      this.participant = null;
      this.token = null;
      this.groups = [];
    }
  },
});
