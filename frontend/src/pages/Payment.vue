<!--
  Payment.vue
  Page de paiement complète (mobile money et virement bancaire).

  Reçoit l'EC à payer via query params:
    /payment?ec=EC-001

  Étapes Mobile Money:
    1. Sélection du provider (MVola/Orange/Airtel)
    2. Saisie du numéro de téléphone
    3. Confirmation et initiation du paiement
    4. Suivi du statut (polling)
    5. Résultat (succès/échec)

  Étapes Virement Bancaire:
    1. Sélection de la banque (BFV/BNI)
    2. Affichage des coordonnées bancaires + référence unique
    3. Soumission de preuve (référence bancaire ou photo reçu)
    4. En attente de validation admin
    5. Résultat (validé/rejeté)
-->
<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { Card, Button, Input, Spinner, Dialog } from 'frappe-ui'
import { createResource } from 'frappe-ui'
import { usePayment } from '@/composables/usePayment'
import ProviderSelector from '@/components/custom/ProviderSelector.vue'
import BankPaymentForm from '@/components/custom/BankPaymentForm.vue'
import StatusBadge from '@/components/custom/StatusBadge.vue'

const router = useRouter()
const route = useRoute()

const {
  providers,
  banks,
  initiatePayment,
  initiateBankPayment,
  submitBankProof,
  checkPaymentStatus,
  startPolling,
  stopPolling,
  simulatePaymentSuccess,
  validatePhoneNumber,
  detectProvider,
  formatAmount,
  loading,
  paymentStatus,
  currentPayment,
  error,
  isProcessing,
  isCompleted,
  isFailed,
  isPendingTransfer,
  isPendingValidation,
  isBankPayment,
  reset,
} = usePayment()

// Form state
const paymentType = ref('mobile') // 'mobile' or 'bank'
const selectedProvider = ref('')
const selectedBank = ref('')
const phoneNumber = ref('')
const phoneError = ref('')
const step = ref(1) // 1: form, 2: processing/bank-info, 3: result
const showConfirmDialog = ref(false)

// EC data
const ec = ref(null)
const ecLoading = ref(false)

// Load EC details
const ecResource = createResource({
  url: 'cntemad_lms.api.ec.get_ec_detail',
  auto: false,
  onSuccess(data) {
    ec.value = data
    ecLoading.value = false
  },
  onError(err) {
    console.error('Error loading EC:', err)
    ecLoading.value = false
  },
})

// Computed
const isMobilePayment = computed(() => paymentType.value === 'mobile')
const isBankPaymentType = computed(() => paymentType.value === 'bank')

const canSubmitMobile = computed(() => {
  return (
    selectedProvider.value &&
    phoneNumber.value &&
    !phoneError.value &&
    !loading.value &&
    ec.value
  )
})

const canSubmitBank = computed(() => {
  return selectedBank.value && !loading.value && ec.value
})

const providerLabel = computed(() => {
  if (isMobilePayment.value) {
    const p = providers.value.find((p) => p.id === selectedProvider.value)
    return p?.name || selectedProvider.value
  } else {
    const b = banks.value.find((b) => b.id === selectedBank.value)
    return b?.name || selectedBank.value
  }
})

// Watch phone number for auto-detection and validation
watch(phoneNumber, (newValue) => {
  if (newValue.length >= 3 && !selectedProvider.value) {
    const detected = detectProvider(newValue)
    if (detected) {
      selectedProvider.value = detected
    }
  }

  if (selectedProvider.value && newValue) {
    const validation = validatePhoneNumber(newValue, selectedProvider.value)
    phoneError.value = validation.valid ? '' : validation.message
  } else {
    phoneError.value = ''
  }
})

// Watch provider change to re-validate phone
watch(selectedProvider, () => {
  if (phoneNumber.value) {
    const validation = validatePhoneNumber(phoneNumber.value, selectedProvider.value)
    phoneError.value = validation.valid ? '' : validation.message
  }
})

// Handle payment type change from ProviderSelector
const handleTypeChange = (type) => {
  paymentType.value = type
  selectedProvider.value = ''
  selectedBank.value = ''
  phoneNumber.value = ''
  phoneError.value = ''
}

// Handle provider/bank selection from ProviderSelector
const handleSelection = (id) => {
  if (paymentType.value === 'mobile') {
    selectedProvider.value = id
  } else {
    selectedBank.value = id
  }
}

