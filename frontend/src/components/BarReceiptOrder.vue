<script setup lang="ts">
  import {storeToRefs} from "pinia";
  import {useBarReceiptsStore} from "@/stores/BarReceiptss";
  import { debounce } from "lodash";
  import {useBarItemsStore} from "@/stores/BarItems";

  const {order, sending, error, hasAnyItemsInOrder, orderTotal, basic_info_loading, basic_info_error, basic_info} = storeToRefs(useBarReceiptsStore())
  const { itemCatalog } = storeToRefs(useBarItemsStore())
  const {addItemQuantityToOrder, takeItemQuantityToOrder, createBarReceipt, fetchAccountBasicInfo} = useBarReceiptsStore();

  const fetchAccountBasicInfoDebounced = debounce((e) => fetchAccountBasicInfo(), 500);
</script>

<template>
  Zamówienie:<br>
  Krecha na usera: <input v-model="order.account" @input="fetchAccountBasicInfoDebounced">
  <span v-if="basic_info_loading">Wczytuję podsumowanie usera...</span>
  <span v-if="basic_info_error">Błąd wczytywania podsumowanie usera!<br>{{ basic_info_error }}</span>
  <span v-if="basic_info">promocyjne ceny: {{basic_info.is_staff }} stan konta: {{basic_info.balance }} suma wpłat na krechę: {{basic_info.credits}}</span>
  <br>
  <ul v-if="hasAnyItemsInOrder" class="bar-items">
    <li v-for="orderItem in order.items" :key="orderItem.item_id">
      <span>x{{ orderItem.quantity }} {{ itemCatalog[orderItem.item_id].name }} {{ itemCatalog[orderItem.item_id].price * orderItem.quantity }} zł</span>
      <button @click="addItemQuantityToOrder(orderItem.item_id)">+</button>
      <button @click="takeItemQuantityToOrder(orderItem.item_id)">-</button>
    </li>
  </ul>
  <div v-else>Brak produktów w zamówieniu!</div>
  <div v-if="hasAnyItemsInOrder">SUMA: {{ orderTotal }} zł</div>
  <button v-if="hasAnyItemsInOrder" @click="createBarReceipt()">Zamów!</button>
  <span v-if="sending">Zamawiam...</span>
  <span v-if="error">Błąd w zamiawaniu!<br>{{ error }}</span>
</template>