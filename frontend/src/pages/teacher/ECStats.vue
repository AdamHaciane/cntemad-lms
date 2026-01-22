<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="bg-white border-b sticky top-0 z-10">
      <div class="px-4 py-4">
        <div class="flex items-center gap-3">
          <router-link to="/teacher/courses">
            <Button variant="ghost" class="p-2">
              <ArrowLeft class="w-5 h-5" />
            </Button>
          </router-link>
          <div class="flex-1">
            <h1 class="text-xl font-bold text-gray-900">
              {{ ecStats?.ec?.title || 'Statistiques EC' }}
            </h1>
            <p class="text-sm text-gray-500">
              {{ formatAmount(ecStats?.ec?.price || 0) }} •
              <Badge :theme="ecStats?.ec?.is_published ? 'green' : 'gray'" size="sm">
                {{ ecStats?.ec?.is_published ? 'Publié' : 'Brouillon' }}
              </Badge>
            </p>
          </div>
          <Button variant="outline" @click="refreshStats" :loading="loading">
            <RefreshCw class="w-4 h-4 mr-2" />
            Actualiser
          </Button>
        </div>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="loading && !ecStats" class="flex justify-center py-12">
      <Spinner class="w-8 h-8" />
    </div>

    <!-- Content -->
    <div v-else-if="ecStats" class="p-4 space-y-6">
      <!-- KPIs -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <StatsCard
          title="Étudiants inscrits"
          :value="ecStats.stats.total_students"
          icon="Users"
          color="blue"
        />
        <StatsCard
          title="EC validés"
          :value="ecStats.stats.validated"
          icon="CheckCircle"
          color="green"
        />
        <StatsCard
          title="Taux de validation"
          :value="`${ecStats.stats.validation_rate}%`"
          icon="TrendingUp"
          color="purple"
        />
        <StatsCard
          title="Revenus"
          :value="formatAmount(ecStats.stats.total_revenue)"
          icon="DollarSign"
          color="emerald"
        />
      </div>

      <!-- Quiz score -->
      <Card>
        <template #title>Performance au quiz</template>
        <div class="p-4">
          <div class="flex items-center justify-between mb-4">
            <div>
              <p class="text-3xl font-bold text-gray-900">
                {{ ecStats.stats.avg_quiz_score }}%
              </p>
              <p class="text-sm text-gray-500">Score moyen</p>
            </div>
            <div class="text-right">
              <p class="text-lg font-semibold text-gray-900">
                {{ ecStats.stats.validated }} / {{ ecStats.stats.total_students }}
              </p>
              <p class="text-sm text-gray-500">ont réussi</p>
            </div>
          </div>

          <!-- Progress bar -->
          <div class="w-full bg-gray-200 rounded-full h-3">
            <div
              class="h-3 rounded-full transition-all duration-500"
              :class="getScoreColor(ecStats.stats.avg_quiz_score)"
              :style="{ width: `${ecStats.stats.avg_quiz_score}%` }"
            ></div>
          </div>
        </div>
      </Card>

      <!-- Enrollment trends -->
      <Card v-if="ecStats.trends?.length > 0">
        <template #title>Inscriptions (6 derniers mois)</template>
        <div class="p-4">
          <div class="flex items-end justify-between h-40 gap-2">
            <div
              v-for="trend in ecStats.trends"
              :key="trend.month"
              class="flex-1 flex flex-col items-center"
            >
              <div
                class="w-full bg-blue-500 rounded-t transition-all duration-300"
                :style="{ height: `${getBarHeight(trend.count)}%` }"
              ></div>
              <span class="text-xs text-gray-500 mt-2">{{ trend.month }}</span>
              <span class="text-sm font-medium">{{ trend.count }}</span>
            </div>
          </div>
        </div>
      </Card>

      <!-- Status distribution -->
      <Card>
        <template #title>Répartition des étudiants</template>
        <div class="p-4">
          <div class="space-y-4">
            <!-- Validated -->
            <div>
              <div class="flex items-center justify-between mb-1">
                <span class="text-sm text-gray-600">Validés</span>
                <span class="text-sm font-medium text-green-600">
                  {{ ecStats.stats.validated }}
                </span>
              </div>
              <div class="w-full bg-gray-200 rounded-full h-2">
                <div
                  class="bg-green-500 h-2 rounded-full transition-all"
                  :style="{ width: `${getPercent(ecStats.stats.validated)}%` }"
                ></div>
              </div>
            </div>

            <!-- In progress -->
            <div>
              <div class="flex items-center justify-between mb-1">
                <span class="text-sm text-gray-600">En cours</span>
                <span class="text-sm font-medium text-blue-600">
                  {{ ecStats.stats.in_progress }}
                </span>
              </div>
              <div class="w-full bg-gray-200 rounded-full h-2">
                <div
                  class="bg-blue-500 h-2 rounded-full transition-all"
                  :style="{ width: `${getPercent(ecStats.stats.in_progress)}%` }"
                ></div>
              </div>
            </div>

            <!-- Not started -->
            <div>
              <div class="flex items-center justify-between mb-1">
                <span class="text-sm text-gray-600">Non commencés</span>
                <span class="text-sm font-medium text-gray-600">
                  {{ ecStats.stats.total_students - ecStats.stats.validated - ecStats.stats.in_progress }}
                </span>
              </div>
              <div class="w-full bg-gray-200 rounded-full h-2">
                <div
                  class="bg-gray-400 h-2 rounded-full transition-all"
                  :style="{ width: `${getPercent(ecStats.stats.total_students - ecStats.stats.validated - ecStats.stats.in_progress)}%` }"
                ></div>
              </div>
            </div>
          </div>
        </div>
      </Card>

      <!-- Recent enrollments -->
      <Card>
        <template #title>Inscriptions récentes</template>
        <div v-if="ecStats.recent_enrollments?.length > 0" class="divide-y">
          <div
            v-for="enrollment in ecStats.recent_enrollments"
            :key="enrollment.student"
            class="p-4 flex items-center gap-3"
          >
            <Avatar
              :label="enrollment.student_name"
              size="sm"
            />
            <div class="flex-1 min-w-0">
              <p class="font-medium text-gray-900 truncate">
                {{ enrollment.student_name }}
              </p>
              <p class="text-xs text-gray-500">
                {{ enrollment.student_email }}
              </p>
            </div>
            <div class="text-right">
              <Badge :theme="getStatusTheme(enrollment.status)" size="sm">
                {{ getStatusLabel(enrollment.status) }}
              </Badge>
              <p class="text-xs text-gray-500 mt-1">
                {{ formatDate(enrollment.creation) }}
              </p>
            </div>
          </div>
        </div>
        <div v-else class="p-8 text-center text-gray-500">
          Aucune inscription récente
        </div>
      </Card>
    </div>

    <!-- Error -->
    <div v-else class="text-center py-12">
      <AlertTriangle class="w-12 h-12 text-gray-300 mx-auto mb-4" />
      <p class="text-gray-500">Impossible de charger les statistiques</p>
      <Button variant="outline" class="mt-4" @click="refreshStats">
        Réessayer
      </Button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { Button, Card, Badge, Avatar, Spinner } from 'frappe-ui'
