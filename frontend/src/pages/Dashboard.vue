<!--
  Dashboard.vue
  Page d'accueil étudiant avec progression et EC en cours.

  Utilise:
    - useStudent composable
    - ProgressBar, ECCard, StatsCard components
-->
<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Card, Badge, Button, Spinner, Alert } from 'frappe-ui'
import { useStudent } from '@/composables/useStudent'
import ProgressBar from '@/components/custom/ProgressBar.vue'
import ECCard from '@/components/custom/ECCard.vue'
import StatsCard from '@/components/custom/StatsCard.vue'

const router = useRouter()

const {
  student,
  loading,
  error,
  progressPercent,
  validatedEC,
  totalEC,
  currentYear,
  recentActivities,
  pendingPayments,
  enrollmentsByStatus,
  fetchDashboard,
} = useStudent()

onMounted(() => {
  fetchDashboard()
})

const navigateTo = (path) => {
  router.push(path)
}

const formatDate = (date) => {
  if (!date) return ''
  return new Date(date).toLocaleDateString('fr-FR', {
    day: 'numeric',
    month: 'short',
  })
}

const formatAmount = (amount) => {
  return new Intl.NumberFormat('fr-MG').format(amount) + ' Ar'
}
</script>

<template>
  <div class="min-h-screen bg-gray-50 pb-20 md:pb-6">
    <!-- Header -->
    <header class="bg-white border-b px-4 py-4 sticky top-0 z-10">
      <div class="max-w-4xl mx-auto flex justify-between items-center">
        <div>
          <h1 class="text-xl font-bold text-gray-900">
            Bonjour{{ student?.full_name ? ', ' + student.full_name.split(' ')[0] : '' }} 👋
          </h1>
          <p class="text-sm text-gray-500">Bienvenue sur votre espace</p>
        </div>
        <Badge v-if="currentYear" theme="blue" size="lg">
          {{ currentYear }}
        </Badge>
      </div>
    </header>

    <!-- Loading -->
    <div v-if="loading" class="flex justify-center items-center py-20">
      <Spinner class="w-8 h-8" />
    </div>

    <!-- Error -->
    <Alert v-else-if="error" theme="red" class="m-4">
      {{ error }}
    </Alert>

    <!-- Content -->
    <main v-else class="px-4 py-6">
      <div class="max-w-4xl mx-auto space-y-6">

        <!-- Progress Card -->
        <Card class="p-6">
          <div class="flex justify-between items-start mb-4">
            <h2 class="font-semibold text-gray-900">Ma Progression</h2>
            <Button variant="subtle" size="sm" @click="navigateTo('/progression')">
              Détails
            </Button>
          </div>
          <ProgressBar
            :value="validatedEC"
            :max="totalEC"
            label="EC validés"
            size="lg"
          />
          <div class="mt-4 grid grid-cols-3 gap-4 text-center">
            <div>
              <div class="text-2xl font-bold text-green-600">{{ validatedEC }}</div>
              <div class="text-xs text-gray-500">Validés</div>
            </div>
            <div>
              <div class="text-2xl font-bold text-yellow-600">
                {{ enrollmentsByStatus.in_progress?.length || 0 }}
              </div>
              <div class="text-xs text-gray-500">En cours</div>
            </div>
            <div>
              <div class="text-2xl font-bold text-gray-400">
                {{ totalEC - validatedEC - (enrollmentsByStatus.in_progress?.length || 0) }}
              </div>
              <div class="text-xs text-gray-500">Restants</div>
            </div>
          </div>
        </Card>

        <!-- Pending Payments Alert -->
        <Alert v-if="pendingPayments.length > 0" theme="yellow" class="flex items-center justify-between">
          <div>
            <strong>{{ pendingPayments.length }} paiement(s) en attente</strong>
            <p class="text-sm">Total: {{ formatAmount(pendingPayments.reduce((sum, p) => sum + p.amount, 0)) }}</p>
          </div>
          <Button size="sm" variant="solid" @click="navigateTo('/payment')">
            Payer
          </Button>
        </Alert>

        <!-- EC en cours -->
        <section v-if="enrollmentsByStatus.in_progress?.length > 0">
          <div class="flex justify-between items-center mb-3">
            <h2 class="font-semibold text-gray-900">EC en cours</h2>
            <Button variant="ghost" size="sm" @click="navigateTo('/courses')">
              Voir tout →
            </Button>
          </div>
          <div class="space-y-3">
            <ECCard
              v-for="enrollment in enrollmentsByStatus.in_progress.slice(0, 3)"
              :key="enrollment.ec"
              :ec="{
                id: enrollment.ec,
                title: enrollment.ec_title || enrollment.ec,
                status: 'in_progress',
                price: 0,
              }"
              compact
              @click="navigateTo(`/ec/${enrollment.ec}`)"
            />
          </div>
        </section>

        <!-- Quick Stats -->
        <div class="grid grid-cols-2 gap-4">
          <StatsCard
            icon="📚"
            label="Cours inscrits"
            :value="totalEC"
            size="sm"
            link="/courses"
          />
          <StatsCard
            icon="✅"
            label="Taux de réussite"
            :value="`${Math.round(progressPercent)}%`"
            size="sm"
          />
        </div>

        <!-- Quick Actions -->
        <section>
          <h2 class="font-semibold text-gray-900 mb-3">Actions rapides</h2>
          <div class="grid grid-cols-2 gap-4">
            <Button
              class="h-20 flex-col gap-2"
              variant="outline"
              @click="navigateTo('/catalog')"
            >
              <span class="text-2xl">🛒</span>
              <span class="text-sm">Catalogue EC</span>
            </Button>
            <Button
              class="h-20 flex-col gap-2"
              variant="outline"
              @click="navigateTo('/courses')"
            >
              <span class="text-2xl">📖</span>
              <span class="text-sm">Mes cours</span>
            </Button>
            <Button
              class="h-20 flex-col gap-2"
              variant="outline"
              @click="navigateTo('/payment')"
            >
              <span class="text-2xl">💳</span>
              <span class="text-sm">Paiements</span>
            </Button>
            <Button
              class="h-20 flex-col gap-2"
              variant="outline"
              @click="navigateTo('/profile')"
            >
              <span class="text-2xl">👤</span>
              <span class="text-sm">Mon profil</span>
            </Button>
          </div>
        </section>

        <!-- Recent Activity -->
        <section v-if="recentActivities.length > 0">
          <h2 class="font-semibold text-gray-900 mb-3">Activité récente</h2>
          <Card class="divide-y">
            <div
              v-for="activity in recentActivities"
              :key="activity.ec + activity.modified"
              class="p-3 flex justify-between items-center"
            >
              <div>
                <div class="font-medium text-sm">{{ activity.ec }}</div>
                <div class="text-xs text-gray-500">{{ formatDate(activity.modified) }}</div>
              </div>
              <Badge :theme="activity.status === 'Validated' ? 'green' : 'yellow'" size="sm">
                {{ activity.status }}
              </Badge>
            </div>
          </Card>
        </section>

      </div>
    </main>

    <!-- Bottom Navigation (Mobile) -->
    <nav class="fixed bottom-0 left-0 right-0 bg-white border-t md:hidden safe-area-bottom">
      <div class="flex justify-around py-2">
        <button
          class="flex flex-col items-center p-2 text-cntemad-primary"
          @click="navigateTo('/dashboard')"
        >
          <span class="text-xl">🏠</span>
          <span class="text-xs font-medium">Accueil</span>
        </button>
        <button
          class="flex flex-col items-center p-2 text-gray-500"
          @click="navigateTo('/courses')"
        >
          <span class="text-xl">📚</span>
          <span class="text-xs">Cours</span>
        </button>
        <button
          class="flex flex-col items-center p-2 text-gray-500"
          @click="navigateTo('/catalog')"
        >
          <span class="text-xl">🛒</span>
          <span class="text-xs">Catalogue</span>
        </button>
        <button
          class="flex flex-col items-center p-2 text-gray-500"
          @click="navigateTo('/profile')"
        >
          <span class="text-xl">👤</span>
          <span class="text-xs">Profil</span>
        </button>
      </div>
    </nav>
  </div>
</template>

<style scoped>
.safe-area-bottom {
  padding-bottom: env(safe-area-inset-bottom);
}
</style>
