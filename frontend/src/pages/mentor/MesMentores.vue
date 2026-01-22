<!--
  MesMentores.vue
  Page principale du mentor affichant la liste des mentorés avec stats.
-->
<script setup>
import { ref, computed, onMounted } from 'vue'
import { Card, Button, Badge, Input, Spinner } from 'frappe-ui'
import {
  Users, Search, Filter, UserCheck, UserX, MessageSquare,
  TrendingUp, AlertTriangle, ChevronRight, RefreshCw
} from 'lucide-vue-next'
import { useMentor } from '@/composables/useMentor'
import { useRouter } from 'vue-router'

const router = useRouter()
const {
  dashboard,
  mentees,
  alerts,
  loading,
  stats,
  mentor,
  recentActivity,
  activeMentees,
  inactiveMentees,
  activeAlerts,
  fetchDashboard,
  fetchMentees,
  getStatusColor,
  getProgressColor,
  getAlertSeverityColor,
} = useMentor()

const searchQuery = ref('')
const statusFilter = ref('all')
const yearFilter = ref('')

onMounted(async () => {
  await fetchDashboard()
})

const filteredMentees = computed(() => {
  let result = mentees.value

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(m =>
      m.name?.toLowerCase().includes(query) ||
      m.id?.toLowerCase().includes(query) ||
      m.email?.toLowerCase().includes(query)
    )
  }

  if (statusFilter.value !== 'all') {
    result = result.filter(m => m.status === statusFilter.value)
  }

  if (yearFilter.value) {
    result = result.filter(m => m.year === yearFilter.value)
  }

  return result
})

const uniqueYears = computed(() => {
  const years = new Set(mentees.value.map(m => m.year))
  return Array.from(years).sort()
})

const openMenteeDetail = (mentee) => {
  router.push(`/mentor/mentee/${mentee.id}`)
}

const openMessages = (mentee) => {
  router.push(`/mentor/messages/${mentee.id}`)
}

