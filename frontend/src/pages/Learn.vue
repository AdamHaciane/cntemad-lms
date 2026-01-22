<!--
  Learn.vue
  Page d'apprentissage d'un EC avec contenu multimédia.

  Route: /ec/:id/learn
-->
<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Card, Button, Spinner, Alert, Badge } from 'frappe-ui'
import { createResource } from 'frappe-ui'
import LessonViewer from '@/components/custom/LessonViewer.vue'
import ProgressBar from '@/components/custom/ProgressBar.vue'

const route = useRoute()
const router = useRouter()

// State
const ec = ref(null)
const lessons = ref([])
const currentLessonIndex = ref(0)
const completedLessons = ref(new Set())
const loading = ref(true)
const error = ref(null)

// Resources
const ecResource = createResource({
  url: 'cntemad_lms.api.ec.get_ec_content',
  auto: false,
  onSuccess(data) {
    ec.value = data.ec
    lessons.value = data.lessons || []

    // Initialize completed lessons from server data
    if (data.progress?.completed_lessons) {
      completedLessons.value = new Set(data.progress.completed_lessons)
    }
  },
  onError(err) {
    error.value = err.message || 'Erreur de chargement du contenu'
  },
})

const progressResource = createResource({
  url: 'cntemad_lms.api.ec.update_lesson_progress',
  auto: false,
})

// Computed
const currentLesson = computed(() => {
  if (lessons.value.length === 0) return null
  return lessons.value[currentLessonIndex.value]
})

const lessonContent = computed(() => {
  if (!currentLesson.value) return { type: 'text', data: '', title: '' }

  return {
    type: currentLesson.value.content_type || 'text',
    data: currentLesson.value.content || currentLesson.value.video_url || '',
    title: currentLesson.value.title || `Leçon ${currentLessonIndex.value + 1}`,
  }
})

const enrichedLessons = computed(() => {
  return lessons.value.map((lesson, index) => ({
    ...lesson,
    completed: completedLessons.value.has(lesson.name || index),
  }))
})

const progressPercent = computed(() => {
  if (lessons.value.length === 0) return 0
  return (completedLessons.value.size / lessons.value.length) * 100
})

const allLessonsCompleted = computed(() => {
  return lessons.value.length > 0 && completedLessons.value.size === lessons.value.length
})

const canAccessQuiz = computed(() => {
  return allLessonsCompleted.value && ec.value?.quiz_id
})

// Methods
const fetchContent = async () => {
  loading.value = true
  error.value = null

  try {
    await ecResource.fetch({ ec_id: route.params.id })
  } finally {
    loading.value = false
  }
}

const handleLessonComplete = () => {
  const lesson = currentLesson.value
  if (!lesson) return

  const lessonId = lesson.name || currentLessonIndex.value
  completedLessons.value.add(lessonId)

  // Save progress to server
  saveProgress(lessonId)

  // Auto-advance to next lesson
  if (currentLessonIndex.value < lessons.value.length - 1) {
    setTimeout(() => {
      currentLessonIndex.value++
    }, 500)
  }
}

const handleNavigate = (index) => {
  currentLessonIndex.value = index
}

const handleLessonProgress = (percent) => {
  // Track video progress if needed
  if (percent >= 90) {
    handleLessonComplete()
  }
}

const saveProgress = async (lessonId) => {
  try {
    await progressResource.fetch({
      ec_id: route.params.id,
      lesson_id: lessonId,
      completed: true,
    })
  } catch (e) {
    console.error('Error saving progress:', e)
  }
}

const goToQuiz = () => {
  router.push(`/ec/${route.params.id}/quiz`)
}

const goToEC = () => {
  router.push(`/ec/${route.params.id}`)
}

// Lifecycle
onMounted(() => {
  fetchContent()
})

// Watch for route changes
watch(
  () => route.params.id,
  () => {
    fetchContent()
  }
)
</script>

