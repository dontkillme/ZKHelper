import { defineStore } from 'pinia';
import type { BarAccountBasicInfo } from 'models/bar';
import { useBarAuthStore } from 'stores/BarAuth';
import api from 'src/api';
import { useBarItemsStore } from 'stores/BarItems';

type ApiResponse = {
	balance: number;
	is_staff: boolean;
	credits: number;
	nick: string;
};

type RootState = {
	orderAccount: number | null;
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
		} as RootState),
	getters: {
		hasAnyItemsInOrder(state) {
			return 0 < Object.keys(state.orderItems).length;
		},
		orderItemCatalog(state) {
			return Object.fromEntries(state.orderItems.map((orderItem) => [orderItem.itemId, orderItem.quantity]));
		},
		orderTotal(state) {
			const { itemCatalog, getItemPrice } = useBarItemsStore();

			return state.orderItems.reduce(
				(acc, element) => acc + getItemPrice(itemCatalog[element.itemId]) * element.quantity,
				0
			);
		},
	},
	actions: {
		clearOrder() {
			resetOrderState(this);
			resetBasicInfoState(this);
		},
		addItemQuantityToOrder(barItemId: number) {
			const orderItemIndex = this.orderItems.findIndex((element) => element.itemId === barItemId);
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
			const orderItemIndex = this.orderItems.findIndex((element) => element.itemId === barItemId);
			if (orderItemIndex !== -1) {
				this.orderItems[orderItemIndex].quantity -= 1;

				if (this.orderItems[orderItemIndex].quantity <= 0) {
					this.orderItems.splice(orderItemIndex, 1);
				}
			}
		},
		async fetchAccountBasicInfo() {
			if (!this.orderAccount) {
				resetBasicInfoState(this);
				this.basicInfoLoading = false;
				this.basicInfoError = null;

				return;
			}

			this.basicInfoLoading = true;
			this.basicInfoError = null;

			try {
				const { data } = await api.get<ApiResponse>(`/bar/account_basics/${this.orderAccount}/`);

				this.basicInfo = {
					balance: data.balance,
					isStaff: data.is_staff,
					credits: data.credits,
					nick: data.nick,
				};

				this.orderStaffPrices = this.basicInfo.isStaff;
			} catch (error) {
				resetBasicInfoState(this);
				this.basicInfoError = error.message;
			}

			this.basicInfoLoading = false;
		},
		async createBarReceipt() {
			this.sending = true;
			this.error = null;

			const { participantId } = useBarAuthStore();

			try {
				await api.post('/bar/receipt/', {
					account: this.orderAccount,
					seller: participantId,
					items: this.orderItems.map((v) => ({
						item_id: v.itemId,
						quantity: v.quantity,
					})),
				});
			} catch (error) {
				this.error = error.message;

				this.sending = false;
				return;
			}

			resetOrderState(this);
			resetBasicInfoState(this);

			this.sending = false;
		},
	},
});
