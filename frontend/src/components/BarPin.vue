<script setup lang="ts">
  import {storeToRefs} from "pinia";
  import {useBarAuthStore} from "@/stores/BarAuth";
  import {ref} from "vue";

  const {participant, isAuthenticated, groups, sending, error} = storeToRefs(useBarAuthStore())
  const {login, logout} = useBarAuthStore();

  let pin = ref(null);

  function loginAction() {
    if (pin.value) {
      login(pin.value);
      pin.value = null;
    }
  }
</script>

<template>
  <div v-if="!isAuthenticated && !sending">
    Podaj pin:<br><input type="password" pattern="[0-9]*" inputmode="numeric" v-model="pin"><button @click="loginAction">Login</button>
  </div>
  <div v-if="isAuthenticated">Zalogowano jako {{ participant.nick }}! <button @click="logout">Wyloguj</button></div>
  <div v-if="isAuthenticated">{{ groups }}</div>
  <div v-if="sending">Loguję...</div>
  <div v-if="error">Błąd logowania!<br>{{ error }}</div>
</template>