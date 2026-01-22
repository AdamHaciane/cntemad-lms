<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="bg-white border-b sticky top-0 z-10">
      <div class="px-4 py-4">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-xl font-bold text-gray-900">
              {{ center?.center_name || 'Dashboard Centre' }}
            </h1>
            <p class="text-sm text-gray-500">
              {{ center?.region || 'Chargement...' }}
            </p>
          </div>
          <Button
            variant="outline"
            @click="refreshDashboard"
            :loading="loading"
          >
            <RefreshCw class="w-4 h-4 mr-2" />
            Actualiser
          </Button>
        </div>
      </div>
    </div>

    <!-- Content -->
    <div class="p-4 space-y-6">
      <!-- KPIs -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <StatsCard
          title="Étudiants"
          :value="kpis?.total_students || 0"
          icon="Users"
          color="blue"
        />
        <StatsCard
          title="Étudiants actifs"
          :value="kpis?.active_students || 0"
          icon="UserCheck"
          color="green"
        />
        <StatsCard
          title="Paiements ce mois"
          :value="kpis?.payments_this_month || 0"
          icon="CreditCard"
          color="purple"
        />
        <StatsCard
          title="Revenus ce mois"
          :value="formatAmount(kpis?.revenue_this_month || 0)"
          icon="TrendingUp"
          color="emerald"
        />
      </div>

      <!-- Taux de validation -->
      <Card>
        <template #title>Taux de validation</template>
        <div class="p-4">
          <div class="flex items-center justify-between mb-2">
            <span class="text-sm text-gray-600">EC validés</span>
            <span class="text-sm font-medium">
              {{ kpis?.validation_rate || 0 }}%
            </span>
          </div>
          <div class="w-full bg-gray-200 rounded-full h-3">
            <div
              class="bg-green-500 h-3 rounded-full transition-all duration-500"
              :style="{ width: `${kpis?.validation_rate || 0}%` }"
            ></div>
          </div>
          <p class="mt-2 text-xs text-gray-500">
            {{ kpis?.validated_enrollments || 0 }} sur {{ kpis?.total_enrollments || 0 }} inscriptions validées
          </p>
        </div>
      </Card>

      <!-- Tendances -->
      <Card v-if="trends.length > 0">
        <template #title>Inscriptions (6 derniers mois)</template>
        <div class="p-4">
          <div class="flex items-end justify-between h-32 gap-2">
            <div
              v-for="trend in trends"
              :key="trend.month"
              class="flex-1 flex flex-col items-center"
            >
              <div
                class="w-full bg-blue-500 rounded-t transition-all duration-300"
                :style="{ height: `${getBarHeight(trend.count)}%` }"
              ></div>
              <span class="text-xs text-gray-500 mt-2">{{ trend.month }}</span>
              <span class="text-xs font-medium">{{ trend.count }}</span>
            </div>
          </div>
        </div>
      </Card>

      <!-- Alertes -->
      <Card v-if="alerts.length > 0">
        <template #title>
          <div class="flex items-center gap-2">
            <AlertTriangle class="w-5 h-5 text-amber-500" />
            Alertes ({{ alerts.length }})
          </div>
        </template>
        <div class="divide-y">
          <div
            v-for="alert in alerts"
            :key="alert.id"
            class="p-4 flex items-start gap-3"
          >
            <div
              :class="[
                'w-2 h-2 rounded-full mt-2',
                alert.level === 'warning' ? 'bg-amber-500' : 'bg-red-500'
              ]"
            ></div>
            <div class="flex-1">
              <p class="text-sm text-gray-900">{{ alert.message }}</p>
              <p class="text-xs text-gray-500 mt-1">{{ alert.date }}</p>
            </div>
          </div>
        </div>
      </Card>

      <!-- Activité récente -->
      <Card>
        <template #title>Activité récente</template>
        <div class="divide-y" v-if="recentActivity.length > 0">
          <div
            v-for="activity in recentActivity"
            :key="activity.id"
            class="p-4 flex items-start gap-3"
          >
            <div
              :class="[
                'w-8 h-8 rounded-full flex items-center justify-center',
                getActivityColor(activity.type)
              ]"
            >
              <component :is="getActivityIcon(activity.type)" class="w-4 h-4" />
            </div>
            <div class="flex-1">
              <p class="text-sm text-gray-900">{{ activity.description }}</p>
              <p class="text-xs text-gray-500 mt-1">{{ activity.time }}</p>
            </div>
          </div>
        </div>
        <div v-else class="p-8 text-center text-gray-500">
          Aucune activité récente
        </div>
      </Card>

      <!-- Actions rapides -->
      <div class="grid grid-cols-2 gap-4">
        <router-link to="/admin/students">
          <Card class="hover:bg-gray-50 transition-colors cursor-pointer">
            <div class="p-4 flex items-center gap-3">
              <div class="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
                <Users class="w-5 h-5 text-blue-600" />
              </div>
              <div>
                <p class="font-medium text-gray-900">Étudiants</p>
                <p class="text-xs text-gray-500">Voir la liste</p>
              </div>
            </div>
          </Card>
        </router-link>

        <router-link to="/admin/payments">
          <Card class="hover:bg-gray-50 transition-colors cursor-pointer">
            <div class="p-4 flex items-center gap-3">
              <div class="w-10 h-10 bg-green-100 rounded-full flex items-center justify-center">
                <CreditCard class="w-5 h-5 text-green-600" />
              </div>
              <div>
                <p class="font-medium text-gray-900">Paiements</p>
                <p class="text-xs text-gray-500">Voir les transactions</p>
              </div>
            </div>
          </Card>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, computed } from 'vue'
import { Button, Card } from 'frappe-ui'
import {
  RefreshCw,
  Users,
  UserCheck,
  CreditCard,
  TrendingUp,
  AlertTriangle,
  CheckCircle,
  XCircle,
  BookOpen
} from 'lucide-vue-next'
import StatsCard from '@/components/custom/StatsCard.vue'
import { useCenter } from '@/composables/useCenter'

const {
  center,
  dashboard,
  kpis,
  trends,
  alerts,
  recentActivity,
  loading,
  fetchDashboard,
  formatAmount
} = useCenter()

onMounted(() => {
  fetchDashboard()
})

const refreshDashboard = () => {
  fetchDashboard()
}

const maxTrendCount = computed(() => {
  if (!trends.value.length) return 1
  return Math.max(...trends.value.map(t => t.count), 1)
})

const getBarHeight = (count) => {
  return Math.max((count / maxTrendCount.value) * 100, 5)
}

const getActivityColor = (type) => {
  const colors = {
    enrollment: 'bg-blue-100 text-blue-600',
    payment: 'bg-green-100 text-green-600',
    validation: 'bg-purple-100 text-purple-600',
    registration: 'bg-amber-100 text-amber-600'
  }
  return colors[type] || 'bg-gray-100 text-gray-600'
}

const getActivityIcon = (type) => {
  const icons = {
    enrollment: BookOpen,
    payment: CreditCard,
    validation: CheckCircle,
    registration: Users
  }
  return icons[type] || Users
}
</script>
