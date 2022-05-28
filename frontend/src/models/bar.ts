export interface BarItem {
  id: number;
  name: string;
  price: number;
  staff_price: number;
  category_id: number;
  modify_date: string;
  available: boolean;
}

export interface BarItemCategory {
  id: number;
  name: string;
}

export interface BarReceiptOrderItem {
  item_id: number;
  quantity: number;
}

export interface BarReceiptOrder {
  account: number | null;
  seller: number;
  items: BarReceiptOrderItem[];
}

export interface BarAccountBasicInfo {
  balance: number;
  is_staff: boolean;
  credits: number;
}