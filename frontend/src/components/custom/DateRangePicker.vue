<!--
  DateRangePicker.vue
  Sélecteur de période avec presets.

  Props:
    - startDate (String): Date de début
    - endDate (String): Date de fin

  Events:
    - @change({ start, end }): Émis au changement

  Example:
    <DateRangePicker
      v-model:startDate="start"
      v-model:endDate="end"
      @change="handleDateChange"
    />
-->
<script setup>
import { Button } from 'frappe-ui'
import { ref, computed } from 'vue'

const props = defineProps({
  startDate: {
    type: String,
    default: '',
  },
  endDate: {
    type: String,
    default: '',
  },
})

const emit = defineEmits(['update:startDate', 'update:endDate', 'change'])

const presets = [
  { label: 'Aujourd\'hui', days: 0 },
  { label: '7 jours', days: 7 },
  { label: '30 jours', days: 30 },
  { label: '3 mois', days: 90 },
  { label: '1 an', days: 365 },
]

const formatDate = (date) => {
  return date.toISOString().split('T')[0]
}

const applyPreset = (days) => {
  const end = new Date()
  const start = new Date()
  start.setDate(start.getDate() - days)

  emit('update:startDate', formatDate(start))
  emit('update:endDate', formatDate(end))
  emit('change', { start: formatDate(start), end: formatDate(end) })
}

const handleStartChange = (e) => {
  emit('update:startDate', e.target.value)
  if (props.endDate) {
    emit('change', { start: e.target.value, end: props.endDate })
  }
}

const handleEndChange = (e) => {
  emit('update:endDate', e.target.value)
  if (props.startDate) {
    emit('change', { start: props.startDate, end: e.target.value })
  }
}
</script>

<template>
  <div class="space-y-3">
    <!-- Presets -->
    <div class="flex flex-wrap gap-2">
      <Button
        v-for="preset in presets"
        :key="preset.days"
        variant="subtle"
        size="sm"
        @click="applyPreset(preset.days)"
      >
        {{ preset.label }}
      </Button>
    </div>

    <!-- Date inputs -->
    <div class="flex flex-col sm:flex-row gap-3">
      <div class="flex-1">
        <label class="block text-sm text-gray-600 mb-1">Du</label>
        <input
          type="date"
          :value="startDate"
          class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-cntemad-primary focus:border-transparent"
          @change="handleStartChange"
        />
      </div>
      <div class="flex-1">
        <label class="block text-sm text-gray-600 mb-1">Au</label>
        <input
          type="date"
          :value="endDate"
          class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-cntemad-primary focus:border-transparent"
          @change="handleEndChange"
        />
      </div>
    </div>
  </div>
</template>
