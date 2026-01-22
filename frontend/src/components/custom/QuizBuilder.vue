<template>
  <div class="quiz-builder">
    <!-- Quiz settings -->
    <Card class="mb-4">
      <template #title>Paramètres du quiz</template>
      <div class="p-4 grid grid-cols-1 md:grid-cols-3 gap-4">
        <Input
          v-model="quiz.title"
          label="Titre du quiz"
          placeholder="Quiz de validation"
        />
        <Input
          v-model.number="quiz.passing_percentage"
          type="number"
          label="Score minimum (%)"
          min="0"
          max="100"
        />
        <Input
          v-model.number="quiz.max_attempts"
          type="number"
          label="Tentatives max"
          min="1"
          max="10"
        />
        <Input
          v-model.number="quiz.time_limit"
          type="number"
          label="Durée limite (min)"
          min="0"
          placeholder="0 = illimité"
        />
      </div>
    </Card>

    <!-- Questions list -->
    <div class="space-y-4">
      <div
        v-for="(question, qIndex) in quiz.questions"
        :key="qIndex"
        class="border rounded-lg bg-white"
      >
        <!-- Question header -->
        <div class="flex items-center gap-3 p-4 border-b bg-gray-50 rounded-t-lg">
          <div class="w-8 h-8 bg-blue-500 text-white rounded-full flex items-center justify-center font-medium">
            {{ qIndex + 1 }}
          </div>
          <span class="font-medium flex-1">Question {{ qIndex + 1 }}</span>
          <Select
            v-model="question.type"
            :options="questionTypes"
            class="w-40"
          />
          <button
            type="button"
            class="p-2 text-gray-400 hover:text-red-500 transition-colors"
            @click="removeQuestion(qIndex)"
          >
            <Trash2 class="w-5 h-5" />
          </button>
        </div>

        <!-- Question content -->
        <div class="p-4 space-y-4">
          <Textarea
            v-model="question.question"
            label="Question"
            placeholder="Entrez votre question..."
            rows="2"
          />

          <!-- Options -->
          <div>
            <div class="flex items-center justify-between mb-2">
              <label class="text-sm font-medium text-gray-700">Options</label>
              <Button
                variant="ghost"
                size="sm"
                @click="addOption(qIndex)"
                :disabled="question.options.length >= 6"
              >
                <Plus class="w-4 h-4 mr-1" />
                Ajouter option
              </Button>
            </div>

            <div class="space-y-2">
              <div
                v-for="(option, oIndex) in question.options"
                :key="oIndex"
                class="flex items-center gap-2"
              >
                <!-- Correct checkbox -->
                <button
                  type="button"
                  class="w-6 h-6 rounded-full border-2 flex items-center justify-center transition-colors"
                  :class="option.is_correct
                    ? 'border-green-500 bg-green-500 text-white'
                    : 'border-gray-300 hover:border-green-400'"
                  @click="toggleCorrect(qIndex, oIndex)"
                  :title="option.is_correct ? 'Bonne réponse' : 'Marquer comme correcte'"
                >
                  <Check v-if="option.is_correct" class="w-4 h-4" />
                </button>

                <!-- Option text -->
                <Input
                  v-model="option.option"
                  :placeholder="`Option ${oIndex + 1}`"
                  class="flex-1"
                />

                <!-- Remove option -->
                <button
                  type="button"
                  class="p-2 text-gray-400 hover:text-red-500 transition-colors"
                  @click="removeOption(qIndex, oIndex)"
                  :disabled="question.options.length <= 2"
                >
                  <X class="w-4 h-4" />
                </button>
              </div>
            </div>

            <p v-if="!hasCorrectAnswer(question)" class="text-xs text-red-500 mt-2">
              Sélectionnez au moins une bonne réponse
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Add question button -->
    <Button
      variant="outline"
      class="w-full mt-4"
      @click="addQuestion"
    >
      <Plus class="w-4 h-4 mr-2" />
      Ajouter une question
    </Button>

    <!-- Preview -->
    <div v-if="quiz.questions.length > 0" class="mt-6 p-4 bg-gray-50 rounded-lg">
      <div class="flex items-center justify-between">
        <div>
          <p class="font-medium text-gray-900">{{ quiz.questions.length }} question(s)</p>
          <p class="text-sm text-gray-500">
            Score requis: {{ quiz.passing_percentage }}% •
            {{ quiz.max_attempts }} tentative(s) •
            {{ quiz.time_limit > 0 ? quiz.time_limit + ' min' : 'Sans limite' }}
          </p>
        </div>
        <Badge v-if="isValid" theme="green">Valide</Badge>
        <Badge v-else theme="red">Incomplet</Badge>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { Button, Card, Input, Textarea, Select, Badge } from 'frappe-ui'
import { Plus, Trash2, X, Check } from 'lucide-vue-next'

const props = defineProps({
  modelValue: {
    type: Object,
    default: () => ({
      title: '',
      passing_percentage: 70,
      max_attempts: 3,
      time_limit: 0,
      questions: []
    })
  }
})

const emit = defineEmits(['update:modelValue'])

const quiz = ref({ ...props.modelValue })

// Watch for external changes
watch(() => props.modelValue, (newVal) => {
  quiz.value = { ...newVal }
}, { deep: true })

// Emit changes
watch(quiz, (newVal) => {
  emit('update:modelValue', newVal)
}, { deep: true })

const questionTypes = [
  { label: 'Choix unique', value: 'Choices' },
  { label: 'Choix multiples', value: 'Multiple' }
]

const isValid = computed(() => {
  if (quiz.value.questions.length === 0) return false

  return quiz.value.questions.every(q => {
    if (!q.question.trim()) return false
    if (q.options.length < 2) return false
    if (!q.options.some(o => o.is_correct)) return false
    if (q.options.some(o => !o.option.trim())) return false
    return true
  })
})

const addQuestion = () => {
  quiz.value.questions.push({
    question: '',
    type: 'Choices',
    options: [
      { option: '', is_correct: false },
      { option: '', is_correct: false }
    ]
  })
}

const removeQuestion = (index) => {
  quiz.value.questions.splice(index, 1)
}

const addOption = (qIndex) => {
  if (quiz.value.questions[qIndex].options.length < 6) {
    quiz.value.questions[qIndex].options.push({
      option: '',
      is_correct: false
    })
  }
}

const removeOption = (qIndex, oIndex) => {
  if (quiz.value.questions[qIndex].options.length > 2) {
    quiz.value.questions[qIndex].options.splice(oIndex, 1)
  }
}

const toggleCorrect = (qIndex, oIndex) => {
  const question = quiz.value.questions[qIndex]
  const option = question.options[oIndex]

  if (question.type === 'Choices') {
    // Single choice - unselect others
    question.options.forEach((o, i) => {
      o.is_correct = i === oIndex
    })
  } else {
    // Multiple choice - toggle
    option.is_correct = !option.is_correct
  }
}

const hasCorrectAnswer = (question) => {
  return question.options.some(o => o.is_correct)
}

// Expose methods
defineExpose({
  getQuiz: () => quiz.value,
  setQuiz: (data) => {
    quiz.value = { ...data }
  },
  isValid: () => isValid.value,
  clear: () => {
    quiz.value = {
      title: '',
      passing_percentage: 70,
      max_attempts: 3,
      time_limit: 0,
      questions: []
    }
  }
})
</script>
