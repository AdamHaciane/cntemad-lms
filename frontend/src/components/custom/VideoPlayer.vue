<!--
  VideoPlayer.vue
  Lecteur vidéo pour YouTube et fichiers vidéo locaux.

  Props:
    - src (String): URL YouTube ou chemin fichier vidéo
    - title (String): Titre de la vidéo
    - autoplay (Boolean): Lecture automatique

  Events:
    - @ended: Vidéo terminée
    - @progress(percent): Progression de lecture

  Example:
    <VideoPlayer
      src="https://www.youtube.com/watch?v=abc123"
      title="Introduction au cours"
      @ended="handleVideoEnd"
    />
-->
<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  src: {
    type: String,
    required: true,
  },
  title: {
    type: String,
    default: '',
  },
  autoplay: {
    type: Boolean,
    default: false,
  },
  poster: {
    type: String,
    default: '',
  },
})

const emit = defineEmits(['ended', 'progress', 'play', 'pause'])

const videoRef = ref(null)
const isPlaying = ref(false)
const currentTime = ref(0)
const duration = ref(0)
const isFullscreen = ref(false)

// Detect video type
const videoType = computed(() => {
  const url = props.src.toLowerCase()
  if (url.includes('youtube.com') || url.includes('youtu.be')) {
    return 'youtube'
  }
  if (url.includes('vimeo.com')) {
    return 'vimeo'
  }
  return 'native'
})

// Extract YouTube video ID
const youtubeId = computed(() => {
  if (videoType.value !== 'youtube') return null

  const url = props.src
  // Handle various YouTube URL formats
  const patterns = [
    /(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\s?]+)/,
    /youtube\.com\/v\/([^&\s?]+)/,
  ]

  for (const pattern of patterns) {
    const match = url.match(pattern)
    if (match) return match[1]
  }
  return null
})

// YouTube embed URL
const youtubeEmbedUrl = computed(() => {
  if (!youtubeId.value) return ''
  const params = new URLSearchParams({
    rel: '0',
    modestbranding: '1',
    autoplay: props.autoplay ? '1' : '0',
  })
  return `https://www.youtube.com/embed/${youtubeId.value}?${params}`
})

// Progress percentage
const progressPercent = computed(() => {
  if (duration.value === 0) return 0
  return (currentTime.value / duration.value) * 100
})

// Native video handlers
const handleTimeUpdate = () => {
  if (videoRef.value) {
    currentTime.value = videoRef.value.currentTime
    duration.value = videoRef.value.duration
    emit('progress', progressPercent.value)
  }
}

const handleEnded = () => {
  isPlaying.value = false
  emit('ended')
}

const handlePlay = () => {
  isPlaying.value = true
  emit('play')
}

const handlePause = () => {
  isPlaying.value = false
  emit('pause')
}

const togglePlay = () => {
  if (videoRef.value) {
    if (isPlaying.value) {
      videoRef.value.pause()
    } else {
      videoRef.value.play()
    }
  }
}

const toggleFullscreen = () => {
  const container = videoRef.value?.parentElement

  if (!document.fullscreenElement) {
    container?.requestFullscreen?.()
    isFullscreen.value = true
  } else {
    document.exitFullscreen?.()
    isFullscreen.value = false
  }
}

const formatTime = (seconds) => {
  const mins = Math.floor(seconds / 60)
  const secs = Math.floor(seconds % 60)
  return `${mins}:${secs.toString().padStart(2, '0')}`
}

// Handle fullscreen change
const handleFullscreenChange = () => {
  isFullscreen.value = !!document.fullscreenElement
}

onMounted(() => {
  document.addEventListener('fullscreenchange', handleFullscreenChange)
})

onUnmounted(() => {
  document.removeEventListener('fullscreenchange', handleFullscreenChange)
})
</script>

