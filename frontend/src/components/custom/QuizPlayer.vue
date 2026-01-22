<!--
  QuizPlayer.vue
  Lecteur de quiz QCM complet avec score et feedback.

  Props:
    - questions (Array): Liste des questions
    - title (String): Titre du quiz
    - timeLimit (Number): Limite de temps en secondes (0 = pas de limite)
    - showFeedback (Boolean): Feedback immédiat après chaque question
    - passingScore (Number): Score minimum pour réussir (pourcentage)

  Events:
    - @complete(result): Quiz terminé avec résultats
    - @timeout: Temps écoulé

  Example:
    <QuizPlayer
      :questions="quizQuestions"
      title="Quiz Module 1"
      :timeLimit="600"
      :passingScore="70"
      showFeedback
      @complete="handleQuizComplete"
    />
-->
<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { Card, Button, Badge } from 'frappe-ui'
import QuestionCard from './QuestionCard.vue'
import ProgressBar from './ProgressBar.vue'

const props = defineProps({
  questions: {
    type: Array,
    required: true,
    default: () => [],
  },
  title: {
    type: String,
    default: 'Quiz',
  },
  timeLimit: {
    type: Number,
    default: 0, // 0 = no limit
  },
  showFeedback: {
    type: Boolean,
    default: false,
  },
  passingScore: {
    type: Number,
    default: 70,
  },
})

const emit = defineEmits(['complete', 'timeout', 'answer'])

// State
const currentQuestionIndex = ref(0)
const answers = ref({})
const quizState = ref('intro') // intro, playing, review, result
const timeRemaining = ref(props.timeLimit)
const timerInterval = ref(null)

// Computed
const totalQuestions = computed(() => props.questions.length)

const currentQuestion = computed(() => {
  return props.questions[currentQuestionIndex.value] || null
})

const progress = computed(() => {
  const answered = Object.keys(answers.value).length
  return (answered / totalQuestions.value) * 100
})

const answeredCount = computed(() => Object.keys(answers.value).length)

const isLastQuestion = computed(() => {
  return currentQuestionIndex.value === totalQuestions.value - 1
})

const canFinish = computed(() => {
  // Allow finish if all questions answered or if no feedback mode
  return answeredCount.value === totalQuestions.value
})

const score = computed(() => {
  let correct = 0

  for (let i = 0; i < props.questions.length; i++) {
    const question = props.questions[i]
    const answer = answers.value[i]

    if (answer === undefined || answer === null) continue

    const correctAnswers = Array.isArray(question.correctAnswer)
      ? question.correctAnswer
      : [question.correctAnswer]

    const userAnswers = Array.isArray(answer) ? answer : [answer]

    // Check if answers match
    const isCorrect =
      userAnswers.length === correctAnswers.length &&
      userAnswers.every((a) => correctAnswers.includes(a))

    if (isCorrect) correct++
  }

  return correct
})

const scorePercent = computed(() => {
  if (totalQuestions.value === 0) return 0
  return Math.round((score.value / totalQuestions.value) * 100)
})

const hasPassed = computed(() => {
  return scorePercent.value >= props.passingScore
})

const formattedTime = computed(() => {
  const minutes = Math.floor(timeRemaining.value / 60)
  const seconds = timeRemaining.value % 60
  return `${minutes}:${seconds.toString().padStart(2, '0')}`
})

// Methods
const startQuiz = () => {
  quizState.value = 'playing'
  currentQuestionIndex.value = 0
  answers.value = {}

  if (props.timeLimit > 0) {
    startTimer()
  }
}

const startTimer = () => {
  timeRemaining.value = props.timeLimit
  timerInterval.value = setInterval(() => {
    timeRemaining.value--

    if (timeRemaining.value <= 0) {
      stopTimer()
      handleTimeout()
    }
  }, 1000)
}

const stopTimer = () => {
  if (timerInterval.value) {
    clearInterval(timerInterval.value)
    timerInterval.value = null
  }
}

const handleTimeout = () => {
  emit('timeout')
  finishQuiz()
}

