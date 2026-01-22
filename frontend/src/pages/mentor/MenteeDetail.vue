<!--
  MenteeDetail.vue
  Vue progression détaillée d'un mentoré.
-->
<script setup>
import { ref, computed, onMounted } from 'vue'
import { Card, Button, Badge, Spinner } from 'frappe-ui'
import {
  ArrowLeft, User, Mail, Phone, MapPin, Calendar,
  BookOpen, CheckCircle, Clock, TrendingUp, MessageSquare,
  Award, Target, Activity
} from 'lucide-vue-next'
import { useMentor } from '@/composables/useMentor'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const {
  currentMentee,
  loading,
  error,
  fetchMenteeDetail,
  fetchMenteeStats,
  getProgressColor,
} = useMentor()

const menteeStats = ref(null)
const studentId = computed(() => route.params.id)

onMounted(async () => {
  if (studentId.value) {
    await fetchMenteeDetail(studentId.value)
    menteeStats.value = await fetchMenteeStats(studentId.value)
  }
})

const student = computed(() => currentMentee.value?.student || null)
const progress = computed(() => currentMentee.value?.progress || null)
const ecs = computed(() => currentMentee.value?.ecs || [])
const activity = computed(() => currentMentee.value?.activity || [])
const progressTrend = computed(() => currentMentee.value?.progress_trend || [])

const goBack = () => {
  router.push('/mentor/mentees')
}

const openMessages = () => {
  router.push(`/mentor/messages/${studentId.value}`)
}