<template>
  <div class="video-player rounded-lg overflow-hidden bg-black">
    <!-- YouTube Embed -->
    <template v-if="videoType === 'youtube'">
      <div class="relative aspect-video">
        <iframe
          :src="youtubeEmbedUrl"
          :title="title"
          class="absolute inset-0 w-full h-full"
          frameborder="0"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
          allowfullscreen
        />
      </div>
    </template>

    <!-- Native Video -->
    <template v-else>
      <div class="relative aspect-video group">
        <video
          ref="videoRef"
          :src="src"
          :poster="poster"
          :autoplay="autoplay"
          class="w-full h-full object-contain"
          @timeupdate="handleTimeUpdate"
          @ended="handleEnded"
          @play="handlePlay"
          @pause="handlePause"
        />

        <!-- Controls Overlay -->
        <div
          class="absolute inset-0 flex items-center justify-center bg-black/30 opacity-0 group-hover:opacity-100 transition-opacity"
        >
          <!-- Play/Pause Button -->
          <button
            class="w-16 h-16 rounded-full bg-white/90 flex items-center justify-center hover:bg-white transition-colors"
            @click="togglePlay"
          >
            <svg
              v-if="!isPlaying"
              class="w-8 h-8 text-gray-900 ml-1"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path d="M6.3 2.841A1.5 1.5 0 004 4.11V15.89a1.5 1.5 0 002.3 1.269l9.344-5.89a1.5 1.5 0 000-2.538L6.3 2.84z" />
            </svg>
            <svg
              v-else
              class="w-8 h-8 text-gray-900"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path d="M5.75 3a.75.75 0 00-.75.75v12.5c0 .414.336.75.75.75h1.5a.75.75 0 00.75-.75V3.75A.75.75 0 007.25 3h-1.5zM12.75 3a.75.75 0 00-.75.75v12.5c0 .414.336.75.75.75h1.5a.75.75 0 00.75-.75V3.75a.75.75 0 00-.75-.75h-1.5z" />
            </svg>
          </button>
        </div>

        <!-- Bottom Controls -->
        <div
          class="absolute bottom-0 left-0 right-0 p-3 bg-gradient-to-t from-black/70 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"
        >
          <!-- Progress Bar -->
          <div class="mb-2">
            <div class="h-1 bg-white/30 rounded-full overflow-hidden">
              <div
                class="h-full bg-cntemad-primary transition-all"
                :style="{ width: `${progressPercent}%` }"
              />
            </div>
          </div>

          <div class="flex items-center justify-between text-white text-sm">
            <span>{{ formatTime(currentTime) }} / {{ formatTime(duration) }}</span>

            <button
              class="p-1 hover:bg-white/20 rounded"
              @click="toggleFullscreen"
            >
              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path
                  v-if="!isFullscreen"
                  d="M4.75 5.75a1 1 0 00-1 1v2.5a.75.75 0 01-1.5 0v-2.5A2.5 2.5 0 014.75 4.25h2.5a.75.75 0 010 1.5h-2.5zM17.25 9.25a.75.75 0 01-.75-.75v-2.5a1 1 0 00-1-1h-2.5a.75.75 0 010-1.5h2.5a2.5 2.5 0 012.5 2.5v2.5a.75.75 0 01-.75.75zM4.75 14.25a1 1 0 001 1h2.5a.75.75 0 010 1.5h-2.5a2.5 2.5 0 01-2.5-2.5v-2.5a.75.75 0 011.5 0v2.5zM15.5 14.25a1 1 0 01-1 1h-2.5a.75.75 0 000 1.5h2.5a2.5 2.5 0 002.5-2.5v-2.5a.75.75 0 00-1.5 0v2.5z"
                />
                <path
                  v-else
                  d="M3.28 2.22a.75.75 0 00-1.06 1.06L5.94 7H4.75a.75.75 0 000 1.5h3.5a.75.75 0 00.75-.75v-3.5a.75.75 0 00-1.5 0v1.19L3.28 2.22zM16.72 2.22a.75.75 0 111.06 1.06L14.06 7h1.19a.75.75 0 010 1.5h-3.5a.75.75 0 01-.75-.75v-3.5a.75.75 0 011.5 0v1.19l3.72-3.72zM3.28 17.78a.75.75 0 01-1.06-1.06L5.94 13H4.75a.75.75 0 010-1.5h3.5a.75.75 0 01.75.75v3.5a.75.75 0 01-1.5 0v-1.19l-3.72 3.72zM16.72 17.78a.75.75 0 001.06-1.06L14.06 13h1.19a.75.75 0 000-1.5h-3.5a.75.75 0 00-.75.75v3.5a.75.75 0 001.5 0v-1.19l3.72 3.72z"
                />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </template>

    <!-- Title -->
    <div v-if="title" class="p-3 bg-gray-900 text-white text-sm">
      {{ title }}
    </div>
  </div>
</template>

<style scoped>
.video-player {
  contain: layout;
}
</style>
