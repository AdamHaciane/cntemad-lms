<!--
  Quiz.vue
  Page de quiz pour validation d'un EC.

  Route: /ec/:id/quiz
-->
<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Card, Button, Spinner, Alert, Dialog } from 'frappe-ui'
import { createResource } from 'frappe-ui'
import QuizPlayer from '@/components/custom/QuizPlayer.vue'

const route = useRoute()
const router = useRouter()

// State
const ec = ref(null)
const quiz = ref(null)
const questions = ref([])
const loading = ref(true)
const error = ref(null)
const submitting = ref(false)
const result = ref(null)
const showExitDialog = ref(false)

// Resources
const quizResource = createResource({
  url: 'cntemad_lms.api.quiz.get_quiz',
  auto: false,
  onSuccess(data) {
    ec.value = data.ec
    quiz.value = data.quiz
    questions.value = data.questions || []
  },
  onError(err) {
    error.value = err.message || 'Erreur de chargement du quiz'
  },
})

const submitResource = createResource({
  url: 'cntemad_lms.api.quiz.submit_quiz',
  auto: false,
  onSuccess(data) {
    result.value = data
  },
  onError(err) {
    error.value = err.message || 'Erreur lors de la soumission'
  },
})

// Computed
const quizTitle = computed(() => quiz.value?.title || ec.value?.title || 'Quiz')

const passingScore = computed(() => quiz.value?.passing_score || 70)

const timeLimit = computed(() => {
  // Convert minutes to seconds
  const minutes = quiz.value?.time_limit || 0
  return minutes * 60
})

// Methods
const fetchQuiz = async () => {
  loading.value = true
  error.value = null

  try {
    await quizResource.fetch({ ec_id: route.params.id })
  } finally {
    loading.value = false
  }
}

const handleQuizComplete = async (quizResult) => {
  submitting.value = true
  error.value = null

  try {
    // Format answers for submission
    const formattedAnswers = []
    for (const [index, answer] of Object.entries(quizResult.answers)) {
      const question = questions.value[parseInt(index)]
      if (question) {
        formattedAnswers.push({
          question_id: question.name || question.id,
          answer: Array.isArray(answer) ? answer : [answer],
        })
      }
    }

    await submitResource.fetch({
      ec_id: route.params.id,
      quiz_id: quiz.value?.name,
      answers: JSON.stringify(formattedAnswers),
      time_spent: quizResult.timeSpent,
    })
  } finally {
    submitting.value = false
  }
}

const handleTimeout = () => {
  // Quiz timed out, submit whatever we have
  handleQuizComplete({
    answers: {},
    timeSpent: timeLimit.value,
  })
}

const confirmExit = () => {
  showExitDialog.value = true
}

const exitQuiz = () => {
  showExitDialog.value = false
  router.push(`/ec/${route.params.id}`)
}

const goToDashboard = () => {
  router.push('/dashboard')
}

const goToEC = () => {
  router.push(`/ec/${route.params.id}`)
}

const retryQuiz = () => {
  result.value = null
  fetchQuiz()
}

// Prevent accidental page leave during quiz
const handleBeforeUnload = (e) => {
  if (!result.value && questions.value.length > 0) {
    e.preventDefault()
    e.returnValue = ''
  }
}

// Lifecycle
onMounted(() => {
  fetchQuiz()
  window.addEventListener('beforeunload', handleBeforeUnload)
})

onUnmounted(() => {
  window.removeEventListener('beforeunload', handleBeforeUnload)
})
</script>

