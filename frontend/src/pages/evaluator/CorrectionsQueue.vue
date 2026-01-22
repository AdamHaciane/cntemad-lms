<!--
  CorrectionsQueue.vue
  File d'attente des corrections pour l'évaluateur.
  Affiche la liste des soumissions à corriger avec filtres et tri.
-->
<script setup>
import { ref, computed, onMounted } from 'vue'
import { Card, Button, Badge, Input, Spinner, Dialog } from 'frappe-ui'
import { Search, Filter, Clock, User, BookOpen, ChevronRight, RefreshCw, AlertCircle } from 'lucide-vue-next'
import { useEvaluator } from '@/composables/useEvaluator'
import { useRouter } from 'vue-router'

const router = useRouter()
const {
  dashboard,
  pendingCorrections,
  recentCorrections,
  loading,
  error,
  stats,
  evaluator,
  fetchDashboard,
  fetchPendingCorrections,
} = useEvaluator()

const searchQuery = ref('')
const selectedFilter = ref('all')
const showFilterDialog = ref(false)
const filters = ref({
  ec: '',
  course: '',
  urgency: 'all', // all, urgent, normal
})

onMounted(async () => {
  await fetchDashboard()
})

const filteredCorrections = computed(() => {
  let result = pendingCorrections.value

  // Filtre par recherche
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(c =>
      c.student_name?.toLowerCase().includes(query) ||
      c.ec_title?.toLowerCase().includes(query) ||
      c.student_id?.toLowerCase().includes(query)
    )
  }

  // Filtre par urgence
  if (filters.value.urgency === 'urgent') {
    result = result.filter(c => c.days_pending > 5)
  } else if (filters.value.urgency === 'normal') {
    result = result.filter(c => c.days_pending <= 5)
  }

  // Filtre par EC
  if (filters.value.ec) {
    result = result.filter(c => c.ec_id === filters.value.ec)
  }

  return result
})

const uniqueECs = computed(() => {
  const ecs = new Map()
  pendingCorrections.value.forEach(c => {
    if (c.ec_id && !ecs.has(c.ec_id)) {
      ecs.set(c.ec_id, c.ec_title)
    }
  })
  return Array.from(ecs, ([id, title]) => ({ id, title }))
})