<template>
  <div class="min-h-screen bg-gray-50 pb-20 md:pb-6">
    <!-- Header -->
    <header class="bg-white border-b px-4 py-4 sticky top-0 z-10">
      <div class="max-w-4xl mx-auto">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-3">
            <Button variant="ghost" size="sm" @click="goToEC">
              ← Retour
            </Button>
            <div>
              <h1 class="font-semibold text-gray-900 truncate">
                {{ ec?.title || 'Chargement...' }}
              </h1>
              <p class="text-sm text-gray-500">
                {{ lessons.length }} leçon{{ lessons.length > 1 ? 's' : '' }}
              </p>
            </div>
          </div>

          <Badge v-if="allLessonsCompleted" theme="green">
            Terminé
          </Badge>
        </div>

        <!-- Progress -->
        <div class="mt-3">
          <ProgressBar
            :value="completedLessons.size"
            :max="lessons.length"
            size="sm"
            :showPercent="false"
          />
          <p class="text-xs text-gray-500 mt-1">
            {{ completedLessons.size }} / {{ lessons.length }} leçons complétées
          </p>
        </div>
      </div>
    </header>

    <!-- Loading -->
    <div v-if="loading" class="flex justify-center items-center py-20">
      <Spinner class="w-8 h-8" />
    </div>

    <!-- Error -->
    <Alert v-else-if="error" theme="red" class="m-4">
      {{ error }}
    </Alert>

    <!-- Not Paid -->
    <Card v-else-if="ec && !ec.is_paid" class="m-4 p-8 text-center">
      <div class="text-5xl mb-4">🔒</div>
      <h2 class="text-xl font-bold text-gray-900 mb-2">Contenu verrouillé</h2>
      <p class="text-gray-600 mb-4">
        Vous devez payer cet EC pour accéder au contenu.
      </p>
      <Button variant="solid" @click="router.push({ path: '/payment', query: { ec: route.params.id }})">
        Payer maintenant
      </Button>
    </Card>

    <!-- No Content -->
    <Card v-else-if="lessons.length === 0" class="m-4 p-8 text-center">
      <div class="text-5xl mb-4">📭</div>
      <h2 class="text-xl font-bold text-gray-900 mb-2">Pas de contenu</h2>
      <p class="text-gray-600">
        Le contenu de cet EC n'est pas encore disponible.
      </p>
    </Card>

    <!-- Content -->
    <main v-else class="px-4 py-6">
      <div class="max-w-4xl mx-auto">
        <!-- Lesson Viewer -->
        <LessonViewer
          :content="lessonContent"
          :lessons="enrichedLessons"
          :currentIndex="currentLessonIndex"
          @complete="handleLessonComplete"
          @navigate="handleNavigate"
          @progress="handleLessonProgress"
        />

        <!-- Quiz CTA -->
        <Card v-if="allLessonsCompleted" class="mt-6 p-6">
          <div class="flex flex-col sm:flex-row items-center gap-4">
            <div class="text-4xl">🎯</div>
            <div class="flex-1 text-center sm:text-left">
              <h3 class="font-semibold text-gray-900">
                Prêt pour le quiz ?
              </h3>
              <p class="text-sm text-gray-600">
                Vous avez terminé toutes les leçons. Passez le quiz pour valider cet EC.
              </p>
            </div>
            <Button
              v-if="canAccessQuiz"
              variant="solid"
              theme="green"
              @click="goToQuiz"
            >
              Passer le quiz
            </Button>
            <p v-else class="text-sm text-gray-500">
              Quiz non disponible
            </p>
          </div>
        </Card>
      </div>
    </main>

    <!-- Bottom Navigation (Mobile) -->
    <nav class="fixed bottom-0 left-0 right-0 bg-white border-t md:hidden safe-area-bottom">
      <div class="flex justify-around py-2">
        <button
          class="flex flex-col items-center p-2 text-gray-500"
          @click="router.push('/dashboard')"
        >
          <span class="text-xl">🏠</span>
          <span class="text-xs">Accueil</span>
        </button>
        <button
          class="flex flex-col items-center p-2 text-cntemad-primary"
          @click="goToEC"
        >
          <span class="text-xl">📚</span>
          <span class="text-xs font-medium">EC</span>
        </button>
        <button
          class="flex flex-col items-center p-2 text-gray-500"
          @click="router.push('/catalog')"
        >
          <span class="text-xl">🛒</span>
          <span class="text-xs">Catalogue</span>
        </button>
        <button
          class="flex flex-col items-center p-2 text-gray-500"
          @click="router.push('/profile')"
        >
          <span class="text-xl">👤</span>
          <span class="text-xs">Profil</span>
        </button>
      </div>
    </nav>
  </div>
</template>

<style scoped>
.safe-area-bottom {
  padding-bottom: env(safe-area-inset-bottom);
}
</style>
