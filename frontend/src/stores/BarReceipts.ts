import { defineStore } from 'pinia';
import type { BarAccountBasicInfo } from 'models/bar';
import { useAuthStore } from 'stores/AuthStore';
import api from 'src/api';
import { useBarItemsStore } from 'stores/BarItems';

type ReceiptHistoryApiResponse = Record<
	string,
	{
		id: number;
		bar_items: {
			id: number;
			item_name: string;
			quantity: number;
			price: string;
      item_id: number;
		};
		created_at: string;
		sum: string;
	}
>;

type SearchParticipantsApiResponse = Record<
	string,
	{
		nick: string;
		baraccount: number;
		id: number;
	}
>;

type BasicInfoApiResponse = {
	balance: string;
	is_staff: boolean;
	credits: string;
	nick: string;
  state: number;
};

type RootState = {
	orderAccount: { label: string; value: number } | null;
	orderItems: {
		itemId: number;
		quantity: number;
	}[];
	orderStaffPrices: boolean;
	sending: boolean;
	error: string | null;
	basicInfo: BarAccountBasicInfo | null;
	basicInfoLoading: boolean;
	basicInfoError: string | null;
	accountListLoading: boolean;
  orderId: number | null;
	accountList: {
		nick: string;
		account: number;
	}[];
	receiptHistoryListLoading: boolean;
	receiptHistoryList: {
		id: number;
		createdAt: Date;
		sum: number;
		items: {
			id: number;
			name: string;
			quantity: number;
			price: number;
		}[];
	}[];
};

function resetOrderState(state: RootState) {
	state.orderAccount = null;
	state.orderItems = [];
	state.orderStaffPrices = false;
}

function resetBasicInfoState(state: RootState) {
	state.basicInfo = null;
	state.orderStaffPrices = false;
}

function resetOrderData(state: RootState) {
  state.orderId = null;
  state.orderItems = [];
}

