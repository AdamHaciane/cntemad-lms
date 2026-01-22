<!--
  ECDetail.vue
  Page détail d'un EC avec contenu et quiz.
-->
<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Card, Badge, Button, Spinner, Alert } from 'frappe-ui'
import { createResource } from 'frappe-ui'
import ProgressBar from '@/components/custom/ProgressBar.vue'
import PaymentButton from '@/components/custom/PaymentButton.vue'

const route = useRoute()
const router = useRouter()

const ec = ref(null)
const loading = ref(true)
const error = ref(null)

// Resource
const ecResource = createResource({
  url: 'cntemad_lms.api.ec.get_ec_detail',
  auto: false,
  onSuccess(data) {
    ec.value = data
  },
  onError(err) {
    error.value = err.message
  },
})

// Computed
const isPaid = computed(() => {
  const status = ec.value?.user_status
  return status && ['paid', 'in_progress', 'validated'].includes(status)
})

const isValidated = computed(() => {
  return ec.value?.user_status === 'validated'
})

const statusConfig = computed(() => {
  const status = ec.value?.user_status
  const configs = {
    not_paid: { label: 'Non payé', theme: 'gray' },
    paid: { label: 'Payé', theme: 'blue' },
    in_progress: { label: 'En cours', theme: 'yellow' },
    validated: { label: 'Validé', theme: 'green' },
  }
  return configs[status] || configs.not_paid
})

// Methods
const fetchEC = async () => {
  loading.value = true
  error.value = null
  await ecResource.fetch({ ec_id: route.params.id })
  loading.value = false
}

const handlePay = () => {
  router.push({
    path: '/payment',
    query: { ec: route.params.id },
  })
}

const startLearning = () => {
  router.push(`/ec/${route.params.id}/learn`)
}

const startQuiz = () => {
  router.push(`/ec/${route.params.id}/quiz`)
}

const navigateTo = (path) => {
  router.push(path)
}

const formatPrice = (price) => {
  return new Intl.NumberFormat('fr-MG').format(price) + ' Ar'
}

onMounted(() => {
  fetchEC()
})
</script>

<template>
  <div class="min-h-screen bg-gray-50 pb-20 md:pb-6">
    <!-- Header -->
    <header class="bg-white border-b px-4 py-4 sticky top-0 z-10">
      <div class="max-w-4xl mx-auto flex items-center gap-4">
        <Button variant="ghost" size="sm" @click="router.back()">
          ← Retour
        </Button>
        <h1 class="text-lg font-semibold truncate flex-1">
          {{ ec?.title || 'Chargement...' }}
        </h1>
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
    <main v-else-if="ec" class="px-4 py-6">
      <div class="max-w-4xl mx-auto space-y-6">

        <!-- Hero Card -->
        <Card class="overflow-hidden">
          <!-- Image -->
          <div v-if="ec.image" class="h-48 bg-gray-200">
            <img
              :src="ec.image"
              :alt="ec.title"
              class="w-full h-full object-cover"
            />
          </div>
          <div v-else class="h-48 bg-gradient-to-br from-cntemad-primary to-blue-600 flex items-center justify-center">
            <span class="text-6xl text-white/50">📚</span>
          </div>

          <div class="p-6">
            <div class="flex justify-between items-start gap-4">
              <div>
                <h1 class="text-2xl font-bold text-gray-900">{{ ec.title }}</h1>
                <p v-if="ec.course_title" class="text-sm text-gray-500 mt-1">
                  {{ ec.course_title }} • {{ ec.year }}
                </p>
              </div>
              <Badge :theme="statusConfig.theme" size="lg">
                {{ statusConfig.label }}
              </Badge>
            </div>

            <p class="text-gray-600 mt-4">{{ ec.description }}</p>

            <!-- Meta -->
            <div class="flex flex-wrap gap-4 mt-6 text-sm text-gray-500">
              <div v-if="ec.duration_hours" class="flex items-center gap-1">
                <span>⏱️</span>
                <span>{{ ec.duration_hours }}h estimées</span>
              </div>
              <div class="flex items-center gap-1">
                <span>💰</span>
                <span class="font-semibold text-cntemad-primary">
                  {{ formatPrice(ec.price) }}
                </span>
              </div>
            </div>
          </div>
        </Card>

        <!-- Actions -->
        <Card class="p-6">
          <template v-if="!isPaid">
            <!-- Not paid: Show payment button -->
            <div class="text-center">
              <p class="text-gray-600 mb-4">
                Payez cet EC pour accéder au contenu et au quiz de validation.
              </p>
              <PaymentButton
                :amount="ec.price"
                provider="mvola"
                @pay="handlePay"
              />
            </div>
          </template>

          <template v-else-if="isValidated">
            <!-- Validated: Show success -->
            <div class="text-center">
              <div class="text-5xl mb-4">🎉</div>
              <h3 class="text-xl font-bold text-green-600">EC Validé !</h3>
              <p class="text-gray-500 mt-2">
                Félicitations, vous avez validé cet élément constitutif.
              </p>
              <Button variant="outline" class="mt-4" @click="startLearning">
                Revoir le contenu
              </Button>
            </div>
          </template>

          <template v-else>
            <!-- Paid: Show learning options -->
            <div class="space-y-4">
              <Button
                variant="solid"
                class="w-full"
                size="lg"
                @click="startLearning"
              >
                <span class="mr-2">📖</span>
                Continuer l'apprentissage
              </Button>
              <Button
                v-if="ec.quiz_id"
                variant="outline"
                class="w-full"
                @click="startQuiz"
              >
                <span class="mr-2">📝</span>
                Passer le quiz de validation
              </Button>
            </div>
          </template>
        </Card>

        <!-- Content Preview (if not paid) -->
        <Card v-if="!isPaid" class="p-6">
          <h3 class="font-semibold mb-4">Ce que vous apprendrez</h3>
          <div class="space-y-2 text-sm text-gray-600">
            <div class="flex items-start gap-2">
              <span class="text-green-500">✓</span>
              <span>Accès complet au contenu pédagogique</span>
            </div>
            <div class="flex items-start gap-2">
              <span class="text-green-500">✓</span>
              <span>Quiz de validation auto-corrigé</span>
            </div>
            <div class="flex items-start gap-2">
              <span class="text-green-500">✓</span>
              <span>Progression comptabilisée dans votre année</span>
            </div>
            <div class="flex items-start gap-2">
              <span class="text-green-500">✓</span>
              <span>Support accessible 24/7</span>
            </div>
          </div>
        </Card>

      </div>
    </main>

    <!-- Bottom Navigation (Mobile) -->
    <nav class="fixed bottom-0 left-0 right-0 bg-white border-t md:hidden safe-area-bottom">
      <div class="flex justify-around py-2">
        <button
          class="flex flex-col items-center p-2 text-gray-500"
          @click="navigateTo('/dashboard')"
        >
          <span class="text-xl">🏠</span>
          <span class="text-xs">Accueil</span>
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