const handleAnswer = (answer) => {
  answers.value[currentQuestionIndex.value] = answer
  emit('answer', {
    questionIndex: currentQuestionIndex.value,
    answer,
  })
}

const goToNext = () => {
  if (currentQuestionIndex.value < totalQuestions.value - 1) {
    currentQuestionIndex.value++
  } else if (!props.showFeedback) {
    finishQuiz()
  }
}

const goToPrevious = () => {
  if (currentQuestionIndex.value > 0) {
    currentQuestionIndex.value--
  }
}

const goToQuestion = (index) => {
  currentQuestionIndex.value = index
}

const finishQuiz = () => {
  stopTimer()
  quizState.value = 'result'

  const result = {
    score: score.value,
    total: totalQuestions.value,
    percent: scorePercent.value,
    passed: hasPassed.value,
    answers: { ...answers.value },
    timeSpent: props.timeLimit > 0 ? props.timeLimit - timeRemaining.value : null,
  }

  emit('complete', result)
}

const reviewQuiz = () => {
  quizState.value = 'review'
  currentQuestionIndex.value = 0
}

const retryQuiz = () => {
  answers.value = {}
  currentQuestionIndex.value = 0
  timeRemaining.value = props.timeLimit
  quizState.value = 'intro'
}

// Lifecycle
onMounted(() => {
  // Auto-start if no intro needed
  if (props.questions.length === 0) {
    quizState.value = 'result'
  }
})

onUnmounted(() => {
  stopTimer()
})
</script>