export const useBarReceiptsStore = defineStore({
	id: 'BarReceipts',
	state: () =>
		({
			orderAccount: null,
			orderItems: [],
			orderStaffPrices: false,
			sending: false,
			error: null,
			basicInfoLoading: false,
			basicInfoError: null,
			basicInfo: null,
			accountListLoading: false,
			accountList: [],
			receiptHistoryListLoading: false,
			receiptHistoryList: [],
      orderId: null,
		} as RootState),
	getters: {
		hasAnyItemsInOrder(state) {
			return 0 < Object.keys(state.orderItems).length;
		},
		orderItemCatalog(state) {
			return Object.fromEntries(
				state.orderItems.map((orderItem) => [
					orderItem.itemId,
					orderItem.quantity,
				])
			);
		},
		orderTotal(state) {
			const { itemCatalog, getItemPrice } = useBarItemsStore();

			return state.orderItems.reduce(
				(acc, element) =>
					acc +
					getItemPrice(itemCatalog[element.itemId]) *
						element.quantity,
				0
			);
		},
	},
	actions: {
    setCurrentAccount(accountId) {
      this.orderAccount = accountId;
    },
		clearOrder() {
      if (this.orderId) {
        resetOrderData(this);
        return;
      }
			resetOrderState(this);
			resetBasicInfoState(this);
		},
		addItemQuantityToOrder(barItemId: number) {
			const orderItemIndex = this.orderItems.findIndex(
				(element) => element.itemId === barItemId
			);
			if (orderItemIndex === -1) {
				this.orderItems.push({
					itemId: barItemId,
					quantity: 1,
				});
			} else {
				this.orderItems[orderItemIndex].quantity += 1;
			}
		},
		takeItemQuantityToOrder(barItemId: number) {
			const orderItemIndex = this.orderItems.findIndex(
				(element) => element.itemId === barItemId
			);
			if (orderItemIndex !== -1) {
				this.orderItems[orderItemIndex].quantity -= 1;

				if (this.orderItems[orderItemIndex].quantity <= 0) {
					this.orderItems.splice(orderItemIndex, 1);
				}
			}
		},
    setOrderItemsFromReceipt(receipt) {
      this.orderItems = [];
      for (const item of receipt.items) {
        this.orderItems.push({
					itemId: item.item_id,
					quantity: item.quantity,
				});
      }
      this.orderId = receipt.id
    },
    updateReceiptHistory() {
      if (this.orderId) {
        this.fetchAccountBasicInfo();
        this.fetchReceiptHistory();
      }
    },
    async fetchReceiptHistory(accountFilter=true,pageSize=null,page=null) {
			this.receiptHistoryListLoading = true;
      let filter = accountFilter ? `?account=${this.orderAccount?.value}&` : "?"
      filter += (pageSize ? `page_size=${pageSize}` : '');
      filter += (page ? `page=${page}` : '');
      
			try {
				let { data } = await api.get<ReceiptHistoryApiResponse>(
					'/bar/receipt/' + filter
				);

        if (data.results) {
          data = data.results;
        }
				this.receiptHistoryList = data.map((v) => ({
					id: v.id,
          account: v.account ?? null,
					createdAt: new Date(v.created_at),
					sum: parseFloat(v.sum),
					items: v.bar_items.map((i) => ({
						id: i.id,
						name: i.item_name,
						quantity: i.quantity,
						price: parseFloat(i.price),
            item_id: i.item_id
					})),
				}));
			} catch (error) {
				this.receiptHistoryList = [];
			}

			this.receiptHistoryListLoading = false;
		},
		async fetchFilteredAccountList(searchValue: string) {
			this.accountListLoading = true;

			try {
				const { data } = await api.get<SearchParticipantsApiResponse>(
					`/bar/search/?search=${searchValue}`
				);

				this.accountList = data.map((v) => ({
					label: `${v.nick} (#${v.id})`,
					value: v.id,
				}));
			} catch (error) {
				this.accountList = [];
			}

			this.accountListLoading = false;
		},
		async fetchAccountBasicInfo(e, accountID=null) {
			if (!this.orderAccount && !accountID) {
				resetBasicInfoState(this);
				this.basicInfoLoading = false;
				this.basicInfoError = null;

				return;
			}
      console.log(accountID)

			this.basicInfoLoading = true;
			this.basicInfoError = null;
      const personIDToSend= accountID ? accountID : this.orderAccount?.value;

			try {
				const { data } = await api.get<BasicInfoApiResponse>(
					`/bar/account_basics/${personIDToSend}/`
				);

				this.basicInfo = {
					balance: parseFloat(data.balance),
					isStaff: data.is_staff,
					credits: parseFloat(data.credits),
					nick: data.nick,
          state: data.state,
				};

				this.orderStaffPrices = this.basicInfo.isStaff;
			} catch (error) {
				resetBasicInfoState(this);
				this.basicInfoError = error.message;
			}

			this.basicInfoLoading = false;
		},
		async addCredits(creditValue: number, inferring: number) {
			await api.post('bar/bar_account/', {
				participant_id: this.orderAccount?.value,
        inferring: inferring,
				credits: creditValue,
			});
		},
    async changeAccountState(action: string, userId: number) {
      await api.post('bar/change_state/', {
				participant_id: this.orderAccount?.value,
				action: action,
        user_id: userId
			});
    },
		async createBarReceipt(noAccount=false) {
			const { participantId } = useAuthStore();
      const data = {
				seller: participantId,
				price_mode: Number(this.orderStaffPrices),
				items: this.orderItems.map((v) => ({
					item_id: v.itemId,
					quantity: v.quantity,
				})),
			}

      if (this.orderAccount && !noAccount) {
        data['account'] = this.orderAccount?.value ? this.orderAccount.value : this.orderAccount;
      }

      if (this.orderId) {
        await api.put(`/bar/receipt/${this.orderId}/`, data);
      } else {
        await api.post('/bar/receipt/', data);
        resetOrderState(this);
        resetBasicInfoState(this);
      }
		},
	},
});
