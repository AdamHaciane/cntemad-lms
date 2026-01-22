<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="bg-white border-b sticky top-0 z-10">
      <div class="px-4 py-4">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-xl font-bold text-gray-900">Dashboard National</h1>
            <p class="text-sm text-gray-500">
              CNTEMAD - {{ kpis?.total_centers || 34 }} centres régionaux
            </p>
          </div>
          <div class="flex gap-2">
            <Button variant="outline" @click="showExportDialog = true">
              <Download class="w-4 h-4 mr-2" />
              Exporter
            </Button>
            <Button variant="outline" @click="refreshDashboard" :loading="loading">
              <RefreshCw class="w-4 h-4" />
            </Button>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="loading && !dashboard" class="flex justify-center py-12">
      <Spinner class="w-8 h-8" />
    </div>

    <!-- Content -->
    <div v-else class="p-4 space-y-6">
      <!-- KPIs Row 1 -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <StatsCard
          title="Étudiants"
          :value="formatNumber(kpis?.total_students || 0)"
          icon="Users"
          color="blue"
        />
        <StatsCard
          title="Étudiants actifs"
          :value="formatNumber(kpis?.active_students || 0)"
          icon="UserCheck"
          color="green"
        />
        <StatsCard
          title="Centres"
          :value="kpis?.total_centers || 0"
          icon="Building"
          color="purple"
        />
        <StatsCard
          title="EC publiés"
          :value="kpis?.published_ecs || 0"
          icon="BookOpen"
          color="amber"
        />
      </div>

      <!-- KPIs Row 2 -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <StatsCard
          title="Inscriptions"
          :value="formatNumber(kpis?.total_enrollments || 0)"
          icon="FileText"
          color="blue"
        />
        <StatsCard
          title="Validées"
          :value="formatNumber(kpis?.validated_enrollments || 0)"
          icon="CheckCircle"
          color="green"
        />
        <StatsCard
          title="Revenus ce mois"
          :value="formatAmount(kpis?.revenue_this_month || 0)"
          icon="TrendingUp"
          color="emerald"
        />
        <StatsCard
          title="Revenus totaux"
          :value="formatAmount(kpis?.total_revenue || 0)"
          icon="DollarSign"
          color="emerald"
        />
      </div>

      <!-- Validation rate -->
      <Card>
        <template #title>Taux de validation national</template>
        <div class="p-4">
          <div class="flex items-center justify-between mb-2">
            <span class="text-sm text-gray-600">EC validés</span>
            <span class="text-2xl font-bold text-green-600">
              {{ kpis?.validation_rate || 0 }}%
            </span>
          </div>
          <div class="w-full bg-gray-200 rounded-full h-4">
            <div
              class="bg-green-500 h-4 rounded-full transition-all duration-500"
              :style="{ width: `${kpis?.validation_rate || 0}%` }"
            ></div>
          </div>
          <p class="text-sm text-gray-500 mt-2">
            {{ formatNumber(kpis?.validated_enrollments || 0) }} sur
            {{ formatNumber(kpis?.total_enrollments || 0) }} inscriptions
          </p>
        </div>
      </Card>

      <!-- Trends chart -->
      <Card v-if="trends.length > 0">
        <template #title>Évolution nationale (6 mois)</template>
        <div class="p-4">
          <div class="flex items-end justify-between h-48 gap-2">
            <div
              v-for="trend in trends"
              :key="trend.month"
              class="flex-1 flex flex-col items-center"
            >
              <div class="w-full flex flex-col gap-1" style="height: 160px;">
                <!-- Enrollments bar -->
                <div
                  class="w-full bg-blue-500 rounded-t transition-all duration-300"
                  :style="{ height: `${getBarHeight(trend.enrollments, 'enrollments')}%` }"
                  :title="`${trend.enrollments} inscriptions`"
                ></div>
              </div>
              <span class="text-xs text-gray-500 mt-2">{{ trend.month_short }}</span>
              <span class="text-xs font-medium">{{ trend.enrollments }}</span>
            </div>
          </div>
          <div class="flex items-center justify-center gap-6 mt-4 text-sm">
            <span class="flex items-center gap-2">
              <span class="w-3 h-3 bg-blue-500 rounded"></span>
              Inscriptions
            </span>
          </div>
        </div>
      </Card>

      <!-- Top centers + Alerts -->
      <div class="grid md:grid-cols-2 gap-4">
        <!-- Top centers -->
        <Card>
          <template #title>
            <div class="flex items-center justify-between">
              <span>Top 5 centres</span>
              <router-link to="/national/centers">
                <Button variant="ghost" size="sm">Voir tout</Button>
              </router-link>
            </div>
          </template>
          <div class="divide-y">
            <div
              v-for="(center, index) in topCenters"
              :key="center.name"
              class="p-4 flex items-center gap-3"
            >
              <div
                class="w-8 h-8 rounded-full flex items-center justify-center font-bold text-white"
                :class="getMedalColor(index)"
              >
                {{ index + 1 }}
              </div>
              <div class="flex-1 min-w-0">
                <p class="font-medium text-gray-900 truncate">
                  {{ center.center_name }}
                </p>
                <p class="text-xs text-gray-500">
                  {{ center.region }} • {{ center.student_count }} étudiants
                </p>
              </div>
              <span class="text-sm font-medium text-green-600">
                {{ formatAmount(center.revenue) }}
              </span>
            </div>
          </div>
        </Card>

        <!-- Alerts -->
        <Card>
          <template #title>
            <div class="flex items-center gap-2">
              <AlertTriangle class="w-5 h-5 text-amber-500" />
              Alertes ({{ alerts.length }})
            </div>
          </template>
          <div v-if="alerts.length > 0" class="divide-y">
            <div
              v-for="alert in alerts"
              :key="alert.id"
              class="p-4 flex items-start gap-3"
            >
              <div
                :class="[
                  'w-2 h-2 rounded-full mt-2',
                  alert.level === 'error' ? 'bg-red-500' : 'bg-amber-500'
                ]"
              ></div>
              <div>
                <p class="text-sm text-gray-900">{{ alert.message }}</p>
                <p v-if="alert.center" class="text-xs text-gray-500 mt-1">
                  {{ alert.center }}
                </p>
              </div>
            </div>
          </div>
          <div v-else class="p-8 text-center text-gray-500">
            Aucune alerte
          </div>
        </Card>
      </div>

      <!-- Recent activity -->
      <Card>
        <template #title>Activité récente</template>
        <div v-if="recentActivity.length > 0" class="divide-y">
          <div
            v-for="activity in recentActivity"
            :key="activity.id"
            class="p-4 flex items-center gap-3"
          >
            <div
              :class="[
                'w-10 h-10 rounded-full flex items-center justify-center',
                getActivityColor(activity.type)
              ]"
            >
              <component :is="getActivityIcon(activity.type)" class="w-5 h-5" />
            </div>
            <div class="flex-1 min-w-0">
              <p class="text-sm text-gray-900">{{ activity.description }}</p>
              <p class="text-xs text-gray-500">
                {{ activity.center }} • {{ activity.time }}
              </p>
            </div>
          </div>
        </div>
        <div v-else class="p-8 text-center text-gray-500">
          Aucune activité récente
        </div>
      </Card>

      <!-- Quick actions -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <router-link to="/national/map">
          <Card class="hover:bg-gray-50 transition-colors cursor-pointer h-full">
            <div class="p-4 flex flex-col items-center text-center">
              <Map class="w-8 h-8 text-blue-600 mb-2" />
              <p class="font-medium text-gray-900">Carte</p>
              <p class="text-xs text-gray-500">34 centres</p>
            </div>
          </Card>
        </router-link>

        <router-link to="/national/centers">
          <Card class="hover:bg-gray-50 transition-colors cursor-pointer h-full">
            <div class="p-4 flex flex-col items-center text-center">
              <Building class="w-8 h-8 text-purple-600 mb-2" />
              <p class="font-medium text-gray-900">Centres</p>
              <p class="text-xs text-gray-500">Voir détails</p>
            </div>
          </Card>
        </router-link>

        <router-link to="/national/compare">
          <Card class="hover:bg-gray-50 transition-colors cursor-pointer h-full">
            <div class="p-4 flex flex-col items-center text-center">
              <BarChart3 class="w-8 h-8 text-green-600 mb-2" />
              <p class="font-medium text-gray-900">Comparer</p>
              <p class="text-xs text-gray-500">Analyse centres</p>
            </div>
          </Card>
        </router-link>

        <Card
          class="hover:bg-gray-50 transition-colors cursor-pointer h-full"
          @click="showExportDialog = true"
        >
          <div class="p-4 flex flex-col items-center text-center">
            <Download class="w-8 h-8 text-amber-600 mb-2" />
            <p class="font-medium text-gray-900">Rapports</p>
            <p class="text-xs text-gray-500">Exporter CSV</p>
          </div>
        </Card>
      </div>
    </div>

    <!-- Export Dialog -->
    <Dialog v-model="showExportDialog" :options="{ title: 'Exporter un rapport' }">
      <template #body-content>
        <div class="space-y-4">
          <Select
            v-model="exportType"
            :options="exportOptions"
            label="Type de rapport"
          />
          <div class="grid grid-cols-2 gap-4">
            <Input
              v-model="exportDateFrom"
              type="date"
              label="Date début"
            />
            <Input
              v-model="exportDateTo"
              type="date"
              label="Date fin"
            />
          </div>
        </div>
      </template>
      <template #actions>
        <Button variant="outline" @click="showExportDialog = false">Annuler</Button>
        <Button
          variant="solid"
          @click="handleExport"
          :loading="exporting"
        >
          <Download class="w-4 h-4 mr-2" />
          Exporter CSV
        </Button>
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { Button, Card, Badge, Input, Select, Dialog, Spinner } from 'frappe-ui'
import {
  RefreshCw,
  Download,
  AlertTriangle,
  Map,
  Building,
  BarChart3,
  Users,
  CreditCard,
  CheckCircle,
  BookOpen
} from 'lucide-vue-next'
import StatsCard from '@/components/custom/StatsCard.vue'
import { useNational } from '@/composables/useNational'