const getUrgencyBadge = (daysPending) => {
  if (daysPending > 7) return { label: 'Très urgent', theme: 'red' }
  if (daysPending > 5) return { label: 'Urgent', theme: 'orange' }
  if (daysPending > 3) return { label: 'Modéré', theme: 'yellow' }
  return { label: 'Normal', theme: 'green' }
}

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleDateString('fr-FR', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

const openCorrection = (correction) => {
  router.push(`/evaluator/correction/${correction.id}`)
}

const refreshList = async () => {
  await fetchDashboard()
}

const applyFilters = () => {
  showFilterDialog.value = false
}

const resetFilters = () => {
  filters.value = {
    ec: '',
    course: '',
    urgency: 'all',
  }
  searchQuery.value = ''
}
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="bg-white border-b sticky top-0 z-10">
      <div class="max-w-7xl mx-auto px-4 py-4">
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h1 class="text-xl font-bold text-gray-900">File de corrections</h1>
            <p class="text-sm text-gray-500" v-if="evaluator">
              {{ evaluator.full_name }} - {{ evaluator.specialty || 'Évaluateur' }}
            </p>
          </div>
          <div class="flex items-center gap-2">
            <Badge v-if="stats" theme="blue">
              {{ stats.pending_count || 0 }} en attente
            </Badge>
            <Button variant="subtle" size="sm" @click="refreshList" :loading="loading">
              <RefreshCw class="w-4 h-4" />
            </Button>
          </div>
        </div>
      </div>
    </div>

    <div class="max-w-7xl mx-auto px-4 py-6">
      <!-- Stats rapides -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <Card class="p-4">
          <div class="text-sm text-gray-500">En attente</div>
          <div class="text-2xl font-bold text-blue-600">{{ stats?.pending_count || 0 }}</div>
        </Card>
        <Card class="p-4">
          <div class="text-sm text-gray-500">Urgentes</div>
          <div class="text-2xl font-bold text-red-600">
            {{ pendingCorrections.filter(c => c.days_pending > 5).length }}
          </div>
        </Card>
        <Card class="p-4">
          <div class="text-sm text-gray-500">Cette semaine</div>
          <div class="text-2xl font-bold text-green-600">{{ stats?.week_count || 0 }}</div>
        </Card>
        <Card class="p-4">
          <div class="text-sm text-gray-500">Ce mois</div>
          <div class="text-2xl font-bold text-gray-700">{{ stats?.month_count || 0 }}</div>
        </Card>
      </div>

      <!-- Barre de recherche et filtres -->
      <div class="flex flex-col sm:flex-row gap-3 mb-6">
        <div class="relative flex-1">
          <Search class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Rechercher par nom, EC..."
            class="w-full pl-10 pr-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
        <div class="flex gap-2">
          <select
            v-model="filters.urgency"
            class="px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 bg-white"
          >
            <option value="all">Toutes urgences</option>
            <option value="urgent">Urgent seulement</option>
            <option value="normal">Normal seulement</option>
          </select>
          <Button variant="subtle" @click="showFilterDialog = true">
            <Filter class="w-4 h-4" />
            <span class="hidden sm:inline ml-1">Filtres</span>
          </Button>
        </div>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="flex justify-center py-12">
        <Spinner class="w-8 h-8" />
      </div>

      <!-- Error -->
      <div v-else-if="error" class="bg-red-50 text-red-700 p-4 rounded-lg flex items-center gap-2">
        <AlertCircle class="w-5 h-5" />
        {{ error }}
      </div>

      <!-- Liste vide -->
      <div v-else-if="filteredCorrections.length === 0" class="text-center py-12">
        <BookOpen class="w-12 h-12 text-gray-300 mx-auto mb-3" />
        <p class="text-gray-500">Aucune correction en attente</p>
        <p class="text-sm text-gray-400" v-if="searchQuery || filters.urgency !== 'all'">
          Essayez de modifier vos filtres
        </p>
      </div>

      <!-- Liste des corrections -->
      <div v-else class="space-y-3">
        <Card
          v-for="correction in filteredCorrections"
          :key="correction.id"
          class="p-4 hover:shadow-md transition-shadow cursor-pointer"
          @click="openCorrection(correction)"
        >
          <div class="flex items-start justify-between gap-4">
            <div class="flex-1 min-w-0">
              <div class="flex items-center gap-2 flex-wrap">
                <span class="font-medium text-gray-900 truncate">
                  {{ correction.student_name }}
                </span>
                <Badge :theme="getUrgencyBadge(correction.days_pending).theme" size="sm">
                  {{ getUrgencyBadge(correction.days_pending).label }}
                </Badge>
              </div>

              <div class="text-sm text-gray-600 mt-1">
                {{ correction.ec_title }}
              </div>

              <div class="flex items-center gap-4 mt-2 text-xs text-gray-500">
                <span class="flex items-center gap-1">
                  <User class="w-3 h-3" />
                  {{ correction.student_id }}
                </span>
                <span class="flex items-center gap-1">
                  <Clock class="w-3 h-3" />
                  {{ formatDate(correction.submitted_at) }}
                </span>
                <span v-if="correction.days_pending > 0" class="text-orange-600">
                  {{ correction.days_pending }}j d'attente
                </span>
              </div>
            </div>

            <ChevronRight class="w-5 h-5 text-gray-400 flex-shrink-0" />
          </div>
        </Card>
      </div>

      <!-- Corrections récentes -->
      <div v-if="recentCorrections.length > 0" class="mt-8">
        <h2 class="text-lg font-semibold text-gray-900 mb-4">Corrections récentes</h2>
        <div class="space-y-2">
          <div
            v-for="correction in recentCorrections.slice(0, 5)"
            :key="correction.id"
            class="flex items-center justify-between p-3 bg-white rounded-lg border"
          >
            <div>
              <span class="font-medium">{{ correction.student_name }}</span>
              <span class="text-gray-500 mx-2">-</span>
              <span class="text-sm text-gray-600">{{ correction.ec_title }}</span>
            </div>
            <div class="flex items-center gap-3">
              <span class="font-bold" :class="correction.grade >= 10 ? 'text-green-600' : 'text-red-600'">
                {{ correction.grade }}/20
              </span>
              <span class="text-xs text-gray-400">{{ formatDate(correction.corrected_at) }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Dialog Filtres avancés -->
    <Dialog v-model="showFilterDialog" :options="{ title: 'Filtres avancés' }">
      <template #body-content>
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">EC</label>
            <select v-model="filters.ec" class="w-full px-3 py-2 border rounded-lg">
              <option value="">Tous les EC</option>
              <option v-for="ec in uniqueECs" :key="ec.id" :value="ec.id">
                {{ ec.title }}
              </option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Urgence</label>
            <select v-model="filters.urgency" class="w-full px-3 py-2 border rounded-lg">
              <option value="all">Toutes</option>
              <option value="urgent">Urgent (> 5 jours)</option>
              <option value="normal">Normal</option>
            </select>
          </div>
        </div>
      </template>
      <template #actions>
        <Button variant="subtle" @click="resetFilters">Réinitialiser</Button>
        <Button variant="solid" @click="applyFilters">Appliquer</Button>
      </template>
    </Dialog>
  </div>
</template>
