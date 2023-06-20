<script setup lang="ts">
	import { computed, ref } from 'vue';
import BarReceiptAccount from 'components/BarReceiptAccount.vue';
import BarReceiptItems from 'components/BarReceiptItems.vue';

	const props = defineProps({
		modelValue: {
			type: Boolean,
			required: true,
		},
	});
	const emit = defineEmits(['update:modelValue']);
	const payByCash = ref(false);
	const dialogState = computed({
		get: () => props.modelValue,
		set: (dialogState) => emit('update:modelValue', dialogState),
	});
  const btnColorState = computed(() => (payByCash.value ? "secondary" : "primary"));

</script>

<template>
	<q-dialog v-model="dialogState">
		<q-card style="width: 90vw; max-width: 80vw">
          <q-card-section class="row items-center">
            <div class="row" >
              <div class="col-auto" v-if="!payByCash">
                <BarReceiptAccount basic-view=true />
              </div>
              <div class="col-auto">
                <q-btn
                  :color="btnColorState"
                  size="lg"
                  @click="payByCash=!payByCash"
                >Gotówka</q-btn>
              </div>
            </div>
          </q-card-section>
			<q-separator />

			<q-card-section>
				<BarReceiptItems v-model:payCash="payByCash" v-model:dialog-state="dialogState"/>
			</q-card-section>
		</q-card>
	</q-dialog>
</template>
