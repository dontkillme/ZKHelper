import { defineStore } from 'pinia';
import type { BarAccountBasicInfo } from 'models/bar';
import api from 'src/api';

type ReceiptHistoryApiResponse = Record<
	string,
	{
		id: number;
		bar_items: {
			id: number;
			item_name: string;
			quantity: number;
			price: string;
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
};

type RootState = {
	basicInfo: BarAccountBasicInfo | null;
	basicInfoLoading: boolean;
	basicInfoError: string | null;
	accountListLoading: boolean;
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

function resetBasicInfoState(state: RootState) {
	state.basicInfo = null;
}

export const useBarReceiptsStore = defineStore({
	id: 'BarReceipts',
	state: () =>
		({
			orderAccount: null,
			orderItems: [],
			orderStaffPrices: false,
			basicInfoLoading: false,
			basicInfoError: null,
			basicInfo: null,
			accountListLoading: false,
			accountList: [],
			receiptHistoryListLoading: false,
			receiptHistoryList: [],
		} as RootState),
	actions: {
		async fetchReceiptHistory() {
			this.receiptHistoryListLoading = true;

			try {
				const { data } = await api.get<ReceiptHistoryApiResponse>(
					`/bar/receipt/?account=${this.orderAccount?.value}`
				);

				this.receiptHistoryList = data.map((v) => ({
					id: v.id,
					createdAt: new Date(v.created_at),
					sum: parseFloat(v.sum),
					items: v.bar_items.map((i) => ({
						id: i.id,
						name: i.item_name,
						quantity: i.quantity,
						price: parseFloat(i.price),
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
				const { data } = await api.get<BasicInfoApiResponse>(
					`/bar/account_basics/${this.orderAccount?.value}/`
				);

				this.basicInfo = {
					balance: parseFloat(data.balance),
					isStaff: data.is_staff,
					credits: parseFloat(data.credits),
					nick: data.nick,
				};

				this.orderStaffPrices = this.basicInfo.isStaff;
			} catch (error) {
				resetBasicInfoState(this);
				this.basicInfoError = error.message;
			}

			this.basicInfoLoading = false;
		},
		async addCredits(creditValue: number) {
			await api.post('bar/bar_account/', {
				participant_id: this.orderAccount?.value,
				credits: creditValue,
			});
		},
	},
});
