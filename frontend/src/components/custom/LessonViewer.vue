<!--
  LessonViewer.vue
  Visualiseur de contenu de leçon (texte, PDF, vidéo).

  Props:
    - content (Object): { type, data, title }
    - lessons (Array): Liste des leçons pour navigation
    - currentIndex (Number): Index leçon actuelle

  Events:
    - @complete: Leçon terminée
    - @navigate(index): Navigation vers autre leçon
    - @progress(percent): Progression dans la leçon

  Example:
    <LessonViewer
      :content="{ type: 'video', data: 'https://youtube.com/...', title: 'Intro' }"
      :lessons="lessonsList"
      :currentIndex="0"
      @complete="handleComplete"
    />
-->
<script setup>
import { ref, computed, watch } from 'vue'
import { Button, Card } from 'frappe-ui'
import VideoPlayer from './VideoPlayer.vue'

const props = defineProps({
  content: {
    type: Object,
    required: true,
    default: () => ({ type: 'text', data: '', title: '' }),
  },
  lessons: {
    type: Array,
    default: () => [],
  },
  currentIndex: {
    type: Number,
    default: 0,
  },
})

const emit = defineEmits(['complete', 'navigate', 'progress'])

const isFullscreen = ref(false)
const lessonProgress = ref(0)

// Computed
const contentType = computed(() => {
  const type = props.content?.type?.toLowerCase() || 'text'

  // Auto-detect from data URL
  if (!type || type === 'auto') {
    const data = props.content?.data || ''
    if (data.includes('youtube.com') || data.includes('youtu.be') || data.includes('vimeo.com')) {
      return 'video'
    }
    if (data.endsWith('.pdf') || data.includes('/pdf/')) {
      return 'pdf'
    }
    if (data.endsWith('.mp4') || data.endsWith('.webm')) {
      return 'video'
    }
    return 'text'
  }

  return type
})

const hasPrevious = computed(() => props.currentIndex > 0)
const hasNext = computed(() => props.currentIndex < props.lessons.length - 1)

const currentLesson = computed(() => {
  if (props.lessons.length > 0) {
    return props.lessons[props.currentIndex]
  }
  return props.content
})

// Methods
const handleVideoEnd = () => {
  lessonProgress.value = 100
  emit('progress', 100)
  emit('complete')
}

const handleVideoProgress = (percent) => {
  lessonProgress.value = percent
  emit('progress', percent)
}

const goToPrevious = () => {
  if (hasPrevious.value) {
    emit('navigate', props.currentIndex - 1)
  }
}

const goToNext = () => {
  if (hasNext.value) {
    emit('navigate', props.currentIndex + 1)
  }
}

const markAsComplete = () => {
  lessonProgress.value = 100
  emit('progress', 100)
  emit('complete')
}

const toggleFullscreen = () => {
  const container = document.querySelector('.lesson-viewer-container')

  if (!document.fullscreenElement) {
    container?.requestFullscreen?.()
    isFullscreen.value = true
  } else {
    document.exitFullscreen?.()
    isFullscreen.value = false
  }
}

// Reset progress when content changes
watch(
  () => props.content,
  () => {
    lessonProgress.value = 0
  }
)
</script>

