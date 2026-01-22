<!--
  ChildProgress.vue
  Page de suivi détaillé de la progression d'un enfant.
-->
<script setup>
import { ref, computed, onMounted } from 'vue'
import { Card, Button, Badge, Spinner } from 'frappe-ui'
import {
  ArrowLeft, User, Mail, Phone, MapPin, Calendar,
  BookOpen, CheckCircle, Clock, TrendingUp, CreditCard,
  Award, Target, XCircle
} from 'lucide-vue-next'
import { useGuardian } from '@/composables/useGuardian'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const {
  currentChild,
  childPayments,
  loading,
  error,
  fetchChildProgress,
  fetchChildPayments,
  getProgressColor,
  getProgressBgColor,
  formatAmount,
  getProviderLabel,
} = useGuardian()

const studentId = computed(() => route.params.id)

onMounted(async () => {
  if (studentId.value) {
    await fetchChildProgress(studentId.value)
    await fetchChildPayments(studentId.value)
  }
})

const student = computed(() => currentChild.value?.student || null)
const progress = computed(() => currentChild.value?.progress || null)
const ecs = computed(() => currentChild.value?.ecs || [])
const trend = computed(() => currentChild.value?.trend || [])
const gradesHistory = computed(() => currentChild.value?.grades_history || [])

const goBack = () => {
  router.push('/parent/dashboard')
}

const payForEc = () => {
  router.push(`/parent/pay/${studentId.value}`)
}

const getEcStatusBadge = (status) => {
  switch (status) {
    case 'validated':
      return { label: 'Validé', theme: 'green', icon: CheckCircle }
    case 'in_progress':
      return { label: 'En cours', theme: 'blue', icon: Clock }
    case 'not_started':
      return { label: 'Non payé', theme: 'gray', icon: Target }
    default:
      return { label: status, theme: 'gray', icon: Target }
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
            <p class="text-sm text-gray-500">Suivi de progression</p>
          </div>
          <Button variant="solid" @click="payForEc">
            <CreditCard class="w-4 h-4 mr-2" />
            Payer un EC
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
                <span>Inscrit le {{ formatDate(student.enrolled_since) }}</span>
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

          <!-- Historique notes -->
          <Card v-if="gradesHistory.length > 0" class="p-4">
            <h3 class="font-semibold mb-4 flex items-center gap-2">
              <Award class="w-4 h-4" />
              Dernières notes
            </h3>
            <div class="space-y-2">
              <div
                v-for="grade in gradesHistory"
                :key="grade.ec"
                class="flex items-center justify-between p-2 bg-gray-50 rounded"
              >
                <span class="text-sm">{{ grade.ec }}</span>
                <span class="font-bold" :class="grade.grade >= 10 ? 'text-green-600' : 'text-red-600'">
                  {{ grade.grade }}/20
                </span>
              </div>
            </div>
          </Card>
        </div>

        <!-- Colonne droite: EC + Paiements -->
        <div class="lg:col-span-2 space-y-6">
          <!-- Tendance progression -->
          <Card class="p-4">
            <h3 class="font-semibold mb-4 flex items-center gap-2">
              <TrendingUp class="w-4 h-4" />
              Évolution de la progression
            </h3>
            <div class="flex items-end justify-between h-32 gap-2">
              <div
                v-for="(point, index) in trend"
                :key="index"
                class="flex-1 flex flex-col items-center"
              >
                <div
                  class="w-full rounded-t transition-all"
                  :class="getProgressBgColor(point.progress)"
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
                  <span>{{ formatDate(ec.validated_at) }}</span>
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

                <div v-else class="flex items-center justify-between mt-2">
                  <span class="text-sm text-gray-500">{{ formatAmount(ec.price) }}</span>
                  <Button variant="solid" size="sm" @click="payForEc">
                    Payer
                  </Button>
                </div>
              </div>
            </div>
          </Card>

          <!-- Historique paiements -->
          <Card v-if="childPayments.length > 0" class="p-4">
            <h3 class="font-semibold mb-4 flex items-center gap-2">
              <CreditCard class="w-4 h-4" />
              Historique des paiements
            </h3>
            <div class="space-y-2">
              <div
                v-for="payment in childPayments"
                :key="payment.id"
                class="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
              >
                <div>
                  <div class="font-medium">{{ payment.ec_title }}</div>
                  <div class="text-xs text-gray-500">
                    {{ getProviderLabel(payment.provider) }} - {{ formatDate(payment.paid_at) }}
                  </div>
                </div>
                <div class="text-right">
                  <div class="font-semibold text-green-600">{{ formatAmount(payment.amount) }}</div>
                  <Badge theme="green" size="sm">Payé</Badge>
                </div>
              </div>
            </div>
          </Card>
        </div>
      </div>
    </div>
  </div>
</template>
