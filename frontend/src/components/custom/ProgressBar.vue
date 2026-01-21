<!--
  ProgressBar.vue
  Affiche une barre de progression avec label.

  Props:
    - percent (Number): Pourcentage de progression (0-100)
    - label (String): Label affiché à droite (optionnel)
    - color (String): Couleur de la barre (default: cntemad-primary)
-->
<script setup>
defineProps({
  percent: {
    type: Number,
    required: true,
    validator: (v) => v >= 0 && v <= 100,
  },
  label: {
    type: String,
    default: '',
  },
  color: {
    type: String,
    default: 'bg-cntemad-primary',
  },
})
</script>

<template>
  <div>
    <div class="flex justify-between items-center mb-2">
      <span class="text-sm font-medium">{{ Math.round(percent) }}%</span>
      <span v-if="label" class="text-sm text-gray-500">{{ label }}</span>
    </div>
    <div class="w-full bg-gray-200 rounded-full h-2.5">
      <div
        class="h-2.5 rounded-full transition-all duration-300"
        :class="color"
        :style="{ width: `${percent}%` }"
      ></div>
    </div>
  </div>
</template>
