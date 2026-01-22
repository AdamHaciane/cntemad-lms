<!--
  StatsCard.vue
  Carte KPI avec icône, valeur et variation.

  Props:
    - icon (String): Nom d'icône ou emoji
    - label (String): Label du KPI
    - value (Number|String): Valeur principale
    - change (Number): Variation en % (optionnel)
    - size (String): sm, md, lg
    - link (String): Lien cliquable (optionnel)

  Example:
    <StatsCard icon="👥" label="Étudiants" :value="1250" :change="12" />
-->
<script setup>
import { Card } from 'frappe-ui'
import { computed } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps({
  icon: {
    type: String,
    default: '📊',
  },
  label: {
    type: String,
    required: true,
  },
  value: {
    type: [Number, String],
    required: true,
  },
  change: {
    type: Number,
    default: null,
  },
  size: {
    type: String,
    default: 'md',
    validator: (v) => ['sm', 'md', 'lg'].includes(v),
  },
  link: {
    type: String,
    default: null,
  },
})

const router = useRouter()

const formattedValue = computed(() => {
  if (typeof props.value === 'number') {
    return new Intl.NumberFormat('fr-MG').format(props.value)
  }
  return props.value
})

const changeClass = computed(() => {
  if (props.change === null) return ''
  return props.change >= 0 ? 'text-green-600' : 'text-red-600'
})

const changeIcon = computed(() => {
  if (props.change === null) return ''
  return props.change >= 0 ? '↑' : '↓'
})

const sizeClasses = computed(() => ({
  sm: { card: 'p-3', icon: 'text-xl', value: 'text-xl', label: 'text-xs' },
  md: { card: 'p-4', icon: 'text-2xl', value: 'text-2xl', label: 'text-sm' },
  lg: { card: 'p-5', icon: 'text-3xl', value: 'text-3xl', label: 'text-base' },
}[props.size]))

const handleClick = () => {
  if (props.link) {
    router.push(props.link)
  }
}
</script>

<template>
  <Card
    :class="[
      sizeClasses.card,
      link ? 'cursor-pointer hover:shadow-md transition-shadow' : ''
    ]"
    @click="handleClick"
  >
    <div class="flex items-start justify-between">
      <div>
        <p class="text-gray-500" :class="sizeClasses.label">{{ label }}</p>
        <p class="font-bold text-gray-900 mt-1" :class="sizeClasses.value">
          {{ formattedValue }}
        </p>
        <p v-if="change !== null" class="mt-1 text-sm" :class="changeClass">
          {{ changeIcon }} {{ Math.abs(change) }}% vs mois dernier
        </p>
      </div>
      <span :class="sizeClasses.icon">{{ icon }}</span>
    </div>
  </Card>
</template>
