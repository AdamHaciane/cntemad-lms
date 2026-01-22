<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="bg-white border-b sticky top-0 z-10">
      <div class="px-4 py-4">
        <div class="flex items-center gap-3">
          <router-link to="/admin/dashboard">
            <Button variant="ghost" class="p-2">
              <ArrowLeft class="w-5 h-5" />
            </Button>
          </router-link>
          <div class="flex-1">
            <h1 class="text-xl font-bold text-gray-900">Paiements</h1>
            <p class="text-sm text-gray-500">
              {{ paymentsTotal }} transaction{{ paymentsTotal > 1 ? 's' : '' }}
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Tabs: All Payments / Pending Bank Validation -->
    <div class="bg-white border-b">
      <div class="px-4">
        <div class="flex gap-4">
          <button
            class="py-3 px-1 border-b-2 text-sm font-medium transition-colors"
            :class="activeTab === 'all'
              ? 'border-blue-600 text-blue-600'
              : 'border-transparent text-gray-500 hover:text-gray-700'"
            @click="activeTab = 'all'"
          >
            Tous les paiements
          </button>
          <button
            class="py-3 px-1 border-b-2 text-sm font-medium transition-colors flex items-center gap-2"
            :class="activeTab === 'bank'
              ? 'border-blue-600 text-blue-600'
              : 'border-transparent text-gray-500 hover:text-gray-700'"
            @click="activeTab = 'bank'"
          >
            Virements à valider
            <Badge v-if="pendingBankCount > 0" theme="orange" class="text-xs">
              {{ pendingBankCount }}
            </Badge>
          </button>
        </div>
      </div>
    </div>

    <!-- Tab: All Payments -->
    <template v-if="activeTab === 'all'">
      <!-- Stats rapides -->
      <div class="p-4 grid grid-cols-3 gap-3">
        <Card class="p-3 text-center">
          <p class="text-2xl font-bold text-green-600">
            {{ paymentStats.success?.count || 0 }}
          </p>
          <p class="text-xs text-gray-500">Réussis</p>
        </Card>
        <Card class="p-3 text-center">
          <p class="text-2xl font-bold text-amber-600">
            {{ paymentStats.pending?.count || 0 }}
          </p>
          <p class="text-xs text-gray-500">En attente</p>
        </Card>
        <Card class="p-3 text-center">
          <p class="text-2xl font-bold text-red-600">
            {{ paymentStats.failed?.count || 0 }}
          </p>
          <p class="text-xs text-gray-500">Échoués</p>
        </Card>
      </div>

      <!-- Filtres -->
      <div class="px-4 pb-4 bg-white border-b space-y-3">
        <!-- Recherche -->
        <div class="relative">
          <Search class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
          <Input
            v-model="filters.search"
            placeholder="Rechercher par référence, étudiant..."
            class="pl-10"
            @input="debouncedSearch"
          />
        </div>

        <!-- Filtres ligne -->
        <div class="flex gap-2 overflow-x-auto pb-1">
          <Select
            v-model="filters.status"
            :options="statusOptions"
            placeholder="Statut"
            class="min-w-[120px]"
            @update:modelValue="applyFilters"
          />
          <Select
            v-model="filters.provider"
            :options="providerOptions"
            placeholder="Provider"
            class="min-w-[120px]"
            @update:modelValue="applyFilters"
          />
        </div>

        <!-- Date range -->
        <DateRangePicker
          v-model:start="filters.date_from"
          v-model:end="filters.date_to"
          @change="applyFilters"
        />

        <!-- Tags filtres actifs -->
        <div v-if="hasActiveFilters" class="flex flex-wrap gap-2">
          <Badge
            v-if="filters.status"
            variant="subtle"
            :theme="getStatusTheme(filters.status)"
            class="cursor-pointer"
            @click="clearFilter('status')"
          >
            {{ getStatusLabel(filters.status) }}
            <X class="w-3 h-3 ml-1" />
          </Badge>
          <Badge
            v-if="filters.provider"
            variant="subtle"
            theme="blue"
            class="cursor-pointer"
            @click="clearFilter('provider')"
          >
            {{ filters.provider }}
            <X class="w-3 h-3 ml-1" />
          </Badge>
          <button
            class="text-xs text-blue-600 underline"
            @click="clearAllFilters"
          >
            Effacer tout
          </button>
        </div>
      </div>

      <!-- Liste paiements -->
      <div class="p-4">
        <!-- Loading -->
        <div v-if="loading" class="flex justify-center py-8">
          <Spinner class="w-8 h-8" />
        </div>

        <!-- Liste -->
        <div v-else-if="payments.length > 0" class="space-y-3">
          <Card
            v-for="payment in payments"
            :key="payment.name"
            class="p-4"
            @click="openPaymentDetail(payment)"
          >
            <div class="flex items-start justify-between">
              <div class="flex-1">
                <div class="flex items-center gap-2">
                  <component
                    :is="getProviderIcon(payment.provider)"
                    class="w-5 h-5"
                    :class="getProviderColor(payment.provider)"
                  />
                  <span class="font-medium text-gray-900">
                    {{ formatAmount(payment.amount) }}
                  </span>
                </div>
                <p class="text-sm text-gray-500 mt-1">
                  {{ payment.student_name || payment.student }}
                </p>
                <p class="text-xs text-gray-400 mt-1">
                  {{ payment.reference || payment.name }} • {{ formatDate(payment.creation) }}
                </p>
              </div>
              <Badge :theme="getStatusTheme(payment.status)">
                {{ getStatusLabel(payment.status) }}
              </Badge>
            </div>
          </Card>

          <!-- Pagination -->
          <div v-if="hasMore" class="pt-4">
            <Button
              variant="outline"
              class="w-full"
              @click="loadMore"
              :loading="loadingMore"
            >
              Charger plus
            </Button>
          </div>
        </div>

        <!-- Vide -->
        <div v-else class="text-center py-12">
          <CreditCard class="w-12 h-12 text-gray-300 mx-auto mb-4" />
          <p class="text-gray-500">Aucun paiement trouvé</p>
          <p class="text-sm text-gray-400 mt-1">
            Essayez de modifier vos filtres
          </p>
        </div>
      </div>
    </template>

    <!-- Tab: Pending Bank Payments -->
    <template v-else-if="activeTab === 'bank'">
      <div class="p-4">
        <!-- Info banner -->
        <div class="mb-4 p-4 bg-blue-50 rounded-lg text-sm text-blue-800 flex items-start gap-3">
          <Building2 class="w-5 h-5 flex-shrink-0 mt-0.5" />
          <div>
            <p class="font-medium">Virements bancaires en attente de validation</p>
            <p class="mt-1 text-blue-600">
              Vérifiez les preuves de paiement soumises par les étudiants et validez ou rejetez les virements.
            </p>
          </div>
        </div>

        <!-- Loading -->
        <div v-if="loadingBank" class="flex justify-center py-8">
          <Spinner class="w-8 h-8" />
        </div>

        <!-- Liste virements -->
        <div v-else-if="pendingBankPayments.length > 0" class="space-y-4">
          <Card
            v-for="payment in pendingBankPayments"
            :key="payment.name"
            class="p-4"
          >
            <div class="flex items-start justify-between mb-4">
              <div class="flex-1">
                <div class="flex items-center gap-2">
                  <Building2 class="w-5 h-5 text-blue-600" />
                  <span class="font-medium text-gray-900">
                    {{ formatAmount(payment.amount) }}
                  </span>
                  <Badge theme="orange">En attente</Badge>
                </div>
                <p class="text-sm text-gray-500 mt-1">
                  {{ payment.student_name }}
                </p>
                <p class="text-xs text-gray-400 mt-1">
                  {{ payment.ec_title || payment.ec }}
                </p>
              </div>
              <div class="text-right">
                <div class="text-xs text-gray-500">{{ payment.bank_name }}</div>
                <div class="font-mono text-sm text-gray-700">{{ payment.bank_reference }}</div>
              </div>
            </div>

            <!-- Proof details -->
            <div class="bg-gray-50 rounded-lg p-3 mb-4">
              <div class="text-xs text-gray-500 mb-1">Preuve soumise</div>
              <div class="flex items-center gap-2">
                <Badge
                  :theme="payment.proof_type === 'reference' ? 'blue' : 'purple'"
                  class="text-xs"
                >
                  {{ payment.proof_type === 'reference' ? 'Référence bancaire' : 'Photo reçu' }}
                </Badge>
                <span class="font-mono text-sm truncate max-w-[200px]">
                  {{ payment.proof_value }}
                </span>
              </div>
              <div class="text-xs text-gray-400 mt-1">
                Soumis le {{ formatDateTime(payment.proof_submitted_at) }}
              </div>
            </div>

            <!-- Actions -->
            <div class="flex gap-2">
              <Button
                variant="solid"
                theme="green"
                size="sm"
                class="flex-1"
                @click="openValidateDialog(payment, true)"
              >
                <Check class="w-4 h-4 mr-1" />
                Valider
              </Button>
              <Button
                variant="outline"
                size="sm"
                class="flex-1 text-red-600 hover:bg-red-50"
                @click="openValidateDialog(payment, false)"
              >
                <X class="w-4 h-4 mr-1" />
                Rejeter
              </Button>
            </div>
          </Card>
        </div>

        <!-- Vide -->
        <div v-else class="text-center py-12">
          <CheckCircle class="w-12 h-12 text-green-300 mx-auto mb-4" />
          <p class="text-gray-500">Aucun virement en attente</p>
          <p class="text-sm text-gray-400 mt-1">
            Tous les virements ont été traités
          </p>
        </div>
      </div>
    </template>

    <!-- Dialog détail paiement -->
    <Dialog v-model="showPaymentDialog" :options="{ title: 'Détail paiement' }">
      <template #body-content>
        <div v-if="selectedPayment" class="space-y-4">
          <!-- Montant -->
          <div class="text-center py-4 bg-gray-50 rounded-lg">
            <p class="text-3xl font-bold text-gray-900">
              {{ formatAmount(selectedPayment.amount) }}
            </p>
            <Badge :theme="getStatusTheme(selectedPayment.status)" class="mt-2">
              {{ getStatusLabel(selectedPayment.status) }}
            </Badge>
          </div>

          <!-- Détails -->
          <div class="divide-y">
            <div class="py-3 flex justify-between">
              <span class="text-gray-500">Référence</span>
              <span class="text-gray-900 font-mono text-sm">
                {{ selectedPayment.bank_reference || selectedPayment.reference || selectedPayment.name }}
              </span>
            </div>
            <div class="py-3 flex justify-between">
              <span class="text-gray-500">Provider</span>
              <div class="flex items-center gap-2">
                <component
                  :is="getProviderIcon(selectedPayment.provider)"
                  class="w-4 h-4"
                  :class="getProviderColor(selectedPayment.provider)"
                />
                <span class="text-gray-900">{{ getProviderLabel(selectedPayment.provider) }}</span>
              </div>
            </div>
            <div v-if="selectedPayment.phone" class="py-3 flex justify-between">
              <span class="text-gray-500">Téléphone</span>
              <span class="text-gray-900">{{ selectedPayment.phone }}</span>
            </div>
            <div class="py-3 flex justify-between">
              <span class="text-gray-500">Étudiant</span>
              <span class="text-gray-900">
                {{ selectedPayment.student_name || selectedPayment.student }}
              </span>
            </div>
            <div class="py-3 flex justify-between">
              <span class="text-gray-500">EC</span>
              <span class="text-gray-900">
                {{ selectedPayment.ec_title || selectedPayment.ec || '-' }}
              </span>
            </div>
            <div class="py-3 flex justify-between">
              <span class="text-gray-500">Date</span>
              <span class="text-gray-900">
                {{ formatDateTime(selectedPayment.creation) }}
              </span>
            </div>
            <div v-if="selectedPayment.completed_at" class="py-3 flex justify-between">
              <span class="text-gray-500">Complété le</span>
              <span class="text-gray-900">
                {{ formatDateTime(selectedPayment.completed_at) }}
              </span>
            </div>
            <div v-if="selectedPayment.transaction_id" class="py-3 flex justify-between">
              <span class="text-gray-500">Transaction ID</span>
              <span class="text-gray-900 font-mono text-sm">
                {{ selectedPayment.transaction_id }}
              </span>
            </div>
            <!-- Bank specific -->
            <template v-if="selectedPayment.provider?.startsWith('bank_')">
              <div v-if="selectedPayment.proof_type" class="py-3 flex justify-between">
                <span class="text-gray-500">Type de preuve</span>
                <span class="text-gray-900">
                  {{ selectedPayment.proof_type === 'reference' ? 'Référence bancaire' : 'Photo reçu' }}
                </span>
              </div>
              <div v-if="selectedPayment.proof_value" class="py-3 flex justify-between">
                <span class="text-gray-500">Preuve</span>
                <span class="text-gray-900 font-mono text-sm truncate max-w-[200px]">
                  {{ selectedPayment.proof_value }}
                </span>
              </div>
            </template>
          </div>
        </div>
      </template>
    </Dialog>

    <!-- Dialog validation virement -->
    <Dialog v-model="showValidateDialog" :options="{ title: isApproving ? 'Valider le virement' : 'Rejeter le virement' }">
      <template #body-content>
        <div v-if="validatingPayment" class="space-y-4">
          <div class="p-4 rounded-lg" :class="isApproving ? 'bg-green-50' : 'bg-red-50'">
            <div class="text-center">
              <p class="text-2xl font-bold" :class="isApproving ? 'text-green-600' : 'text-red-600'">
                {{ formatAmount(validatingPayment.amount) }}
              </p>
              <p class="text-sm mt-1" :class="isApproving ? 'text-green-700' : 'text-red-700'">
                {{ validatingPayment.student_name }}
              </p>
            </div>
          </div>

          <div class="text-sm space-y-2">
            <div class="flex justify-between">
              <span class="text-gray-500">EC</span>
              <span>{{ validatingPayment.ec_title }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-500">Référence</span>
              <span class="font-mono">{{ validatingPayment.bank_reference }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-500">Preuve</span>
              <span>{{ validatingPayment.proof_value }}</span>
            </div>
          </div>

          <!-- Note (required for rejection) -->
          <div>
            <label class="block text-sm font-medium mb-2">
              {{ isApproving ? 'Note (optionnelle)' : 'Raison du rejet (requise)' }}
            </label>
            <Input
              v-model="validationNote"
              :placeholder="isApproving ? 'Commentaire optionnel...' : 'Expliquez pourquoi ce paiement est rejeté...'"
              class="w-full"
            />
          </div>

          <div v-if="validationError" class="p-3 bg-red-50 text-red-700 rounded-lg text-sm">
            {{ validationError }}
          </div>
        </div>
      </template>
      <template #actions>
        <Button variant="outline" @click="showValidateDialog = false">
          Annuler
        </Button>
        <Button
          :variant="isApproving ? 'solid' : 'outline'"
          :theme="isApproving ? 'green' : undefined"
          :class="!isApproving ? 'text-red-600 hover:bg-red-50' : ''"
          @click="confirmValidation"
          :loading="validating"
          :disabled="!isApproving && !validationNote"
        >
          {{ isApproving ? 'Valider' : 'Rejeter' }}
        </Button>
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { Button, Card, Input, Select, Badge, Dialog, Spinner } from 'frappe-ui'
import { createResource } from 'frappe-ui'
import {
  ArrowLeft, Search, CreditCard, X, Smartphone, Building2,
  Check, CheckCircle
} from 'lucide-vue-next'
import DateRangePicker from '@/components/custom/DateRangePicker.vue'
import { useCenter } from '@/composables/useCenter'

const {
  payments,
  paymentsTotal,
  paymentStats,
  loading,
  fetchPayments,
  formatAmount
} = useCenter()

const activeTab = ref('all')
const filters = ref({
  search: '',
  status: '',
  provider: '',
  date_from: '',
  date_to: ''
})

const showPaymentDialog = ref(false)
const selectedPayment = ref(null)
const loadingMore = ref(false)
const currentOffset = ref(0)
const pageSize = 20

// Bank validation state
const pendingBankPayments = ref([])
const pendingBankCount = ref(0)
const loadingBank = ref(false)
const showValidateDialog = ref(false)
const validatingPayment = ref(null)
const isApproving = ref(true)
const validationNote = ref('')
const validationError = ref('')
const validating = ref(false)

const statusOptions = [
  { label: 'Tous', value: '' },
  { label: 'Réussi', value: 'completed' },
  { label: 'En attente', value: 'pending' },
  { label: 'En cours', value: 'processing' },
  { label: 'Virement en attente', value: 'pending_transfer' },
  { label: 'Validation en attente', value: 'pending_validation' },
  { label: 'Échoué', value: 'failed' },
  { label: 'Rejeté', value: 'rejected' }
]

const providerOptions = [
  { label: 'Tous', value: '' },
  { label: 'MVola', value: 'mvola' },
  { label: 'Orange Money', value: 'orange_money' },
  { label: 'Airtel Money', value: 'airtel_money' },
  { label: 'Virement BFV', value: 'bank_bfv' },
  { label: 'Virement BNI', value: 'bank_bni' }
]

const hasActiveFilters = computed(() => {
  return filters.value.status ||
    filters.value.provider ||
    filters.value.search ||
    filters.value.date_from ||
    filters.value.date_to
})

const hasMore = computed(() => {
  return payments.value.length < paymentsTotal.value
})

// Resources
const pendingBankResource = createResource({
  url: 'cntemad_lms.api.payment.get_pending_bank_payments',
  auto: false,
  onSuccess(data) {
    pendingBankPayments.value = data.payments || []
    pendingBankCount.value = data.total || 0
    loadingBank.value = false
  },
  onError() {
    loadingBank.value = false
  }
})

const validateBankResource = createResource({
  url: 'cntemad_lms.api.payment.validate_bank_payment',
  auto: false,
})

onMounted(() => {
  loadPayments()
  loadPendingBankPayments()
})

// Watch tab change
watch(activeTab, (newTab) => {
  if (newTab === 'bank') {
    loadPendingBankPayments()
  }
})

const loadPayments = async () => {
  currentOffset.value = 0
  await fetchPayments({
    ...filters.value,
    limit: pageSize,
    offset: 0
  })
}

const loadMore = async () => {
  loadingMore.value = true
  currentOffset.value += pageSize
  try {
    await fetchPayments({
      ...filters.value,
      limit: pageSize,
      offset: currentOffset.value,
      append: true
    })
  } finally {
    loadingMore.value = false
  }
}

const loadPendingBankPayments = async () => {
  loadingBank.value = true
  await pendingBankResource.fetch({ limit: 50, offset: 0 })
}

let searchTimeout = null
const debouncedSearch = () => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    loadPayments()
  }, 300)
}