import { ArrowLeft, RefreshCw, AlertTriangle } from 'lucide-vue-next'
import StatsCard from '@/components/custom/StatsCard.vue'
import { useTeacher } from '@/composables/useTeacher'

const route = useRoute()

const { ecStats, loading, fetchECStats, formatAmount } = useTeacher()

const ecId = computed(() => route.params.id)

onMounted(() => {
  if (ecId.value) {
    fetchECStats(ecId.value)
  }
})

const refreshStats = () => {
  if (ecId.value) {
    fetchECStats(ecId.value)
  }
}

const maxTrendCount = computed(() => {
  if (!ecStats.value?.trends?.length) return 1
  return Math.max(...ecStats.value.trends.map(t => t.count), 1)
})

const getBarHeight = (count) => {
  return Math.max((count / maxTrendCount.value) * 100, 5)
}

const getPercent = (value) => {
  const total = ecStats.value?.stats?.total_students || 1
  return Math.round((value / total) * 100)
}

const getScoreColor = (score) => {
  if (score >= 70) return 'bg-green-500'
  if (score >= 50) return 'bg-yellow-500'
  return 'bg-red-500'
}

const getStatusTheme = (status) => {
  const themes = {
    Validated: 'green',
    'In Progress': 'blue',
    Paid: 'purple'
  }
  return themes[status] || 'gray'
}

const getStatusLabel = (status) => {
  const labels = {
    Validated: 'Validé',
    'In Progress': 'En cours',
    Paid: 'Payé'
  }
  return labels[status] || status
}

const formatDate = (date) => {
  if (!date) return '-'
  return new Date(date).toLocaleDateString('fr-FR', {
    day: 'numeric',
    month: 'short'
  })
}
</script>
