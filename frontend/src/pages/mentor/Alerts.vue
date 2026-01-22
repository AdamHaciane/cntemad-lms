<!--
  Alerts.vue
  Page de gestion des alertes du mentor.
  Affiche les alertes pour étudiants inactifs, progression faible, etc.
-->
<script setup>
import { ref, computed, onMounted } from 'vue'
import { Card, Button, Badge, Dialog, Spinner } from 'frappe-ui'
import {
  AlertTriangle, Bell, UserX, TrendingDown, XCircle,
  CheckCircle, Eye, MessageSquare, RefreshCw, Filter
} from 'lucide-vue-next'
import { useMentor } from '@/composables/useMentor'
import { useRouter } from 'vue-router'

const router = useRouter()

const {
  alerts,
  loading,
  error,
  activeAlerts,
  fetchAlerts,
  dismissAlert,
  getAlertSeverityColor,
} = useMentor()

const statusFilter = ref('active')
const typeFilter = ref('all')
const showDismissDialog = ref(false)
const selectedAlert = ref(null)
const dismissing = ref(false)

onMounted(async () => {
  await fetchAlerts(statusFilter.value)
})

const filteredAlerts = computed(() => {
  let result = alerts.value

  if (statusFilter.value !== 'all') {
    result = result.filter(a => a.status === statusFilter.value)
  }

  if (typeFilter.value !== 'all') {
    result = result.filter(a => a.type === typeFilter.value)
  }

  return result
})

const alertTypes = [
  { value: 'all', label: 'Tous les types' },
  { value: 'inactive', label: 'Inactivité' },
  { value: 'low_progress', label: 'Progression faible' },
  { value: 'failed_quiz', label: 'Échec quiz' },
]

const getAlertIcon = (type) => {
  switch (type) {
    case 'inactive':
      return UserX
    case 'low_progress':
      return TrendingDown
    case 'failed_quiz':
      return XCircle
    default:
      return AlertTriangle
  }
}

const getAlertTypeLabel = (type) => {
  const found = alertTypes.find(t => t.value === type)
  return found?.label || type
}

const viewMentee = (alert) => {
  router.push(`/mentor/mentee/${alert.student_id}`)
}

const sendMessage = (alert) => {
  router.push(`/mentor/messages/${alert.student_id}`)
}

const openDismissDialog = (alert) => {
  selectedAlert.value = alert
  showDismissDialog.value = true
}

const confirmDismiss = async () => {
  if (!selectedAlert.value) return

  dismissing.value = true
  try {
    await dismissAlert(selectedAlert.value.id)
    showDismissDialog.value = false
    // Recharger les alertes
    await fetchAlerts(statusFilter.value)
  } finally {
    dismissing.value = false
  }
}