const applyFilters = () => {
  loadPayments()
}

const clearFilter = (key) => {
  filters.value[key] = ''
  loadPayments()
}

const clearAllFilters = () => {
  filters.value = {
    search: '',
    status: '',
    provider: '',
    date_from: '',
    date_to: ''
  }
  loadPayments()
}

const openPaymentDetail = (payment) => {
  selectedPayment.value = payment
  showPaymentDialog.value = true
}

const openValidateDialog = (payment, approve) => {
  validatingPayment.value = payment
  isApproving.value = approve
  validationNote.value = ''
  validationError.value = ''
  showValidateDialog.value = true
}

const confirmValidation = async () => {
  if (!isApproving.value && !validationNote.value) {
    validationError.value = 'Une raison est requise pour le rejet'
    return
  }

  validating.value = true
  validationError.value = ''

  try {
    await validateBankResource.fetch({
      payment_id: validatingPayment.value.name,
      approved: isApproving.value,
      note: validationNote.value
    })

    showValidateDialog.value = false

    // Refresh the list
    await loadPendingBankPayments()
    await loadPayments()
  } catch (e) {
    validationError.value = e.message || 'Erreur lors de la validation'
  } finally {
    validating.value = false
  }
}

const getStatusLabel = (status) => {
  const labels = {
    completed: 'Réussi',
    pending: 'En attente',
    failed: 'Échoué',
    processing: 'En cours',
    pending_transfer: 'Virement en attente',
    pending_validation: 'À valider',
    rejected: 'Rejeté'
  }
  return labels[status?.toLowerCase()?.replace(' ', '_')] || status
}