<template>
  <div class="quiz-player">
    <!-- Intro Screen -->
    <Card v-if="quizState === 'intro'" class="p-8 text-center">
      <div class="text-5xl mb-4">📝</div>
      <h2 class="text-2xl font-bold text-gray-900 mb-2">{{ title }}</h2>
      <p class="text-gray-600 mb-6">
        {{ totalQuestions }} question{{ totalQuestions > 1 ? 's' : '' }}
        <span v-if="timeLimit > 0">
          • {{ Math.floor(timeLimit / 60) }} min
        </span>
      </p>

      <div class="bg-gray-50 rounded-lg p-4 mb-6 text-left text-sm text-gray-600">
        <h4 class="font-medium text-gray-900 mb-2">Instructions :</h4>
        <ul class="space-y-1">
          <li>• Lisez attentivement chaque question</li>
          <li>• Sélectionnez la ou les bonnes réponses</li>
          <li v-if="showFeedback">• Vous verrez la correction après chaque réponse</li>
          <li>• Score minimum pour valider : {{ passingScore }}%</li>
        </ul>
      </div>

      <Button variant="solid" size="lg" @click="startQuiz">
        Commencer le quiz
      </Button>
    </Card>

    <!-- Playing / Review Screen -->
    <div v-else-if="quizState === 'playing' || quizState === 'review'">
      <!-- Header -->
      <div class="flex items-center justify-between mb-4">
        <div>
          <h2 class="font-semibold text-gray-900">{{ title }}</h2>
          <p class="text-sm text-gray-500">
            Question {{ currentQuestionIndex + 1 }} / {{ totalQuestions }}
          </p>
        </div>

        <div class="flex items-center gap-4">
          <!-- Timer -->
          <div
            v-if="timeLimit > 0 && quizState === 'playing'"
            class="flex items-center gap-2 px-3 py-1 rounded-full"
            :class="timeRemaining < 60 ? 'bg-red-100 text-red-700' : 'bg-gray-100 text-gray-700'"
          >
            <span class="text-lg">⏱️</span>
            <span class="font-mono font-semibold">{{ formattedTime }}</span>
          </div>

          <!-- Review badge -->
          <Badge v-if="quizState === 'review'" theme="blue">
            Mode révision
          </Badge>
        </div>
      </div>

      <!-- Progress Bar -->
      <ProgressBar
        :value="answeredCount"
        :max="totalQuestions"
        class="mb-6"
        label="Progression"
      />

      <!-- Question Card -->
      <QuestionCard
        v-if="currentQuestion"
        :question="currentQuestion"
        :index="currentQuestionIndex"
        :showFeedback="showFeedback || quizState === 'review'"
        :disabled="quizState === 'review'"
        :selectedAnswer="answers[currentQuestionIndex]"
        @answer="handleAnswer"
        @next="goToNext"
      />

      <!-- Navigation -->
      <div class="mt-6 flex items-center justify-between">
        <Button
          variant="outline"
          :disabled="currentQuestionIndex === 0"
          @click="goToPrevious"
        >
          ← Précédent
        </Button>

        <div class="flex gap-2">
          <!-- Question dots -->
          <button
            v-for="(q, i) in questions"
            :key="i"
            class="w-8 h-8 rounded-full text-sm font-medium transition-colors"
            :class="[
              i === currentQuestionIndex
                ? 'bg-cntemad-primary text-white'
                : answers[i] !== undefined
                  ? 'bg-green-100 text-green-700'
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            ]"
            @click="goToQuestion(i)"
          >
            {{ i + 1 }}
          </button>
        </div>

        <div class="flex gap-2">
          <Button
            v-if="!isLastQuestion"
            variant="outline"
            @click="goToNext"
          >
            Suivant →
          </Button>
          <Button
            v-if="canFinish && quizState === 'playing'"
            variant="solid"
            theme="green"
            @click="finishQuiz"
          >
            Terminer
          </Button>
          <Button
            v-if="quizState === 'review'"
            variant="solid"
            @click="quizState = 'result'"
          >
            Voir résultat
          </Button>
        </div>
      </div>
    </div>

    <!-- Result Screen -->
    <Card v-else-if="quizState === 'result'" class="p-8 text-center">
      <div class="text-6xl mb-4">
        {{ hasPassed ? '🎉' : '😔' }}
      </div>

      <h2
        class="text-2xl font-bold mb-2"
        :class="hasPassed ? 'text-green-600' : 'text-red-600'"
      >
        {{ hasPassed ? 'Félicitations !' : 'Dommage...' }}
      </h2>

      <p class="text-gray-600 mb-6">
        {{ hasPassed ? 'Vous avez réussi le quiz !' : 'Vous n\'avez pas atteint le score minimum.' }}
      </p>

      <!-- Score Display -->
      <div class="bg-gray-50 rounded-xl p-6 mb-6">
        <div class="text-5xl font-bold mb-2" :class="hasPassed ? 'text-green-600' : 'text-red-600'">
          {{ scorePercent }}%
        </div>
        <p class="text-gray-600">
          {{ score }} / {{ totalQuestions }} bonnes réponses
        </p>
        <p class="text-sm text-gray-500 mt-2">
          Score minimum : {{ passingScore }}%
        </p>
      </div>

      <!-- Result Details -->
      <div class="grid grid-cols-3 gap-4 mb-6 text-center">
        <div class="bg-green-50 rounded-lg p-3">
          <div class="text-2xl font-bold text-green-600">{{ score }}</div>
          <div class="text-xs text-green-700">Correctes</div>
        </div>
        <div class="bg-red-50 rounded-lg p-3">
          <div class="text-2xl font-bold text-red-600">{{ totalQuestions - score }}</div>
          <div class="text-xs text-red-700">Incorrectes</div>
        </div>
        <div class="bg-blue-50 rounded-lg p-3">
          <div class="text-2xl font-bold text-blue-600">{{ totalQuestions }}</div>
          <div class="text-xs text-blue-700">Total</div>
        </div>
      </div>

      <!-- Actions -->
      <div class="flex flex-col sm:flex-row gap-3 justify-center">
        <Button variant="outline" @click="reviewQuiz">
          Revoir les réponses
        </Button>
        <Button v-if="!hasPassed" variant="solid" @click="retryQuiz">
          Réessayer
        </Button>
      </div>
    </Card>
  </div>
</template>

<style scoped>
.quiz-player {
  max-width: 800px;
  margin: 0 auto;
}
</style>
