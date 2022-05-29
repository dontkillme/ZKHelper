<script setup lang="ts">
  import {storeToRefs} from "pinia";
  import {useBarItemCategoriesStore} from "@/stores/BarItemCategories";

  const {categories, loading, error, selectedCategoryId} = storeToRefs(useBarItemCategoriesStore())
  const {fetchBarItemCategories} = useBarItemCategoriesStore();

  fetchBarItemCategories();
</script>

<template>
  Kategorie:
  <div v-if="loading">Ładuję kategorię...</div>
  <div v-if="error">Błąd ładowania kategorii!<br>{{ error.message }}</div>
  <ul v-if="!loading && !error" class="bar-categories">
    <li><label for="category-0">Wszystkie</label> <input type="radio" id="category-0" :value="null" v-model="selectedCategoryId"></li>
    <li v-for="category in categories" :key="category.id">
      <label :for="'category-' + category.id">{{ category.name }}</label> <input type="radio" :id="'category-' + category.id" :value="category.id" v-model="selectedCategoryId">
    </li>
  </ul>
</template>