const getStatusTheme = (status) => {
  const themes = {
    completed: 'green',
    pending: 'orange',
    failed: 'red',
    processing: 'blue',
    pending_transfer: 'orange',
    pending_validation: 'orange',
    rejected: 'red'
  }
  return themes[status?.toLowerCase()?.replace(' ', '_')] || 'gray'
}

const getProviderIcon = (provider) => {
  if (provider?.startsWith('bank_')) {
    return Building2
  }
  return Smartphone
}

const getProviderColor = (provider) => {
  const colors = {
    mvola: 'text-yellow-600',
    orange_money: 'text-orange-600',
    airtel_money: 'text-red-600',
    bank_bfv: 'text-blue-600',
    bank_bni: 'text-emerald-600'
  }
  return colors[provider?.toLowerCase()] || 'text-gray-600'
}

const getProviderLabel = (provider) => {
  const labels = {
    mvola: 'MVola',
    orange_money: 'Orange Money',
    airtel_money: 'Airtel Money',
    bank_bfv: 'Virement BFV-SG',
    bank_bni: 'Virement BNI'
  }
  return labels[provider?.toLowerCase()] || provider
}

const formatDate = (date) => {
  if (!date) return '-'
  return new Date(date).toLocaleDateString('fr-FR')
}

const formatDateTime = (date) => {
  if (!date) return '-'
  return new Date(date).toLocaleString('fr-FR')
}
</script>
