<!--
  GradeInput.vue
  Saisie de note avec slider, mention automatique et notes rapides.

  Props:
    - modelValue (Number): Note actuelle
    - scale (String): Échelle '0-20' ou '0-100'
    - showSlider (Boolean): Afficher le slider
    - showQuickGrades (Boolean): Afficher les notes rapides
    - showPassStatus (Boolean): Afficher le statut validé/non validé

  Events:
    - @update:modelValue: Émis au changement

  Example:
    <GradeInput v-model="grade" scale="0-20" />
-->
<script setup>
import { ref, computed, watch } from 'vue'
import { Button, Badge } from 'frappe-ui'
import { CheckCircle, XCircle } from 'lucide-vue-next'

const props = defineProps({
  modelValue: {
    type: Number,
    default: 0,
  },
  scale: {
    type: String,
    default: '0-20',
  },
  showSlider: {
    type: Boolean,
    default: true,
  },
  showQuickGrades: {
    type: Boolean,
    default: true,
  },
  showPassStatus: {
    type: Boolean,
    default: true,
  },
})

const emit = defineEmits(['update:modelValue'])

const internalGrade = ref(props.modelValue)

watch(() => props.modelValue, (newVal) => {
  internalGrade.value = newVal
})

watch(internalGrade, (newVal) => {
  emit('update:modelValue', newVal)
})

const max = computed(() => props.scale === '0-100' ? 100 : 20)
const step = computed(() => props.scale === '0-100' ? 1 : 0.5)
const passingGrade = computed(() => props.scale === '0-100' ? 50 : 10)
const isPassing = computed(() => internalGrade.value >= passingGrade.value)

const mentions = computed(() => {
  if (props.scale === '0-100') {
    return [
      { min: 90, label: 'Excellent', color: 'text-green-600', theme: 'green' },
      { min: 80, label: 'Très Bien', color: 'text-green-500', theme: 'green' },
      { min: 70, label: 'Bien', color: 'text-blue-500', theme: 'blue' },
      { min: 60, label: 'Assez Bien', color: 'text-blue-400', theme: 'blue' },
      { min: 50, label: 'Passable', color: 'text-yellow-600', theme: 'yellow' },
      { min: 0, label: 'Insuffisant', color: 'text-red-500', theme: 'red' },
    ]
  }
  return [
    { min: 18, label: 'Excellent', color: 'text-green-600', theme: 'green' },
    { min: 16, label: 'Très Bien', color: 'text-green-500', theme: 'green' },
    { min: 14, label: 'Bien', color: 'text-blue-500', theme: 'blue' },
    { min: 12, label: 'Assez Bien', color: 'text-blue-400', theme: 'blue' },
    { min: 10, label: 'Passable', color: 'text-yellow-600', theme: 'yellow' },
    { min: 0, label: 'Insuffisant', color: 'text-red-500', theme: 'red' },
  ]
})

const currentMention = computed(() => {
  return mentions.value.find((m) => internalGrade.value >= m.min) || mentions.value[mentions.value.length - 1]
})

const quickGrades = computed(() => {
  if (props.scale === '0-100') {
    return [0, 50, 60, 70, 80, 90, 100]
  }
  return [0, 8, 10, 12, 14, 16, 18, 20]
})

const handleInput = (e) => {
  let value = parseFloat(e.target.value)
  if (isNaN(value)) {
    internalGrade.value = 0
    return
  }
  internalGrade.value = Math.max(0, Math.min(max.value, value))
}

const increment = () => {
  internalGrade.value = Math.min(max.value, internalGrade.value + step.value)
}

const decrement = () => {
  internalGrade.value = Math.max(0, internalGrade.value - step.value)
}

const setQuickGrade = (grade) => {
  internalGrade.value = grade
}
</script>

<template>
  <div class="space-y-3">
    <!-- Slider -->
    <div v-if="showSlider" class="space-y-2">
      <input
        type="range"
        v-model.number="internalGrade"
        :min="0"
        :max="max"
        :step="step"
        class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
      />
      <div class="flex justify-between text-xs text-gray-500">
        <span>0</span>
        <span>{{ passingGrade }} (min)</span>
        <span>{{ max }}</span>
      </div>
    </div>

    <!-- Input avec boutons -->
    <div class="flex items-center gap-2">
      <Button variant="subtle" size="sm" @click="decrement">-</Button>

      <div class="relative">
        <input
          type="number"
          :value="internalGrade"
          :min="0"
          :max="max"
          :step="step"
          class="w-24 px-3 py-2 text-center text-lg font-bold border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          :class="currentMention?.color"
          @input="handleInput"
        />
        <span class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 text-sm">
          /{{ max }}
        </span>
      </div>

      <Button variant="subtle" size="sm" @click="increment">+</Button>
    </div>

    <!-- Mention et statut -->
    <div class="flex items-center justify-between">
      <Badge v-if="currentMention" :theme="currentMention.theme">
        {{ currentMention.label }}
      </Badge>
      <span v-if="showPassStatus" class="text-sm flex items-center gap-1">
        <CheckCircle v-if="isPassing" class="w-4 h-4 text-green-500" />
        <XCircle v-else class="w-4 h-4 text-red-500" />
        {{ isPassing ? 'Validé' : 'Non validé' }}
      </span>
    </div>

    <!-- Notes rapides -->
    <div v-if="showQuickGrades" class="flex flex-wrap gap-1">
      <button
        v-for="grade in quickGrades"
        :key="grade"
        type="button"
        class="px-2 py-1 text-xs rounded border transition-colors"
        :class="internalGrade === grade
          ? 'bg-blue-100 border-blue-500 text-blue-700'
          : 'bg-white border-gray-300 hover:border-blue-300'"
        @click="setQuickGrade(grade)"
      >
        {{ grade }}
      </button>
    </div>
  </div>
</template>
