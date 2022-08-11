<script setup lang="ts">
	defineProps({
		icon: String,
		primary: String,
		secondary: String,
	});
</script>

<template>
	<div
		class="col column flex-center q-gutter-md text-grey-5"
		style="height: 100%"
	>
		<q-icon :name="icon" size="5rem" />
		<div class="text-h4">{{ primary }}</div>
		<div class="text-secondary q-mb-lg">{{ secondary }}</div>
	</div>
</template>
