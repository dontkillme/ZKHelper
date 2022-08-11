<script setup lang="ts">
	import { computed } from 'vue';
	import EmptyComponent from 'components/EmptyComponent.vue';

	const props = defineProps({
		modelValue: {
			type: Boolean,
			required: true,
		},
		participant: {
			type: Object,
		},
	});
	const emit = defineEmits([
		'accreditParticipantDialogRequest',
		'tshirtGiveOutDialogRequest',
		'update:modelValue',
	]);

	const dialogState = computed({
		get: () => props.modelValue,
		set: (dialogState) => emit('update:modelValue', dialogState),
	});
</script>

<template>
	<q-dialog v-model="dialogState">
		<q-card style="width: 30rem; max-width: 80vw">
			<q-card-section class="row items-center">
				<div class="text-h6">
					Szczegóły Uczestnika: {{ participant.nick }} (#{{
						participant.id
					}})
				</div>
				<q-space />
				<q-btn icon="close" flat round dense v-close-popup />
			</q-card-section>

			<q-separator />

			<q-card-section>
				<div class="text-body2 text-secondary">Imię i nazwisko</div>
				<div class="text-body1">
					{{ participant.surname }} {{ participant.name }}
				</div>

				<div class="text-body2 text-secondary q-mt-sm">
					Numer telefonu
				</div>
				<div class="text-body1">{{ participant.phone }}</div>

				<div class="text-body2 text-secondary q-mt-sm">
					Alarmowy numer telefonu
				</div>
				<div class="text-body1">
					{{ participant.icePhone }} ({{ participant.iceName }})
				</div>

				<div class="text-body2 text-secondary q-mt-sm">Uwagi</div>
				<div class="text-body1">{{ participant.iceExtra }}</div>
			</q-card-section>

			<q-separator />

			<q-card-actions vertical>
				<div v-if="participant.accredited" class="text-center q-my-sm">
					Uczestnik zakredytowany
				</div>
				<q-btn
					v-else
					flat
					@click="emit('accreditParticipantDialogRequest')"
					>Akredytuj</q-btn
				>
			</q-card-actions>

			<q-separator />

			<q-card-section class="q-pa-none">
				<q-list separator>
					<q-item-label header>Koszulki</q-item-label>
					<q-separator />
				</q-list>
				<q-list separator class="scroll" style="max-height: 50vh">
					<EmptyComponent
						v-if="!participant.tshirt.length"
						icon="checkroom"
						primary="Brak koszulek!"
						secondary="Uczestnik nie zamówił żadnych koszulek."
						class="q-my-md"
					/>
					<q-item
						v-for="tshirt in participant.tshirt"
						:key="tshirt.id"
					>
						<q-item-section>
							<q-item-label>
								<div class="row justify-between text-body1">
									<div>Koszulka {{ tshirt.size }}</div>
									<q-btn
										:disable="tshirt.givenOut"
										@click="
											emit(
												'tshirtGiveOutDialogRequest',
												tshirt
											)
										"
									>
										{{
											tshirt.givenOut ? 'Wydana' : 'Wydaj'
										}}
									</q-btn>
								</div>
							</q-item-label>
							<q-item-label
								v-if="tshirt.extra"
								class="text-body2 text-secondary"
							>
								{{ tshirt.extra }}
							</q-item-label>
						</q-item-section>
					</q-item>
				</q-list>
			</q-card-section>
		</q-card>
	</q-dialog>
</template>
