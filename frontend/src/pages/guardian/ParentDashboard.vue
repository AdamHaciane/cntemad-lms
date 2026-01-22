<!--
  ParentDashboard.vue
  Dashboard principal du parent/tuteur avec vue sur les enfants.
-->
<script setup>
import { ref, computed, onMounted } from 'vue'
import { Card, Button, Badge, Spinner } from 'frappe-ui'
import {
  Users, TrendingUp, CreditCard, Bell, ChevronRight,
  CheckCircle, Clock, AlertTriangle, RefreshCw, User
} from 'lucide-vue-next'
import { useGuardian } from '@/composables/useGuardian'
import { useRouter } from 'vue-router'

const router = useRouter()

const {
  dashboard,
  children,
  notifications,
  loading,
  stats,
  guardian,
  recentActivity,
  unreadCount,
  avgProgress,
  fetchDashboard,
  getProgressColor,
  getProgressBgColor,
  formatAmount,
  getNotificationColor,
} = useGuardian()

onMounted(async () => {
  await fetchDashboard()
})

const viewChild = (child) => {
  router.push(`/parent/child/${child.id}`)
}

const payForChild = (child) => {
  router.push(`/parent/pay/${child.id}`)
}

const viewNotifications = () => {
  router.push('/parent/notifications')
}

const refreshData = async () => {
  await fetchDashboard()
}

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleDateString('fr-FR', { day: '2-digit', month: 'short' })
}

const getActivityIcon = (type) => {
  switch (type) {
    case 'ec_validated':
      return CheckCircle
    case 'payment':
      return CreditCard
    case 'quiz':
      return TrendingUp
    default:
      return Clock
  }
}