const {
  dashboard,
  kpis,
  trends,
  alerts,
  topCenters,
  recentActivity,
  loading,
  exporting,
  fetchDashboard,
  exportReport,
  formatAmount,
  formatNumber
} = useNational()

const showExportDialog = ref(false)
const exportType = ref('summary')
const exportDateFrom = ref('')
const exportDateTo = ref('')

const exportOptions = [
  { label: 'Résumé national', value: 'summary' },
  { label: 'Liste des centres', value: 'centers' },
  { label: 'Liste des étudiants', value: 'students' },
  { label: 'Liste des paiements', value: 'payments' }
]

onMounted(() => {
  fetchDashboard()
})

const refreshDashboard = () => {
  fetchDashboard()
}

const maxTrendValue = computed(() => {
  if (!trends.value.length) return 1
  return Math.max(...trends.value.map(t => t.enrollments), 1)
})

const getBarHeight = (value, type) => {
  return Math.max((value / maxTrendValue.value) * 100, 5)
}

const getMedalColor = (index) => {
  const colors = ['bg-yellow-500', 'bg-gray-400', 'bg-amber-600', 'bg-blue-500', 'bg-purple-500']
  return colors[index] || 'bg-gray-500'
}

const getActivityColor = (type) => {
  const colors = {
    enrollment: 'bg-blue-100 text-blue-600',
    payment: 'bg-green-100 text-green-600',
    validation: 'bg-purple-100 text-purple-600'
  }
  return colors[type] || 'bg-gray-100 text-gray-600'
}

const getActivityIcon = (type) => {
  const icons = {
    enrollment: BookOpen,
    payment: CreditCard,
    validation: CheckCircle
  }
  return icons[type] || Users
}

const handleExport = async () => {
  await exportReport(
    exportType.value,
    exportDateFrom.value || null,
    exportDateTo.value || null
  )
  showExportDialog.value = false
}
</script>