<template>
  <div class="lesson-viewer-container">
    <!-- Header with navigation -->
    <div class="flex items-center justify-between mb-4 px-1">
      <div>
        <h2 class="font-semibold text-gray-900">
          {{ content?.title || 'Leçon' }}
        </h2>
        <p v-if="lessons.length > 1" class="text-sm text-gray-500">
          {{ currentIndex + 1 }} / {{ lessons.length }}
        </p>
      </div>

      <div class="flex items-center gap-2">
        <Button
          variant="ghost"
          size="sm"
          @click="toggleFullscreen"
          title="Plein écran"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              v-if="!isFullscreen"
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4"
            />
            <path
              v-else
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M9 9V4.5M9 9H4.5M9 9L3.75 3.75M9 15v4.5M9 15H4.5M9 15l-5.25 5.25M15 9h4.5M15 9V4.5M15 9l5.25-5.25M15 15h4.5M15 15v4.5m0-4.5l5.25 5.25"
            />
          </svg>
        </Button>
      </div>
    </div>

    <!-- Content -->
    <Card class="overflow-hidden">
      <!-- Video Content -->
      <template v-if="contentType === 'video'">
        <VideoPlayer
          :src="content.data"
          :title="content.title"
          @ended="handleVideoEnd"
          @progress="handleVideoProgress"
        />
      </template>

      <!-- PDF Content -->
      <template v-else-if="contentType === 'pdf'">
        <div class="aspect-[4/3] md:aspect-video">
          <iframe
            :src="content.data"
            :title="content.title"
            class="w-full h-full border-0"
          />
        </div>
        <div class="p-4 bg-gray-50 border-t flex justify-between items-center">
          <span class="text-sm text-gray-600">
            Document PDF
          </span>
          <a
            :href="content.data"
            target="_blank"
            class="text-sm text-cntemad-primary hover:underline"
          >
            Ouvrir dans un nouvel onglet
          </a>
        </div>
      </template>

      <!-- Image Content -->
      <template v-else-if="contentType === 'image'">
        <div class="p-4">
          <img
            :src="content.data"
            :alt="content.title"
            class="max-w-full h-auto mx-auto rounded-lg"
          />
        </div>
      </template>

      <!-- Text/HTML/Markdown Content -->
      <template v-else>
        <div class="p-6 prose prose-sm md:prose max-w-none">
          <!-- If HTML content -->
          <div v-if="content.data?.includes('<')" v-html="content.data" />
          <!-- Plain text -->
          <div v-else class="whitespace-pre-wrap">{{ content.data }}</div>
        </div>
      </template>
    </Card>

    <!-- Progress & Navigation -->
    <div class="mt-4">
      <!-- Progress Bar -->
      <div v-if="contentType === 'video'" class="mb-4">
        <div class="flex justify-between text-sm text-gray-600 mb-1">
          <span>Progression</span>
          <span>{{ Math.round(lessonProgress) }}%</span>
        </div>
        <div class="h-2 bg-gray-200 rounded-full overflow-hidden">
          <div
            class="h-full bg-cntemad-primary transition-all"
            :style="{ width: `${lessonProgress}%` }"
          />
        </div>
      </div>

      <!-- Navigation Buttons -->
      <div class="flex items-center justify-between gap-3">
        <Button
          variant="outline"
          :disabled="!hasPrevious"
          @click="goToPrevious"
        >
          <span class="mr-1">←</span>
          Précédent
        </Button>

        <!-- Mark Complete (for text/pdf content) -->
        <Button
          v-if="contentType !== 'video' && lessonProgress < 100"
          variant="solid"
          theme="green"
          @click="markAsComplete"
        >
          Marquer comme lu
        </Button>

        <Button
          v-if="hasNext"
          variant="solid"
          @click="goToNext"
        >
          Suivant
          <span class="ml-1">→</span>
        </Button>
        <Button
          v-else-if="lessonProgress >= 100"
          variant="solid"
          theme="green"
          @click="emit('complete')"
        >
          Terminer
        </Button>
      </div>
    </div>

    <!-- Lesson List (if multiple) -->
    <div v-if="lessons.length > 1" class="mt-6">
      <h3 class="font-medium text-gray-900 mb-3">Contenu</h3>
      <div class="space-y-2">
        <button
          v-for="(lesson, index) in lessons"
          :key="index"
          class="w-full flex items-center gap-3 p-3 rounded-lg text-left transition-colors"
          :class="[
            index === currentIndex
              ? 'bg-cntemad-primary/10 text-cntemad-primary'
              : 'bg-gray-50 hover:bg-gray-100 text-gray-700'
          ]"
          @click="emit('navigate', index)"
        >
          <span
            class="w-6 h-6 rounded-full flex items-center justify-center text-xs font-medium"
            :class="[
              index === currentIndex
                ? 'bg-cntemad-primary text-white'
                : 'bg-gray-200 text-gray-600'
            ]"
          >
            {{ index + 1 }}
          </span>
          <span class="flex-1 truncate">{{ lesson.title || `Leçon ${index + 1}` }}</span>
          <span v-if="lesson.completed" class="text-green-500">✓</span>
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.lesson-viewer-container:fullscreen {
  background: white;
  padding: 1rem;
  overflow-y: auto;
}

.prose :deep(img) {
  max-width: 100%;
  height: auto;
  border-radius: 0.5rem;
}

.prose :deep(pre) {
  background: #1e1e1e;
  color: #d4d4d4;
  padding: 1rem;
  border-radius: 0.5rem;
  overflow-x: auto;
}

.prose :deep(code) {
  background: #f3f4f6;
  padding: 0.125rem 0.25rem;
  border-radius: 0.25rem;
  font-size: 0.875em;
}

.prose :deep(pre code) {
  background: transparent;
  padding: 0;
}
</style>