// Methods
const loadEC = async () => {
  const ecId = route.query.ec
  if (!ecId) {
    router.push('/catalog')
    return
  }

  ecLoading.value = true
  await ecResource.fetch({ ec_id: ecId })
}

const confirmPayment = () => {
  if (isMobilePayment.value && !canSubmitMobile.value) return
  if (isBankPaymentType.value && !canSubmitBank.value) return
  showConfirmDialog.value = true
}

const handlePayment = async () => {
  showConfirmDialog.value = false
  step.value = 2

  try {
    if (isMobilePayment.value) {
      // Mobile money payment
      const result = await initiatePayment({
        ecId: ec.value.name,
        provider: selectedProvider.value,
        phoneNumber: phoneNumber.value,
      })

      if (result?.payment_id) {
        startPolling(result.payment_id, 3000, 120)
      }
    } else {
      // Bank payment
      const result = await initiateBankPayment({
        ecId: ec.value.name,
        bank: selectedBank.value,
      })

      // Bank payment doesn't need polling, stays on step 2 for info display
    }
  } catch (e) {
    step.value = 3
  }
}

const handleSubmitBankProof = async ({ proofType, proofValue }) => {
  try {
    await submitBankProof({
      paymentId: currentPayment.value.payment_id,
      proofType,
      proofValue,
    })
    step.value = 3
  } catch (e) {
    console.error('Error submitting bank proof:', e)
  }
}

const handleSimulateSuccess = async () => {
  if (currentPayment.value?.payment_id) {
    await simulatePaymentSuccess(currentPayment.value.payment_id)
    step.value = 3
  }
}

const handleRetry = () => {
  reset()
  step.value = 1
  paymentType.value = 'mobile'
  selectedProvider.value = ''
  selectedBank.value = ''
  phoneNumber.value = ''
  phoneError.value = ''
}

const goToDashboard = () => {
  router.push('/dashboard')
}

const goToEC = () => {
  if (ec.value?.name) {
    router.push(`/ec/${ec.value.name}`)
  } else {
    router.push('/catalog')
  }
}

// Watch payment status changes
watch(paymentStatus, (newStatus) => {
  // For mobile money: completed or failed goes to result
  if (isMobilePayment.value && (newStatus === 'completed' || newStatus === 'failed')) {
    stopPolling()
    step.value = 3
  }

  // For bank: pending_validation or completed/rejected goes to result
  if (isBankPaymentType.value && ['completed', 'rejected'].includes(newStatus)) {
    step.value = 3
  }
})

// Lifecycle
onMounted(() => {
  loadEC()
})

onUnmounted(() => {
  stopPolling()
})
</script>