const refreshData = async () => {
  await fetchDashboard()
}

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleDateString('fr-FR', { day: '2-digit', month: 'short' })
}
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="bg-white border-b sticky top-0 z-10">
      <div class="max-w-7xl mx-auto px-4 py-4">
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h1 class="text-xl font-bold text-gray-900">Mes mentorés</h1>
            <p class="text-sm text-gray-500" v-if="mentor">
              {{ mentor.full_name }} - {{ mentor.specialty }}
            </p>
          </div>
          <div class="flex items-center gap-2">
            <Badge theme="blue">{{ mentees.length }} mentorés</Badge>
            <Button variant="subtle" size="sm" @click="refreshData" :loading="loading">
              <RefreshCw class="w-4 h-4" />
            </Button>
          </div>
        </div>
      </div>
    </div>

    <div class="max-w-7xl mx-auto px-4 py-6">
      <!-- Stats -->
      <div class="grid grid-cols-2 md:grid-cols-5 gap-4 mb-6">
        <Card class="p-4">
          <div class="flex items-center gap-3">
            <div class="p-2 bg-blue-100 rounded-lg">
              <Users class="w-5 h-5 text-blue-600" />
            </div>
            <div>
              <div class="text-2xl font-bold">{{ stats?.total_mentees || 0 }}</div>
              <div class="text-xs text-gray-500">Total</div>
            </div>
          </div>
        </Card>
        <Card class="p-4">
          <div class="flex items-center gap-3">
            <div class="p-2 bg-green-100 rounded-lg">
              <UserCheck class="w-5 h-5 text-green-600" />
            </div>
            <div>
              <div class="text-2xl font-bold text-green-600">{{ activeMentees.length }}</div>
              <div class="text-xs text-gray-500">Actifs</div>
            </div>
          </div>
        </Card>
        <Card class="p-4">
          <div class="flex items-center gap-3">
            <div class="p-2 bg-red-100 rounded-lg">
              <UserX class="w-5 h-5 text-red-600" />
            </div>
            <div>
              <div class="text-2xl font-bold text-red-600">{{ inactiveMentees.length }}</div>
              <div class="text-xs text-gray-500">Inactifs</div>
            </div>
          </div>
        </Card>
        <Card class="p-4">
          <div class="flex items-center gap-3">
            <div class="p-2 bg-purple-100 rounded-lg">
              <MessageSquare class="w-5 h-5 text-purple-600" />
            </div>
            <div>
              <div class="text-2xl font-bold text-purple-600">{{ stats?.messages_unread || 0 }}</div>
              <div class="text-xs text-gray-500">Messages</div>
            </div>
          </div>
        </Card>
        <Card class="p-4">
          <div class="flex items-center gap-3">
            <div class="p-2 bg-yellow-100 rounded-lg">
              <TrendingUp class="w-5 h-5 text-yellow-600" />
            </div>
            <div>
              <div class="text-2xl font-bold">{{ stats?.avg_progress?.toFixed(0) || 0 }}%</div>
              <div class="text-xs text-gray-500">Moy. progression</div>
            </div>
          </div>
        </Card>
      </div>

      <!-- Alertes -->
      <div v-if="activeAlerts.length > 0" class="mb-6">
        <h2 class="text-lg font-semibold mb-3 flex items-center gap-2">
          <AlertTriangle class="w-5 h-5 text-yellow-500" />
          Alertes ({{ activeAlerts.length }})
        </h2>
        <div class="space-y-2">
          <div
            v-for="alert in activeAlerts.slice(0, 3)"
            :key="alert.id"
            class="p-3 rounded-lg border flex items-center justify-between"
            :class="getAlertSeverityColor(alert.severity)"
          >
            <div>
              <span class="font-medium">{{ alert.student_name }}</span>
              <span class="mx-2">-</span>
              <span>{{ alert.message }}</span>
            </div>
            <Button
              variant="subtle"
              size="sm"
              @click="openMenteeDetail({ id: alert.student_id })"
            >
              Voir
            </Button>
          </div>
        </div>
      </div>

      <!-- Filtres -->
      <div class="flex flex-col sm:flex-row gap-3 mb-6">
        <div class="relative flex-1">
          <Search class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Rechercher un mentoré..."
            class="w-full pl-10 pr-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <select
          v-model="statusFilter"
          class="px-3 py-2 border rounded-lg bg-white focus:ring-2 focus:ring-blue-500"
        >
          <option value="all">Tous les statuts</option>
          <option value="active">Actifs</option>
          <option value="inactive">Inactifs</option>
        </select>
        <select
          v-model="yearFilter"
          class="px-3 py-2 border rounded-lg bg-white focus:ring-2 focus:ring-blue-500"
        >
          <option value="">Toutes les années</option>
          <option v-for="year in uniqueYears" :key="year" :value="year">{{ year }}</option>
        </select>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="flex justify-center py-12">
        <Spinner class="w-8 h-8" />
      </div>

      <!-- Liste vide -->
      <div v-else-if="filteredMentees.length === 0" class="text-center py-12">
        <Users class="w-12 h-12 text-gray-300 mx-auto mb-3" />
        <p class="text-gray-500">Aucun mentoré trouvé</p>
      </div>

      <!-- Liste des mentorés -->
      <div v-else class="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
        <Card
          v-for="mentee in filteredMentees"
          :key="mentee.id"
          class="p-4 hover:shadow-md transition-shadow cursor-pointer"
          @click="openMenteeDetail(mentee)"
        >
          <div class="flex items-start justify-between mb-3">
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
                <span class="text-blue-600 font-semibold">
                  {{ mentee.name?.charAt(0) || '?' }}
                </span>
              </div>
              <div>
                <div class="font-semibold text-gray-900">{{ mentee.name }}</div>
                <div class="text-xs text-gray-500">{{ mentee.id }}</div>
              </div>
            </div>
            <Badge :theme="mentee.status === 'active' ? 'green' : 'red'" size="sm">
              {{ mentee.status === 'active' ? 'Actif' : 'Inactif' }}
            </Badge>
          </div>

          <div class="grid grid-cols-2 gap-2 text-sm mb-3">
            <div>
              <span class="text-gray-500">Année:</span>
              <span class="ml-1 font-medium">{{ mentee.year }}</span>
            </div>
            <div>
              <span class="text-gray-500">Moyenne:</span>
              <span class="ml-1 font-medium" :class="mentee.average >= 10 ? 'text-green-600' : 'text-red-600'">
                {{ mentee.average?.toFixed(1) || '-' }}
              </span>
            </div>
          </div>

          <!-- Barre progression -->
          <div class="mb-3">
            <div class="flex justify-between text-xs mb-1">
              <span class="text-gray-500">Progression</span>
              <span :class="getProgressColor(mentee.progress)">{{ mentee.progress }}%</span>
            </div>
            <div class="w-full h-2 bg-gray-200 rounded-full">
              <div
                class="h-full rounded-full transition-all"
                :class="{
                  'bg-green-500': mentee.progress >= 80,
                  'bg-blue-500': mentee.progress >= 50 && mentee.progress < 80,
                  'bg-yellow-500': mentee.progress >= 25 && mentee.progress < 50,
                  'bg-red-500': mentee.progress < 25,
                }"
                :style="{ width: `${mentee.progress}%` }"
              ></div>
            </div>
            <div class="text-xs text-gray-500 mt-1">
              {{ mentee.validated_ecs }}/{{ mentee.total_ecs }} EC validés
            </div>
          </div>

          <div class="flex items-center justify-between text-xs">
            <span class="text-gray-500">
              Dernière activité: {{ formatDate(mentee.last_activity) }}
            </span>
            <div class="flex gap-1">
              <Button
                variant="ghost"
                size="sm"
                @click.stop="openMessages(mentee)"
                title="Messages"
              >
                <MessageSquare class="w-4 h-4" />
              </Button>
              <ChevronRight class="w-4 h-4 text-gray-400" />
            </div>
          </div>

          <!-- Alerte inactivité -->
          <div
            v-if="mentee.days_inactive > 7"
            class="mt-3 p-2 bg-yellow-50 text-yellow-700 rounded text-xs flex items-center gap-1"
          >
            <AlertTriangle class="w-3 h-3" />
            Inactif depuis {{ mentee.days_inactive }} jours
          </div>
        </Card>
      </div>

      <!-- Activité récente -->
      <div v-if="recentActivity.length > 0" class="mt-8">
        <h2 class="text-lg font-semibold mb-4">Activité récente</h2>
        <Card class="divide-y">
          <div
            v-for="(activity, index) in recentActivity"
            :key="index"
            class="p-3 flex items-center gap-3"
          >
            <div
              class="w-8 h-8 rounded-full flex items-center justify-center"
              :class="{
                'bg-green-100': activity.type === 'ec_validated',
                'bg-blue-100': activity.type === 'message',
                'bg-purple-100': activity.type === 'quiz_passed',
              }"
            >
              <TrendingUp v-if="activity.type === 'ec_validated'" class="w-4 h-4 text-green-600" />
              <MessageSquare v-else-if="activity.type === 'message'" class="w-4 h-4 text-blue-600" />
              <UserCheck v-else class="w-4 h-4 text-purple-600" />
            </div>
            <div class="flex-1">
              <span class="font-medium">{{ activity.student_name }}</span>
              <span class="text-gray-600 ml-1">{{ activity.description }}</span>
            </div>
            <span class="text-xs text-gray-400">{{ activity.timestamp }}</span>
          </div>
        </Card>
      </div>
    </div>
  </div>
</template>
