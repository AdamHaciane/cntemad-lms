<!--
  QuestionCard.vue
  Carte de question QCM pour quiz.

  Props:
    - question (Object): { text, options, type, correctAnswer }
    - index (Number): Numéro de question
    - showFeedback (Boolean): Afficher correction immédiate
    - disabled (Boolean): Désactiver les réponses
    - selectedAnswer (Array|String): Réponse(s) sélectionnée(s)

  Events:
    - @answer(value): Réponse sélectionnée
    - @next: Passer à la question suivante

  Example:
    <QuestionCard
      :question="{ text: 'Quelle est...', options: [...], type: 'single' }"
      :index="0"
      showFeedback
      @answer="handleAnswer"
    />
-->
<script setup>
import { ref, computed, watch } from 'vue'
import { Card, Button, Badge } from 'frappe-ui'

const props = defineProps({
  question: {
    type: Object,
    required: true,
  },
  index: {
    type: Number,
    default: 0,
  },
  showFeedback: {
    type: Boolean,
    default: false,
  },
  disabled: {
    type: Boolean,
    default: false,
  },
  selectedAnswer: {
    type: [Array, String, Number],
    default: null,
  },
})

const emit = defineEmits(['answer', 'next'])

// Local state for selection
const localSelection = ref(props.selectedAnswer)
const hasAnswered = ref(false)

// Computed
const isMultiple = computed(() => props.question.type === 'multiple')

const correctAnswer = computed(() => {
  if (Array.isArray(props.question.correctAnswer)) {
    return props.question.correctAnswer
  }
  return [props.question.correctAnswer]
})

const isCorrect = computed(() => {
  if (!hasAnswered.value || !localSelection.value) return null

  if (isMultiple.value) {
    const selected = Array.isArray(localSelection.value)
      ? localSelection.value
      : [localSelection.value]

    // Check if arrays match
    return (
      selected.length === correctAnswer.value.length &&
      selected.every((s) => correctAnswer.value.includes(s))
    )
  }

  return correctAnswer.value.includes(localSelection.value)
})

// Methods
const selectOption = (optionIndex) => {
  if (props.disabled || (hasAnswered.value && props.showFeedback)) return

  if (isMultiple.value) {
    // Multiple selection
    const current = Array.isArray(localSelection.value) ? [...localSelection.value] : []
    const idx = current.indexOf(optionIndex)

    if (idx === -1) {
      current.push(optionIndex)
    } else {
      current.splice(idx, 1)
    }
    localSelection.value = current
  } else {
    // Single selection
    localSelection.value = optionIndex
  }

  emit('answer', localSelection.value)
}

const isOptionSelected = (optionIndex) => {
  if (isMultiple.value) {
    return Array.isArray(localSelection.value) && localSelection.value.includes(optionIndex)
  }
  return localSelection.value === optionIndex
}

const isOptionCorrect = (optionIndex) => {
  return correctAnswer.value.includes(optionIndex)
}

const getOptionClass = (optionIndex) => {
  const selected = isOptionSelected(optionIndex)
  const correct = isOptionCorrect(optionIndex)
  const showResult = hasAnswered.value && props.showFeedback

  if (showResult) {
    if (correct) {
      return 'border-green-500 bg-green-50 text-green-800'
    }
    if (selected && !correct) {
      return 'border-red-500 bg-red-50 text-red-800'
    }
  }

  if (selected) {
    return 'border-cntemad-primary bg-cntemad-primary/10 text-cntemad-primary'
  }

  return 'border-gray-200 hover:border-gray-300 hover:bg-gray-50'
}

const submitAnswer = () => {
  if (!localSelection.value || (Array.isArray(localSelection.value) && localSelection.value.length === 0)) {
    return
  }
  hasAnswered.value = true
  emit('answer', localSelection.value)
}

const handleNext = () => {
  emit('next')
}

// Sync with prop changes
watch(
  () => props.selectedAnswer,
  (newVal) => {
    localSelection.value = newVal
  }
)

// Reset on question change
watch(
  () => props.question,
  () => {
    localSelection.value = null
    hasAnswered.value = false
  }
)
</script>

<template>
  <Card class="p-6">
    <!-- Question Header -->
    <div class="flex items-start gap-3 mb-4">
      <span class="flex-shrink-0 w-8 h-8 rounded-full bg-cntemad-primary text-white flex items-center justify-center font-semibold text-sm">
        {{ index + 1 }}
      </span>
      <div class="flex-1">
        <p class="font-medium text-gray-900">{{ question.text }}</p>
        <p v-if="isMultiple" class="text-sm text-gray-500 mt-1">
          (Plusieurs réponses possibles)
        </p>
      </div>
    </div>

    <!-- Options -->
    <div class="space-y-3 mb-6">
      <button
        v-for="(option, optIndex) in question.options"
        :key="optIndex"
        type="button"
        class="w-full text-left p-4 rounded-lg border-2 transition-all flex items-center gap-3"
        :class="getOptionClass(optIndex)"
        :disabled="disabled || (hasAnswered && showFeedback)"
        @click="selectOption(optIndex)"
      >
        <!-- Checkbox/Radio indicator -->
        <span
          class="w-5 h-5 rounded flex-shrink-0 border-2 flex items-center justify-center"
          :class="[
            isMultiple ? 'rounded' : 'rounded-full',
            isOptionSelected(optIndex)
              ? 'border-current bg-current'
              : 'border-gray-300'
          ]"
        >
          <svg
            v-if="isOptionSelected(optIndex)"
            class="w-3 h-3 text-white"
            fill="currentColor"
            viewBox="0 0 20 20"
          >
            <path
              fill-rule="evenodd"
              d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
              clip-rule="evenodd"
            />
          </svg>
        </span>

        <!-- Option text -->
        <span class="flex-1">{{ option }}</span>

        <!-- Feedback icon -->
        <span
          v-if="hasAnswered && showFeedback"
          class="flex-shrink-0"
        >
          <span v-if="isOptionCorrect(optIndex)" class="text-green-500 text-xl">✓</span>
          <span v-else-if="isOptionSelected(optIndex)" class="text-red-500 text-xl">✗</span>
        </span>
      </button>
    </div>

    <!-- Feedback Message -->
    <div
      v-if="hasAnswered && showFeedback"
      class="p-4 rounded-lg mb-4"
      :class="isCorrect ? 'bg-green-50 text-green-800' : 'bg-red-50 text-red-800'"
    >
      <div class="flex items-center gap-2 font-medium">
        <span v-if="isCorrect">✓ Bonne réponse !</span>
        <span v-else>✗ Mauvaise réponse</span>
      </div>
      <p v-if="question.explanation" class="text-sm mt-2 opacity-90">
        {{ question.explanation }}
      </p>
    </div>

    <!-- Actions -->
    <div class="flex justify-end gap-3">
      <Button
        v-if="!hasAnswered && !disabled"
        variant="solid"
        :disabled="!localSelection || (Array.isArray(localSelection) && localSelection.length === 0)"
        @click="submitAnswer"
      >
        Valider
      </Button>
      <Button
        v-if="hasAnswered && showFeedback"
        variant="solid"
        @click="handleNext"
      >
        Suivant →
      </Button>
    </div>
  </Card>
</template>