<template>
  <div class="min-h-screen bg-gray-50 pb-20 md:pb-6">
    <!-- Header -->
    <header class="bg-white border-b px-4 py-4 sticky top-0 z-10">
      <div class="max-w-md mx-auto flex items-center justify-between">
        <div>
          <h1 class="text-xl font-bold text-gray-900">Paiement</h1>
          <p class="text-sm text-gray-500">
            {{ isMobilePayment ? 'Mobile Money' : 'Virement Bancaire' }}
          </p>
        </div>
        <Button variant="ghost" size="sm" @click="router.back()">
          Annuler
        </Button>
      </div>
    </header>

    <main class="px-4 py-6">
      <div class="max-w-md mx-auto space-y-6">
        <!-- Loading EC -->
        <div v-if="ecLoading" class="flex justify-center py-20">
          <Spinner class="w-8 h-8" />
        </div>

        <!-- EC not found -->
        <Card v-else-if="!ec" class="p-8 text-center">
          <div class="text-4xl mb-4">🔍</div>
          <h3 class="font-semibold text-gray-900">EC non trouvé</h3>
          <Button variant="outline" class="mt-4" @click="router.push('/catalog')">
            Voir le catalogue
          </Button>
        </Card>

        <!-- Step 1: Payment Form -->
        <template v-else-if="step === 1">
          <!-- Amount Card -->
          <Card class="p-6 text-center">
            <div class="text-sm text-gray-500 mb-2">Montant à payer</div>
            <div class="text-4xl font-bold text-cntemad-primary">
              {{ formatAmount(ec.price) }}
            </div>
            <div class="text-sm text-gray-500 mt-2">{{ ec.title }}</div>
          </Card>

          <!-- Payment Form -->
          <Card class="p-6">
            <form @submit.prevent="confirmPayment" class="space-y-6">
              <!-- Provider/Bank Selection -->
              <div>
                <label class="block text-sm font-medium mb-3">
                  Choisissez votre mode de paiement
                </label>
                <ProviderSelector
                  :model-value="isMobilePayment ? selectedProvider : selectedBank"
                  :providers="providers"
                  :banks="banks"
                  :show-bank-option="true"
                  @update:model-value="handleSelection"
                  @type-change="handleTypeChange"
                />
              </div>

              <!-- Phone Number (Mobile Money only) -->
              <div v-if="isMobilePayment && selectedProvider">
                <label class="block text-sm font-medium mb-2">
                  Numéro de téléphone
                </label>
                <Input
                  v-model="phoneNumber"
                  type="tel"
                  placeholder="034 XX XXX XX"
                  class="w-full"
                  :class="{ 'border-red-500': phoneError }"
                />
                <p v-if="phoneError" class="text-xs text-red-500 mt-1">
                  {{ phoneError }}
                </p>
                <p v-else class="text-xs text-gray-500 mt-1">
                  Vous recevrez une demande de confirmation sur ce numéro
                </p>
              </div>

              <!-- Submit Button -->
              <Button
                type="submit"
                variant="solid"
                class="w-full"
                theme="green"
                :disabled="isMobilePayment ? !canSubmitMobile : !canSubmitBank"
              >
                {{ isMobilePayment ? `Payer ${formatAmount(ec.price)}` : 'Continuer' }}
              </Button>
            </form>
          </Card>

          <!-- Security Info -->
          <div class="text-center text-sm text-gray-500 space-y-1">
            <p>🔒 Paiement sécurisé</p>
            <p>En cas de problème, contactez votre centre CNTEMAD</p>
          </div>
        </template>

        <!-- Step 2: Processing (Mobile) or Bank Info (Bank) -->
        <template v-else-if="step === 2">
          <!-- Mobile Money Processing -->
          <template v-if="isMobilePayment">
            <Card class="p-8 text-center">
              <Spinner class="w-16 h-16 mx-auto mb-6" />
              <h2 class="text-xl font-bold text-gray-900 mb-2">
                Paiement en cours
              </h2>
              <p class="text-gray-600 mb-4">
                Confirmez le paiement sur votre téléphone {{ providerLabel }}
              </p>
              <div class="bg-gray-100 rounded-lg p-4 mb-6">
                <div class="text-sm text-gray-500">Montant</div>
                <div class="text-2xl font-bold">{{ formatAmount(ec.price) }}</div>
                <div class="text-sm text-gray-500 mt-2">
                  Ref: {{ currentPayment?.payment_id || '...' }}
                </div>
              </div>

              <div class="text-sm text-gray-500 mb-4">
                <p>Vérification automatique du statut...</p>
                <p class="text-xs mt-1">Statut: {{ paymentStatus || 'En attente' }}</p>
              </div>

              <!-- Sandbox: Simulate button -->
              <Button
                variant="outline"
                size="sm"
                class="mt-4"
                @click="handleSimulateSuccess"
                :loading="loading"
              >
                🧪 Simuler succès (sandbox)
              </Button>
            </Card>
          </template>

          <!-- Bank Payment Form -->
          <template v-else>
            <BankPaymentForm
              :payment="currentPayment"
              :loading="loading"
              @submit-proof="handleSubmitBankProof"
              @back="handleRetry"
            />
          </template>
        </template>

        <!-- Step 3: Result -->
        <template v-else-if="step === 3">
          <!-- Success (Mobile or Bank Validated) -->
          <Card v-if="isCompleted" class="p-8 text-center">
            <div class="text-6xl mb-4">✅</div>
            <h2 class="text-xl font-bold text-green-600 mb-2">
              Paiement {{ isBankPayment ? 'validé' : 'réussi' }} !
            </h2>
            <p class="text-gray-600 mb-6">
              Vous pouvez maintenant accéder au contenu de l'EC.
            </p>

            <div class="bg-green-50 border border-green-200 rounded-lg p-4 mb-6 text-left">
              <div class="flex justify-between mb-2">
                <span class="text-gray-600">EC</span>
                <span class="font-medium">{{ ec.title }}</span>
              </div>
              <div class="flex justify-between mb-2">
                <span class="text-gray-600">Montant</span>
                <span class="font-medium">{{ formatAmount(ec.price) }}</span>
              </div>
              <div class="flex justify-between mb-2">
                <span class="text-gray-600">Mode</span>
                <span class="font-medium">{{ providerLabel }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600">Référence</span>
                <span class="font-medium text-sm">
                  {{ currentPayment?.bank_reference || currentPayment?.payment_id }}
                </span>
              </div>
            </div>

            <div class="space-y-3">
              <Button variant="solid" theme="green" class="w-full" @click="goToEC">
                Accéder au contenu
              </Button>
              <Button variant="outline" class="w-full" @click="goToDashboard">
                Retour au dashboard
              </Button>
            </div>
          </Card>

          <!-- Pending Validation (Bank) -->
          <Card v-else-if="isPendingValidation" class="p-8 text-center">
            <div class="text-6xl mb-4">⏳</div>
            <h2 class="text-xl font-bold text-amber-600 mb-2">
              En attente de validation
            </h2>
            <p class="text-gray-600 mb-6">
              Votre preuve de paiement a été soumise. Votre centre CNTEMAD la vérifiera
              et vous notifiera par email une fois validée.
            </p>

            <div class="bg-amber-50 border border-amber-200 rounded-lg p-4 mb-6 text-left">
              <div class="flex justify-between mb-2">
                <span class="text-gray-600">EC</span>
                <span class="font-medium">{{ ec.title }}</span>
              </div>
              <div class="flex justify-between mb-2">
                <span class="text-gray-600">Montant</span>
                <span class="font-medium">{{ formatAmount(ec.price) }}</span>
              </div>
              <div class="flex justify-between mb-2">
                <span class="text-gray-600">Référence</span>
                <span class="font-mono text-sm">{{ currentPayment?.bank_reference }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600">Statut</span>
                <span class="font-medium text-amber-600">En cours de vérification</span>
              </div>
            </div>

            <div class="space-y-3">
              <Button variant="solid" class="w-full" @click="goToDashboard">
                Retour au dashboard
              </Button>
            </div>
          </Card>

          <!-- Failed / Rejected -->
          <Card v-else class="p-8 text-center">
            <div class="text-6xl mb-4">❌</div>
            <h2 class="text-xl font-bold text-red-600 mb-2">
              Paiement {{ paymentStatus === 'rejected' ? 'rejeté' : 'échoué' }}
            </h2>
            <p class="text-gray-600 mb-4">
              {{ error || currentPayment?.failure_reason || 'Une erreur est survenue' }}
            </p>

            <div class="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
              <p class="text-sm text-red-700">
                <template v-if="isBankPayment">
                  Votre preuve de paiement a été rejetée.
                  Contactez votre centre CNTEMAD pour plus d'informations.
                </template>
                <template v-else>
                  Vérifiez votre solde {{ providerLabel }} et réessayez.
                  Si le problème persiste, contactez votre centre CNTEMAD.
                </template>
              </p>
            </div>

            <div class="space-y-3">
              <Button variant="solid" class="w-full" @click="handleRetry">
                Réessayer
              </Button>
              <Button variant="outline" class="w-full" @click="goToDashboard">
                Retour au dashboard
              </Button>
            </div>
          </Card>
        </template>
      </div>
    </main>

    <!-- Confirm Dialog (Mobile Money) -->
    <Dialog v-model="showConfirmDialog" :options="{ title: 'Confirmer le paiement' }">
      <template #body-content>
        <div class="space-y-4">
          <p class="text-gray-600">
            <template v-if="isMobilePayment">
              Vous allez payer <strong>{{ formatAmount(ec?.price || 0) }}</strong> via
              <strong>{{ providerLabel }}</strong>.
            </template>
            <template v-else>
              Vous allez initier un virement bancaire de <strong>{{ formatAmount(ec?.price || 0) }}</strong>
              vers le compte <strong>{{ providerLabel }}</strong>.
            </template>
          </p>
          <p v-if="isMobilePayment" class="text-gray-600">
            Une demande de confirmation sera envoyée au
            <strong>{{ phoneNumber }}</strong>.
          </p>
          <div class="bg-yellow-50 border border-yellow-200 rounded-lg p-3">
            <p class="text-sm text-yellow-800">
              <template v-if="isMobilePayment">
                ⚠️ Gardez votre téléphone à portée de main pour confirmer le paiement.
              </template>
              <template v-else>
                ℹ️ Vous recevrez les coordonnées bancaires et une référence unique à mentionner dans votre virement.
              </template>
            </p>
          </div>
        </div>
      </template>
      <template #actions>
        <Button variant="outline" @click="showConfirmDialog = false">
          Annuler
        </Button>
        <Button variant="solid" theme="green" @click="handlePayment" :loading="loading">
          Confirmer
        </Button>
      </template>
    </Dialog>
  </div>
</template>