const getActivityColor = (type) => {
  switch (type) {
    case 'ec_validated':
      return 'bg-green-100 text-green-600'
    case 'payment':
      return 'bg-blue-100 text-blue-600'
    case 'quiz':
      return 'bg-purple-100 text-purple-600'
    default:
      return 'bg-gray-100 text-gray-600'
  }
}
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="bg-white border-b sticky top-0 z-10">
      <div class="max-w-7xl mx-auto px-4 py-4">
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h1 class="text-xl font-bold text-gray-900">Bonjour, {{ guardian?.full_name?.split(' ')[0] || 'Parent' }}</h1>
            <p class="text-sm text-gray-500">
              Suivi de {{ children.length }} enfant{{ children.length > 1 ? 's' : '' }}
            </p>
          </div>
          <div class="flex items-center gap-2">
            <Button variant="subtle" @click="viewNotifications" class="relative">
              <Bell class="w-5 h-5" />
              <span
                v-if="unreadCount > 0"
                class="absolute -top-1 -right-1 w-5 h-5 bg-red-500 text-white text-xs rounded-full flex items-center justify-center"
              >
                {{ unreadCount }}
              </span>
            </Button>
            <Button variant="subtle" size="sm" @click="refreshData" :loading="loading">
              <RefreshCw class="w-4 h-4" />
            </Button>
          </div>
        </div>
      </div>
    </div>

    <div class="max-w-7xl mx-auto px-4 py-6">
      <!-- Loading -->
      <div v-if="loading && !dashboard" class="flex justify-center py-12">
        <Spinner class="w-8 h-8" />
      </div>

      <template v-else>
        <!-- Stats globales -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
          <Card class="p-4">
            <div class="flex items-center gap-3">
              <div class="p-2 bg-blue-100 rounded-lg">
                <Users class="w-5 h-5 text-blue-600" />
              </div>
              <div>
                <div class="text-2xl font-bold">{{ stats?.total_children || 0 }}</div>
                <div class="text-xs text-gray-500">Enfants</div>
              </div>
            </div>
          </Card>
          <Card class="p-4">
            <div class="flex items-center gap-3">
              <div class="p-2 bg-green-100 rounded-lg">
                <CheckCircle class="w-5 h-5 text-green-600" />
              </div>
              <div>
                <div class="text-2xl font-bold text-green-600">{{ stats?.total_validated_ecs || 0 }}</div>
                <div class="text-xs text-gray-500">EC validés</div>
              </div>
            </div>
          </Card>
          <Card class="p-4">
            <div class="flex items-center gap-3">
              <div class="p-2 bg-purple-100 rounded-lg">
                <TrendingUp class="w-5 h-5 text-purple-600" />
              </div>
              <div>
                <div class="text-2xl font-bold" :class="getProgressColor(avgProgress)">
                  {{ avgProgress.toFixed(0) }}%
                </div>
                <div class="text-xs text-gray-500">Progression moy.</div>
              </div>
            </div>
          </Card>
          <Card class="p-4">
            <div class="flex items-center gap-3">
              <div class="p-2 bg-yellow-100 rounded-lg">
                <CreditCard class="w-5 h-5 text-yellow-600" />
              </div>
              <div>
                <div class="text-xl font-bold">{{ formatAmount(stats?.total_payments || 0) }}</div>
                <div class="text-xs text-gray-500">Total payé</div>
              </div>
            </div>
          </Card>
        </div>

        <!-- Mes enfants -->
        <div class="mb-6">
          <h2 class="text-lg font-semibold mb-4">Mes enfants</h2>
          <div class="grid md:grid-cols-2 gap-4">
            <Card
              v-for="child in children"
              :key="child.id"
              class="p-4 hover:shadow-md transition-shadow cursor-pointer"
              @click="viewChild(child)"
            >
              <div class="flex items-start gap-4">
                <!-- Avatar -->
                <div class="w-14 h-14 bg-blue-100 rounded-full flex items-center justify-center flex-shrink-0">
                  <User class="w-7 h-7 text-blue-600" />
                </div>

                <!-- Info -->
                <div class="flex-1 min-w-0">
                  <div class="flex items-center justify-between mb-1">
                    <h3 class="font-semibold text-gray-900">{{ child.name }}</h3>
                    <Badge :theme="child.status === 'active' ? 'green' : 'red'" size="sm">
                      {{ child.year }}
                    </Badge>
                  </div>
                  <p class="text-sm text-gray-500 mb-2">{{ child.center }}</p>

                  <!-- Progression -->
                  <div class="mb-2">
                    <div class="flex justify-between text-xs mb-1">
                      <span class="text-gray-500">Progression</span>
                      <span :class="getProgressColor(child.progress)">{{ child.progress }}%</span>
                    </div>
                    <div class="w-full h-2 bg-gray-200 rounded-full">
                      <div
                        class="h-full rounded-full transition-all"
                        :class="getProgressBgColor(child.progress)"
                        :style="{ width: `${child.progress}%` }"
                      ></div>
                    </div>
                  </div>

                  <!-- Stats -->
                  <div class="flex items-center justify-between text-xs text-gray-500">
                    <span>{{ child.validated_ecs }}/{{ child.total_ecs }} EC</span>
                    <span>Moy: {{ child.average?.toFixed(1) || '-' }}/20</span>
                  </div>
                </div>

                <ChevronRight class="w-5 h-5 text-gray-400 flex-shrink-0" />
              </div>

              <!-- Actions -->
              <div class="flex gap-2 mt-4 pt-3 border-t">
                <Button variant="subtle" size="sm" class="flex-1" @click.stop="viewChild(child)">
                  Voir détails
                </Button>
                <Button variant="solid" size="sm" class="flex-1" @click.stop="payForChild(child)">
                  <CreditCard class="w-4 h-4 mr-1" />
                  Payer EC
                </Button>
              </div>
            </Card>
          </div>
        </div>

        <!-- Activité récente -->
        <div v-if="recentActivity.length > 0">
          <h2 class="text-lg font-semibold mb-4">Activité récente</h2>
          <Card class="divide-y">
            <div
              v-for="(activity, index) in recentActivity"
              :key="index"
              class="p-4 flex items-start gap-3"
            >
              <div
                class="w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0"
                :class="getActivityColor(activity.type)"
              >
                <component :is="getActivityIcon(activity.type)" class="w-5 h-5" />
              </div>
              <div class="flex-1 min-w-0">
                <div class="flex items-center gap-2">
                  <span class="font-medium text-gray-900">{{ activity.child_name }}</span>
                </div>
                <p class="text-sm text-gray-600">{{ activity.description }}</p>
                <p class="text-xs text-gray-400 mt-1">{{ activity.timestamp }}</p>
              </div>
            </div>
          </Card>
        </div>

        <!-- Notifications non lues -->
        <div v-if="unreadCount > 0" class="mt-6">
          <div class="flex items-center justify-between mb-4">
            <h2 class="text-lg font-semibold">Notifications</h2>
            <Button variant="subtle" size="sm" @click="viewNotifications">
              Voir tout
            </Button>
          </div>
          <div class="space-y-2">
            <div
              v-for="notif in notifications.filter(n => !n.read).slice(0, 3)"
              :key="notif.id"
              class="p-3 rounded-lg border flex items-start gap-3"
              :class="getNotificationColor(notif.type)"
            >
              <AlertTriangle v-if="notif.type === 'warning'" class="w-5 h-5 flex-shrink-0" />
              <CheckCircle v-else-if="notif.type === 'success'" class="w-5 h-5 flex-shrink-0" />
              <Bell v-else class="w-5 h-5 flex-shrink-0" />
              <div class="flex-1">
                <div class="font-medium">{{ notif.title }}</div>
                <div class="text-sm">{{ notif.message }}</div>
              </div>
            </div>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>
