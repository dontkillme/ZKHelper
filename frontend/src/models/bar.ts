export interface BarItem {
	id: number;
	name: string;
	price: number;
	staffPrice: number;
	categoryId: number;
	modifyDate: string;
	available: boolean;
}

export interface BarItemCategory {
	id: number;
	name: string;
}

export interface BarReceiptOrder {
	account: number | null;
	seller: number | null;
	items: {
		itemId: number;
		quantity: number;
	}[];
}

export interface BarAccountBasicInfo {
	balance: number;
	isStaff: boolean;
	credits: number;
}
