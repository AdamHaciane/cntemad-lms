<!--
  ProgressBar.vue
  Affiche une barre de progression EC/année avec couleurs distinctes.

  Props:
    - value (Number): Valeur actuelle (ex: 8 EC validés)
    - max (Number): Valeur maximale (ex: 12 EC total)
    - label (String): Label affiché (ex: "8/12 EC validés")
    - showPercent (Boolean): Afficher le pourcentage
    - size (String): Taille: sm, md, lg
    - animated (Boolean): Animation au chargement

  Example:
    <ProgressBar :value="8" :max="12" label="EC validés" showPercent />
-->
<script setup>
import { computed } from 'vue'

const props = defineProps({
  value: {
    type: Number,
    default: 0,
  },
  max: {
    type: Number,
    default: 100,
  },
  label: {
    type: String,
    default: '',
  },
  showPercent: {
    type: Boolean,
    default: true,
  },
  size: {
    type: String,
    default: 'md',
    validator: (v) => ['sm', 'md', 'lg'].includes(v),
  },
  animated: {
    type: Boolean,
    default: true,
  },
})

const percent = computed(() => {
  if (props.max <= 0) return 0
  const p = (props.value / props.max) * 100
  return Math.min(Math.max(p, 0), 100)
})

const barColor = computed(() => {
  if (percent.value === 100) return 'bg-green-500'
  if (percent.value >= 70) return 'bg-green-400'
  if (percent.value >= 30) return 'bg-yellow-400'
  return 'bg-cntemad-primary'
})

const sizeClasses = computed(() => ({
  sm: 'h-1.5',
  md: 'h-2.5',
  lg: 'h-4',
}[props.size]))

const displayLabel = computed(() => {
  if (props.label) return `${props.value}/${props.max} ${props.label}`
  return ''
})
</script>

<template>
  <div>
    <div class="flex justify-between items-center mb-1">
      <span v-if="showPercent" class="text-sm font-medium text-gray-700">
        {{ Math.round(percent) }}%
      </span>
      <span v-if="displayLabel" class="text-sm text-gray-500">
        {{ displayLabel }}
      </span>
    </div>
    <div class="w-full bg-gray-200 rounded-full overflow-hidden" :class="sizeClasses">
      <div
        class="rounded-full"
        :class="[
          barColor,
          sizeClasses,
          animated ? 'transition-all duration-500 ease-out' : ''
        ]"
        :style="{ width: `${percent}%` }"
      ></div>
    </div>
  </div>
</template>
