<script setup lang="ts">
	import { storeToRefs } from 'pinia';
	import { ref } from 'vue';
	import { useParticipantsStore } from 'stores/ParticipantsStore';
	import EmptyComponent from 'components/EmptyComponent.vue';
	import InfoPointParticipantDialog from 'components/InfoPointParticipantDialog.vue';
	import { ParticipantTshirt } from 'models/infopoint';
	import InfoPointParticipantAccreditDialog from 'components/InfoPointParticipantAccreditDialog.vue';
	import InfoPointParticipantTshirtGiveOutDialog from 'components/InfoPointParticipantTshirtGiveOutDialog.vue';

	const { loading, participants } = storeToRefs(useParticipantsStore());
	const { fetchParticipants } = useParticipantsStore();

	const participantDialog = ref(false);
	const accreditParticipantDialog = ref(false);
	const tshirtGiveOutDialog = ref(false);
	const selectedParticipant = ref(null);
	const selectedTshirt = ref(null);

	const filter = ref('');
	const columns = [
		{ name: 'id', label: 'ID', field: 'id', sortable: true, align: 'left' },
		{
			name: 'nick',
			label: 'Nick',
			field: 'nick',
			sortable: true,
			align: 'left',
		},
		{
			name: 'surname',
			label: 'Nazwisko',
			field: 'surname',
			sortable: true,
			align: 'left',
		},
		{
			name: 'name',
			label: 'Imię',
			field: 'name',
			sortable: true,
			align: 'left',
		},
		{
			name: 'isStaff',
			label: 'Obsługa',
			field: 'isStaff',
			sortable: true,
			align: 'center',
		},
		{
			name: 'accredited',
			label: 'Akredytacja',
			field: 'accredited',
			sortable: true,
			align: 'center',
		},
		{
			name: 'tshirt',
			label: 'Koszulki',
			field: 'tshirt',
			sortable: true,
			align: 'center',
			format: (val: ParticipantTshirt[], row) => {
				const tshirts_given_out = val.reduce(
					(sum: number, current: ParticipantTshirt) =>
						sum + Number(current.givenOut),
					0
				);
				const tshirts_total = val.length;

				if (tshirts_given_out === 0 && tshirts_total === 0) {
					return '-';
				} else {
					return `Wydano ${tshirts_given_out} z ${tshirts_total}`;
				}
			},
		},
	];

	fetchParticipants();
</script>

<template>
	<div class="row justify-center q-py-lg">
		<q-table
			class="col-12 col-sm-10 col-md-8"
			:rows="participants"
			:columns="columns"
			:filter="filter"
			row-key="id"
			:loading="loading"
			:hide-bottom="loading"
			:hide-header="loading"
			:rows-per-page-options="[10, 25, 50, 0]"
			rows-per-page-label="Elementów na stronie:"
			:pagination-label="
				(firstRowIndex, endRowIndex, totalRowsNumber) =>
					`Wyświetlono ${firstRowIndex}-${endRowIndex} z ${totalRowsNumber} elementów`
			"
		>
			<template #top>
				<q-input
					v-model="filter"
					debounce="300"
					placeholder="Szukaj"
					class="col"
					clearable
					rounded
					outlined
					dense
				>
					<template #prepend>
						<q-icon name="search" />
					</template>
				</q-input>
			</template>

			<template #header="props">
				<q-tr :props="props">
					<q-th
						v-for="col in props.cols"
						:key="col.name"
						:props="props"
					>
						{{ col.label }}
					</q-th>
					<q-th auto-width />
				</q-tr>
			</template>

			<template #body="props">
				<q-tr :props="props">
					<q-td
						v-for="col in props.cols"
						:key="col.name"
						:props="props"
					>
						<q-icon
							v-if="['isStaff', 'accredited'].includes(col.name)"
							:name="col.value ? 'check_circle' : 'clear'"
						/>
						<template v-else>{{ col.value }}</template>
					</q-td>
					<q-td auto-width>
						<q-btn
							@click="
								selectedParticipant = participants.find(
									(element) => element.id === props.key
								);
								participantDialog = true;
							"
							icon="o_contact_page"
							no-caps
							round
							flat
							color="grey-5"
							size="1rem"
						/>
					</q-td>
				</q-tr>
			</template>

			<template #loading>
				<q-markup-table>
					<tbody>
						<tr v-for="n in 10" :key="n">
							<td v-for="m in 7" :key="m" class="text-left">
								<q-skeleton animation="fade" type="text" />
							</td>
						</tr>
					</tbody>
				</q-markup-table>
			</template>

			<template #no-data="{ filter }">
				<EmptyComponent
					v-if="!loading"
					icon="search"
					primary="Brak uczestników!"
					:secondary="
						filter
							? 'W podanym filtrze nie znaleziono żadnych uczestników.'
							: 'Nie znaleziono żadnych uczestników.'
					"
					class="q-my-md"
				/>
			</template>
		</q-table>
	</div>

	<InfoPointParticipantDialog
		v-model="participantDialog"
		:participant="selectedParticipant"
		@accredit-participant-dialog-request="accreditParticipantDialog = true"
		@tshirt-give-out-dialog-request="
			(tshirt) => {
				tshirtGiveOutDialog = true;
				selectedTshirt = tshirt;
			}
		"
	/>

	<InfoPointParticipantAccreditDialog
		v-model="accreditParticipantDialog"
		:participant="selectedParticipant"
	/>

	<InfoPointParticipantTshirtGiveOutDialog
		v-model="tshirtGiveOutDialog"
		:participant="selectedParticipant"
		:tshirt="selectedTshirt"
	/>
</template>