const getEcStatusBadge = (status) => {
  switch (status) {
    case 'validated':
      return { label: 'Validé', theme: 'green' }
    case 'in_progress':
      return { label: 'En cours', theme: 'blue' }
    case 'not_started':
      return { label: 'Non commencé', theme: 'gray' }
    default:
      return { label: status, theme: 'gray' }
  }
}

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleDateString('fr-FR', {
    day: '2-digit',
    month: 'long',
    year: 'numeric',
  })
}
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="bg-white border-b sticky top-0 z-10">
      <div class="max-w-7xl mx-auto px-4 py-4">
        <div class="flex items-center gap-4">
          <Button variant="ghost" @click="goBack">
            <ArrowLeft class="w-5 h-5" />
          </Button>
          <div class="flex-1">
            <h1 class="text-lg font-bold text-gray-900">{{ student?.name || 'Chargement...' }}</h1>
            <p class="text-sm text-gray-500">{{ student?.id }}</p>
          </div>
          <Button variant="solid" @click="openMessages">
            <MessageSquare class="w-4 h-4 mr-2" />
            Message
          </Button>
        </div>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="flex justify-center py-12">
      <Spinner class="w-8 h-8" />
    </div>

    <!-- Error -->
    <div v-else-if="error" class="max-w-7xl mx-auto px-4 py-6">
      <div class="bg-red-50 text-red-700 p-4 rounded-lg">{{ error }}</div>
    </div>

    <!-- Content -->
    <div v-else-if="student" class="max-w-7xl mx-auto px-4 py-6">
      <div class="grid lg:grid-cols-3 gap-6">
        <!-- Colonne gauche: Profil + Stats -->
        <div class="space-y-6">
          <!-- Profil -->
          <Card class="p-4">
            <div class="text-center mb-4">
              <div class="w-20 h-20 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-3">
                <User class="w-10 h-10 text-blue-600" />
              </div>
              <h2 class="text-xl font-bold text-gray-900">{{ student.name }}</h2>
              <Badge theme="blue">{{ student.year }}</Badge>
            </div>

            <div class="space-y-3 text-sm">
              <div class="flex items-center gap-3">
                <Mail class="w-4 h-4 text-gray-400" />
                <span>{{ student.email }}</span>
              </div>
              <div class="flex items-center gap-3">
                <Phone class="w-4 h-4 text-gray-400" />
                <span>{{ student.phone }}</span>
              </div>
              <div class="flex items-center gap-3">
                <MapPin class="w-4 h-4 text-gray-400" />
                <span>{{ student.center }}</span>
              </div>
              <div class="flex items-center gap-3">
                <Calendar class="w-4 h-4 text-gray-400" />
                <span>Inscrit depuis {{ formatDate(student.enrolled_since) }}</span>
              </div>
            </div>
          </Card>

          <!-- Progression globale -->
          <Card class="p-4">
            <h3 class="font-semibold mb-4">Progression globale</h3>
            <div class="text-center mb-4">
              <div class="text-4xl font-bold" :class="getProgressColor(progress?.overall || 0)">
                {{ progress?.overall || 0 }}%
              </div>
              <div class="text-sm text-gray-500">de l'année complétée</div>
            </div>

            <div class="space-y-3">
              <div class="flex justify-between text-sm">
                <span class="text-gray-600">EC validés</span>
                <span class="font-semibold">{{ progress?.validated_ecs }}/{{ progress?.total_ecs }}</span>
              </div>
              <div class="flex justify-between text-sm">
                <span class="text-gray-600">Moyenne générale</span>
                <span class="font-semibold" :class="(progress?.average || 0) >= 10 ? 'text-green-600' : 'text-red-600'">
                  {{ progress?.average?.toFixed(2) || '-' }}/20
                </span>
              </div>
              <div class="flex justify-between text-sm">
                <span class="text-gray-600">Classement</span>
                <span class="font-semibold">{{ progress?.rank }}/{{ progress?.total_students }}</span>
              </div>
            </div>
          </Card>

          <!-- Stats engagement -->
          <Card v-if="menteeStats" class="p-4">
            <h3 class="font-semibold mb-4 flex items-center gap-2">
              <Activity class="w-4 h-4" />
              Engagement
            </h3>
            <div class="space-y-3 text-sm">
              <div class="flex justify-between">
                <span class="text-gray-600">Connexions (7j)</span>
                <span class="font-semibold">{{ menteeStats.login_frequency?.last_7_days }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600">Session moyenne</span>
                <span class="font-semibold">{{ menteeStats.login_frequency?.average_session }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600">Quiz réussis</span>
                <span class="font-semibold text-green-600">
                  {{ menteeStats.quiz_performance?.passed }}/{{ menteeStats.quiz_performance?.total_attempts }}
                </span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600">Score engagement</span>
                <span class="font-bold text-blue-600">{{ menteeStats.engagement_score }}%</span>
              </div>
            </div>
          </Card>
        </div>

        <!-- Colonne droite: EC + Activité -->
        <div class="lg:col-span-2 space-y-6">
          <!-- Tendance progression -->
          <Card class="p-4">
            <h3 class="font-semibold mb-4 flex items-center gap-2">
              <TrendingUp class="w-4 h-4" />
              Évolution de la progression
            </h3>
            <div class="flex items-end justify-between h-32 gap-2">
              <div
                v-for="(point, index) in progressTrend"
                :key="index"
                class="flex-1 flex flex-col items-center"
              >
                <div
                  class="w-full bg-blue-500 rounded-t transition-all"
                  :style="{ height: `${point.progress}%` }"
                ></div>
                <span class="text-xs text-gray-500 mt-2">{{ point.month }}</span>
              </div>
            </div>
          </Card>

          <!-- Liste des EC -->
          <Card class="p-4">
            <h3 class="font-semibold mb-4 flex items-center gap-2">
              <BookOpen class="w-4 h-4" />
              Éléments constitutifs ({{ ecs.length }})
            </h3>
            <div class="space-y-3">
              <div
                v-for="ec in ecs"
                :key="ec.id"
                class="p-3 border rounded-lg"
              >
                <div class="flex items-center justify-between mb-2">
                  <span class="font-medium">{{ ec.title }}</span>
                  <Badge :theme="getEcStatusBadge(ec.status).theme" size="sm">
                    {{ getEcStatusBadge(ec.status).label }}
                  </Badge>
                </div>

                <div v-if="ec.status === 'validated'" class="flex items-center gap-4 text-sm text-gray-600">
                  <span class="flex items-center gap-1">
                    <Award class="w-4 h-4 text-green-500" />
                    Note: {{ ec.grade }}/20
                  </span>
                  <span>Validé le {{ formatDate(ec.validated_at) }}</span>
                </div>

                <div v-else-if="ec.status === 'in_progress'" class="mt-2">
                  <div class="flex justify-between text-xs mb-1">
                    <span>Progression</span>
                    <span>{{ ec.progress }}%</span>
                  </div>
                  <div class="w-full h-1.5 bg-gray-200 rounded-full">
                    <div
                      class="h-full bg-blue-500 rounded-full"
                      :style="{ width: `${ec.progress}%` }"
                    ></div>
                  </div>
                </div>

                <div v-else class="text-sm text-gray-500">
                  <Target class="w-4 h-4 inline mr-1" />
                  Non commencé
                </div>
              </div>
            </div>
          </Card>

          <!-- Historique activité -->
          <Card class="p-4">
            <h3 class="font-semibold mb-4 flex items-center gap-2">
              <Clock class="w-4 h-4" />
              Activité récente
            </h3>
            <div class="space-y-3">
              <div
                v-for="(item, index) in activity"
                :key="index"
                class="flex items-start gap-3 pb-3 border-b last:border-0"
              >
                <div
                  class="w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0"
                  :class="{
                    'bg-green-100': item.type === 'quiz',
                    'bg-blue-100': item.type === 'lesson',
                    'bg-purple-100': item.type === 'payment',
                    'bg-gray-100': item.type === 'login',
                  }"
                >
                  <CheckCircle v-if="item.type === 'quiz'" class="w-4 h-4 text-green-600" />
                  <BookOpen v-else-if="item.type === 'lesson'" class="w-4 h-4 text-blue-600" />
                  <Award v-else-if="item.type === 'payment'" class="w-4 h-4 text-purple-600" />
                  <User v-else class="w-4 h-4 text-gray-600" />
                </div>
                <div class="flex-1">
                  <div class="text-sm">{{ item.description }}</div>
                  <div class="text-xs text-gray-500">{{ item.date }}</div>
                </div>
              </div>
            </div>
          </Card>
        </div>
      </div>
    </div>
  </div>
</template>