const refreshAlerts = async () => {
  await fetchAlerts(statusFilter.value)
}

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleDateString('fr-FR', {
    day: '2-digit',
    month: 'short',
    hour: '2-digit',
    minute: '2-digit',
  })
}
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="bg-white border-b sticky top-0 z-10">
      <div class="max-w-7xl mx-auto px-4 py-4">
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div class="flex items-center gap-3">
            <div class="p-2 bg-yellow-100 rounded-lg">
              <Bell class="w-5 h-5 text-yellow-600" />
            </div>
            <div>
              <h1 class="text-xl font-bold text-gray-900">Alertes</h1>
              <p class="text-sm text-gray-500">
                Suivi des mentorés nécessitant attention
              </p>
            </div>
          </div>
          <div class="flex items-center gap-2">
            <Badge v-if="activeAlerts.length > 0" theme="red">
              {{ activeAlerts.length }} actives
            </Badge>
            <Button variant="subtle" size="sm" @click="refreshAlerts" :loading="loading">
              <RefreshCw class="w-4 h-4" />
            </Button>
          </div>
        </div>
      </div>
    </div>

    <div class="max-w-7xl mx-auto px-4 py-6">
      <!-- Stats par type -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <Card class="p-4 text-center">
          <AlertTriangle class="w-6 h-6 text-yellow-500 mx-auto mb-1" />
          <div class="text-2xl font-bold">{{ alerts.length }}</div>
          <div class="text-xs text-gray-500">Total alertes</div>
        </Card>
        <Card class="p-4 text-center">
          <UserX class="w-6 h-6 text-orange-500 mx-auto mb-1" />
          <div class="text-2xl font-bold text-orange-600">
            {{ alerts.filter(a => a.type === 'inactive').length }}
          </div>
          <div class="text-xs text-gray-500">Inactivité</div>
        </Card>
        <Card class="p-4 text-center">
          <TrendingDown class="w-6 h-6 text-red-500 mx-auto mb-1" />
          <div class="text-2xl font-bold text-red-600">
            {{ alerts.filter(a => a.type === 'low_progress').length }}
          </div>
          <div class="text-xs text-gray-500">Progression faible</div>
        </Card>
        <Card class="p-4 text-center">
          <XCircle class="w-6 h-6 text-purple-500 mx-auto mb-1" />
          <div class="text-2xl font-bold text-purple-600">
            {{ alerts.filter(a => a.type === 'failed_quiz').length }}
          </div>
          <div class="text-xs text-gray-500">Échecs quiz</div>
        </Card>
      </div>

      <!-- Filtres -->
      <div class="flex flex-col sm:flex-row gap-3 mb-6">
        <select
          v-model="statusFilter"
          class="px-3 py-2 border rounded-lg bg-white focus:ring-2 focus:ring-blue-500"
          @change="fetchAlerts(statusFilter)"
        >
          <option value="all">Toutes les alertes</option>
          <option value="active">Actives seulement</option>
          <option value="resolved">Résolues</option>
        </select>
        <select
          v-model="typeFilter"
          class="px-3 py-2 border rounded-lg bg-white focus:ring-2 focus:ring-blue-500"
        >
          <option v-for="type in alertTypes" :key="type.value" :value="type.value">
            {{ type.label }}
          </option>
        </select>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="flex justify-center py-12">
        <Spinner class="w-8 h-8" />
      </div>

      <!-- Error -->
      <div v-else-if="error" class="bg-red-50 text-red-700 p-4 rounded-lg">
        {{ error }}
      </div>

      <!-- Liste vide -->
      <div v-else-if="filteredAlerts.length === 0" class="text-center py-12">
        <CheckCircle class="w-12 h-12 text-green-400 mx-auto mb-3" />
        <p class="text-gray-600 font-medium">Aucune alerte</p>
        <p class="text-sm text-gray-500">Tous vos mentorés sont sur la bonne voie !</p>
      </div>

      <!-- Liste des alertes -->
      <div v-else class="space-y-4">
        <Card
          v-for="alert in filteredAlerts"
          :key="alert.id"
          class="p-4"
          :class="{ 'opacity-60': alert.status === 'resolved' }"
        >
          <div class="flex items-start gap-4">
            <!-- Icône -->
            <div
              class="p-2 rounded-lg flex-shrink-0"
              :class="{
                'bg-orange-100': alert.type === 'inactive',
                'bg-red-100': alert.type === 'low_progress',
                'bg-purple-100': alert.type === 'failed_quiz',
                'bg-yellow-100': !['inactive', 'low_progress', 'failed_quiz'].includes(alert.type),
              }"
            >
              <component
                :is="getAlertIcon(alert.type)"
                class="w-5 h-5"
                :class="{
                  'text-orange-600': alert.type === 'inactive',
                  'text-red-600': alert.type === 'low_progress',
                  'text-purple-600': alert.type === 'failed_quiz',
                  'text-yellow-600': !['inactive', 'low_progress', 'failed_quiz'].includes(alert.type),
                }"
              />
            </div>

            <!-- Contenu -->
            <div class="flex-1">
              <div class="flex items-center gap-2 mb-1">
                <span class="font-semibold text-gray-900">{{ alert.student_name }}</span>
                <Badge
                  :theme="alert.severity === 'danger' ? 'red' : alert.severity === 'warning' ? 'orange' : 'blue'"
                  size="sm"
                >
                  {{ getAlertTypeLabel(alert.type) }}
                </Badge>
                <Badge v-if="alert.status === 'resolved'" theme="green" size="sm">
                  Résolu
                </Badge>
              </div>
              <p class="text-gray-600">{{ alert.message }}</p>
              <p class="text-xs text-gray-500 mt-1">
                Créée le {{ formatDate(alert.created_at) }}
              </p>
            </div>

            <!-- Actions -->
            <div class="flex gap-2">
              <Button variant="subtle" size="sm" @click="viewMentee(alert)" title="Voir profil">
                <Eye class="w-4 h-4" />
              </Button>
              <Button variant="subtle" size="sm" @click="sendMessage(alert)" title="Envoyer message">
                <MessageSquare class="w-4 h-4" />
              </Button>
              <Button
                v-if="alert.status === 'active'"
                variant="subtle"
                size="sm"
                theme="green"
                @click="openDismissDialog(alert)"
                title="Marquer résolu"
              >
                <CheckCircle class="w-4 h-4" />
              </Button>
            </div>
          </div>

          <!-- Suggestions d'action -->
          <div
            v-if="alert.status === 'active'"
            class="mt-3 pt-3 border-t text-sm text-gray-600"
          >
            <span class="font-medium">Action suggérée:</span>
            <span v-if="alert.type === 'inactive'" class="ml-1">
              Contactez l'étudiant pour comprendre la raison de son inactivité.
            </span>
            <span v-else-if="alert.type === 'low_progress'" class="ml-1">
              Proposez une session de rattrapage ou un plan d'étude personnalisé.
            </span>
            <span v-else-if="alert.type === 'failed_quiz'" class="ml-1">
              Identifiez les lacunes et suggérez des ressources complémentaires.
            </span>
          </div>
        </Card>
      </div>
    </div>

    <!-- Dialog Confirmation -->
    <Dialog v-model="showDismissDialog" :options="{ title: 'Marquer comme résolu' }">
      <template #body-content>
        <div v-if="selectedAlert" class="space-y-4">
          <p>
            Êtes-vous sûr de vouloir marquer cette alerte comme résolue ?
          </p>
          <div class="p-3 bg-gray-50 rounded-lg">
            <div class="font-medium">{{ selectedAlert.student_name }}</div>
            <div class="text-sm text-gray-600">{{ selectedAlert.message }}</div>
          </div>
          <p class="text-sm text-gray-500">
            L'alerte sera archivée et ne sera plus affichée dans les alertes actives.
          </p>
        </div>
      </template>
      <template #actions>
        <Button variant="subtle" @click="showDismissDialog = false">Annuler</Button>
        <Button variant="solid" theme="green" @click="confirmDismiss" :loading="dismissing">
          <CheckCircle class="w-4 h-4 mr-1" />
          Marquer résolu
        </Button>
      </template>
    </Dialog>
  </div>
</template>