<template>
  <div class="min-h-screen bg-gray-50 pb-6">
    <!-- Header -->
    <header class="bg-white border-b px-4 py-4 sticky top-0 z-10">
      <div class="max-w-4xl mx-auto flex items-center justify-between">
        <div>
          <h1 class="font-semibold text-gray-900">{{ quizTitle }}</h1>
          <p class="text-sm text-gray-500">Quiz de validation</p>
        </div>
        <Button
          v-if="!result"
          variant="ghost"
          size="sm"
          @click="confirmExit"
        >
          Quitter
        </Button>
      </div>
    </header>

    <!-- Loading -->
    <div v-if="loading" class="flex justify-center items-center py-20">
      <Spinner class="w-8 h-8" />
    </div>

    <!-- Error -->
    <Alert v-else-if="error && !result" theme="red" class="m-4">
      {{ error }}
      <template #actions>
        <Button size="sm" variant="outline" @click="fetchQuiz">
          Réessayer
        </Button>
      </template>
    </Alert>

    <!-- Not Paid -->
    <Card v-else-if="ec && !ec.is_paid" class="m-4 p-8 text-center">
      <div class="text-5xl mb-4">🔒</div>
      <h2 class="text-xl font-bold text-gray-900 mb-2">Quiz non accessible</h2>
      <p class="text-gray-600 mb-4">
        Vous devez payer cet EC pour passer le quiz.
      </p>
      <Button variant="solid" @click="router.push({ path: '/payment', query: { ec: route.params.id }})">
        Payer maintenant
      </Button>
    </Card>

    <!-- No Quiz -->
    <Card v-else-if="!quiz || questions.length === 0" class="m-4 p-8 text-center">
      <div class="text-5xl mb-4">📝</div>
      <h2 class="text-xl font-bold text-gray-900 mb-2">Quiz non disponible</h2>
      <p class="text-gray-600 mb-4">
        Le quiz pour cet EC n'est pas encore disponible.
      </p>
      <Button variant="outline" @click="goToEC">
        Retour à l'EC
      </Button>
    </Card>

    <!-- Submitting -->
    <div v-else-if="submitting" class="flex flex-col items-center justify-center py-20">
      <Spinner class="w-12 h-12 mb-4" />
      <p class="text-gray-600">Envoi de vos réponses...</p>
    </div>

    <!-- Result -->
    <div v-else-if="result" class="px-4 py-6">
      <div class="max-w-2xl mx-auto">
        <Card class="p-8 text-center">
          <div class="text-6xl mb-4">
            {{ result.passed ? '🎉' : '😔' }}
          </div>

          <h2
            class="text-2xl font-bold mb-2"
            :class="result.passed ? 'text-green-600' : 'text-red-600'"
          >
            {{ result.passed ? 'EC Validé !' : 'Non validé' }}
          </h2>

          <p class="text-gray-600 mb-6">
            {{ result.passed
              ? 'Félicitations ! Vous avez réussi le quiz et validé cet EC.'
              : 'Vous n\'avez pas atteint le score minimum. Révisez le contenu et réessayez.'
            }}
          </p>

          <!-- Score -->
          <div class="bg-gray-50 rounded-xl p-6 mb-6">
            <div
              class="text-5xl font-bold mb-2"
              :class="result.passed ? 'text-green-600' : 'text-red-600'"
            >
              {{ result.percent }}%
            </div>
            <p class="text-gray-600">
              {{ result.score }} / {{ result.total }} bonnes réponses
            </p>
            <p class="text-sm text-gray-500 mt-2">
              Score minimum requis : {{ passingScore }}%
            </p>
          </div>

          <!-- Actions -->
          <div class="flex flex-col sm:flex-row gap-3 justify-center">
            <Button v-if="result.passed" variant="solid" theme="green" @click="goToDashboard">
              Retour au dashboard
            </Button>
            <template v-else>
              <Button variant="outline" @click="goToEC">
                Revoir le contenu
              </Button>
              <Button
                v-if="result.can_retry"
                variant="solid"
                @click="retryQuiz"
              >
                Réessayer le quiz
              </Button>
            </template>
          </div>

          <!-- Retry info -->
          <p v-if="!result.passed && result.attempts_remaining !== null" class="text-sm text-gray-500 mt-4">
            <span v-if="result.attempts_remaining > 0">
              Tentatives restantes : {{ result.attempts_remaining }}
            </span>
            <span v-else>
              Vous avez épuisé vos tentatives. Contactez votre centre pour assistance.
            </span>
          </p>
        </Card>
      </div>
    </div>

    <!-- Quiz Player -->
    <main v-else class="px-4 py-6">
      <div class="max-w-4xl mx-auto">
        <QuizPlayer
          :questions="questions"
          :title="quizTitle"
          :timeLimit="timeLimit"
          :passingScore="passingScore"
          :showFeedback="quiz?.show_immediate_feedback || false"
          @complete="handleQuizComplete"
          @timeout="handleTimeout"
        />
      </div>
    </main>

    <!-- Exit Confirmation Dialog -->
    <Dialog v-model="showExitDialog" :options="{ title: 'Quitter le quiz ?' }">
      <template #body-content>
        <p class="text-gray-600">
          Si vous quittez maintenant, votre progression sera perdue.
          Êtes-vous sûr de vouloir quitter ?
        </p>
      </template>
      <template #actions>
        <Button variant="outline" @click="showExitDialog = false">
          Continuer le quiz
        </Button>
        <Button variant="solid" theme="red" @click="exitQuiz">
          Quitter
        </Button>
      </template>
    </Dialog>
  </div>
</template>
