/**
 * Composable pour gérer les paiements mobile money et virements bancaires.
 *
 * Usage:
 *   const {
 *     // Mobile money
 *     initiatePayment,
 *     checkPaymentStatus,
 *     simulatePaymentSuccess,
 *     getPaymentHistory,
 *     // Bank transfer
 *     initiateBankPayment,
 *     submitBankProof,
 *     getBanks,
 *     // State
 *     loading,
 *     paymentStatus,
 *     currentPayment,
 *     error
 *   } = usePayment()
 */
import { ref, computed } from 'vue'
import { createResource } from 'frappe-ui'

// Mobile money provider configurations
const PROVIDERS = [
  {
    id: 'mvola',
    name: 'MVola',
    logo: '/assets/cntemad_lms/images/mvola.png',
    prefixes: ['034', '038'],
    color: '#FFD700',
  },
  {
    id: 'orange_money',
    name: 'Orange Money',
    logo: '/assets/cntemad_lms/images/orange.png',
    prefixes: ['032', '037'],
    color: '#FF6600',
  },
  {
    id: 'airtel_money',
    name: 'Airtel Money',
    logo: '/assets/cntemad_lms/images/airtel.png',
    prefixes: ['033'],
    color: '#E4002B',
  },
]

// Bank configurations
const BANKS = [
  {
    id: 'bfv',
    name: 'BFV-SG',
    color: '#1E40AF',
  },
  {
    id: 'bni',
    name: 'BNI Madagascar',
    color: '#059669',
  },
]

export function usePayment() {
  const loading = ref(false)
  const paymentStatus = ref(null)
  const currentPayment = ref(null)
  const error = ref(null)
  const pollingInterval = ref(null)

  // Payment initiation resource
  const initiateResource = createResource({
    url: 'cntemad_lms.api.payment.initiate_payment',
    auto: false,
    onSuccess(data) {
      currentPayment.value = data
      paymentStatus.value = data.status
    },
    onError(err) {
      error.value = err.message || 'Erreur lors du paiement'
      paymentStatus.value = 'failed'
    },
  })

  // Status check resource
  const statusResource = createResource({
    url: 'cntemad_lms.api.payment.check_payment_status',
    auto: false,
    onSuccess(data) {
      currentPayment.value = data
      paymentStatus.value = data.status
    },
  })

  // Payment history resource
  const historyResource = createResource({
    url: 'cntemad_lms.api.payment.get_payment_history',
    auto: false,
  })

  // Simulate success (sandbox only)
  const simulateResource = createResource({
    url: 'cntemad_lms.api.payment.simulate_payment_success',
    auto: false,
    onSuccess(data) {
      currentPayment.value = data
      paymentStatus.value = 'completed'
    },
  })

  // Bank payment initiation resource
  const bankInitiateResource = createResource({
    url: 'cntemad_lms.api.payment.initiate_bank_payment',
    auto: false,
    onSuccess(data) {
      currentPayment.value = data
      paymentStatus.value = data.status
    },
    onError(err) {
      error.value = err.message || 'Erreur lors de l\'initiation du virement'
      paymentStatus.value = 'failed'
    },
  })

  // Bank proof submission resource
  const bankProofResource = createResource({
    url: 'cntemad_lms.api.payment.submit_bank_proof',
    auto: false,
    onSuccess(data) {
      currentPayment.value = { ...currentPayment.value, ...data }
      paymentStatus.value = data.status
    },
    onError(err) {
      error.value = err.message || 'Erreur lors de la soumission de la preuve'
    },
  })

  // Get banks resource
  const banksResource = createResource({
    url: 'cntemad_lms.api.payment.get_banks',
    auto: false,
  })

  // Computed
  const providers = computed(() => PROVIDERS)
  const banks = computed(() => BANKS)

  const isProcessing = computed(() =>
    ['pending', 'processing'].includes(paymentStatus.value)
  )

  const isCompleted = computed(() => paymentStatus.value === 'completed')

  const isFailed = computed(() =>
    ['failed', 'rejected'].includes(paymentStatus.value)
  )

  // Bank payment statuses
  const isPendingTransfer = computed(() =>
    paymentStatus.value === 'pending_transfer'
  )

  const isPendingValidation = computed(() =>
    paymentStatus.value === 'pending_validation'
  )

  const isBankPayment = computed(() =>
    currentPayment.value?.is_bank_payment ||
    currentPayment.value?.provider?.startsWith('bank_')
  )

  // Methods
  const initiatePayment = async ({ ecId, provider, phoneNumber }) => {
    loading.value = true
    error.value = null
    paymentStatus.value = 'pending'

    try {
      await initiateResource.fetch({
        ec_id: ecId,
        provider,
        phone_number: phoneNumber,
      })
      return currentPayment.value
    } catch (e) {
      error.value = e.message || 'Erreur lors du paiement'
      paymentStatus.value = 'failed'
      throw e
    } finally {
      loading.value = false
    }
  }

  const checkPaymentStatus = async (paymentId) => {
    if (!paymentId) return null

    try {
      await statusResource.fetch({ payment_id: paymentId })
      return currentPayment.value
    } catch (e) {
      console.error('Error checking payment status:', e)
      return null
    }
  }

  const startPolling = (paymentId, intervalMs = 5000, maxAttempts = 60) => {
    let attempts = 0

    stopPolling() // Clear any existing polling

    pollingInterval.value = setInterval(async () => {
      attempts++

      const status = await checkPaymentStatus(paymentId)

      if (status?.status === 'completed' || status?.status === 'failed') {
        stopPolling()
      }

      if (attempts >= maxAttempts) {
        stopPolling()
        error.value = 'Délai de vérification dépassé'
      }
    }, intervalMs)
  }

  const stopPolling = () => {
    if (pollingInterval.value) {
      clearInterval(pollingInterval.value)
      pollingInterval.value = null
    }
  }

  const simulatePaymentSuccess = async (paymentId) => {
    loading.value = true
    try {
      await simulateResource.fetch({ payment_id: paymentId })
      return currentPayment.value
    } finally {
      loading.value = false
    }
  }

  const getPaymentHistory = async (limit = 20, offset = 0) => {
    try {
      await historyResource.fetch({ limit, offset })
      return historyResource.data
    } catch (e) {
      console.error('Error fetching payment history:', e)
      return { payments: [], total: 0 }
    }
  }

  // Bank payment methods
  const getBanks = async () => {
    try {
      await banksResource.fetch()
      return banksResource.data
    } catch (e) {
      console.error('Error fetching banks:', e)
      return BANKS // Fallback to local config
    }
  }

  const initiateBankPayment = async ({ ecId, bank }) => {
    loading.value = true
    error.value = null
    paymentStatus.value = 'pending_transfer'

    try {
      await bankInitiateResource.fetch({
        ec_id: ecId,
        bank,
      })
      return currentPayment.value
    } catch (e) {
      error.value = e.message || 'Erreur lors de l\'initiation du virement'
      paymentStatus.value = 'failed'
      throw e
    } finally {
      loading.value = false
    }
  }

  const submitBankProof = async ({ paymentId, proofType, proofValue }) => {
    loading.value = true
    error.value = null

    try {
      await bankProofResource.fetch({
        payment_id: paymentId,
        proof_type: proofType,
        proof_value: proofValue,
      })
      return currentPayment.value
    } catch (e) {
      error.value = e.message || 'Erreur lors de la soumission de la preuve'
      throw e
    } finally {
      loading.value = false
    }
  }

  const getBankLabel = (bankId) => {
    const bank = BANKS.find((b) => b.id === bankId)
    return bank?.name || bankId
  }

  const detectProvider = (phoneNumber) => {
    const cleaned = phoneNumber.replace(/[\s\-\.]/g, '')
    const prefix = cleaned.substring(0, 3)

    for (const provider of PROVIDERS) {
      if (provider.prefixes.includes(prefix)) {
        return provider.id
      }
    }
    return null
  }

  const validatePhoneNumber = (phoneNumber, providerId) => {
    const cleaned = phoneNumber.replace(/[\s\-\.]/g, '')

    // Check length (10 digits for Madagascar)
    if (cleaned.length !== 10) {
      return { valid: false, message: 'Le numéro doit contenir 10 chiffres' }
    }

    // Check prefix matches provider
    const provider = PROVIDERS.find((p) => p.id === providerId)
    if (!provider) {
      return { valid: false, message: 'Provider invalide' }
    }

    const prefix = cleaned.substring(0, 3)
    if (!provider.prefixes.includes(prefix)) {
      return {
        valid: false,
        message: `Numéro invalide pour ${provider.name}. Préfixes: ${provider.prefixes.join(', ')}`,
      }
    }

    return { valid: true, message: '' }
  }

  const formatAmount = (amount) => {
    return new Intl.NumberFormat('fr-MG', {
      style: 'decimal',
      minimumFractionDigits: 0,
    }).format(amount) + ' Ar'
  }

  const reset = () => {
    loading.value = false
    paymentStatus.value = null
    currentPayment.value = null
    error.value = null
    stopPolling()
  }

  return {
    // State
    loading,
    paymentStatus,
    currentPayment,
    error,

    // Computed
    providers,
    banks,
    isProcessing,
    isCompleted,
    isFailed,
    isPendingTransfer,
    isPendingValidation,
    isBankPayment,

    // Mobile money methods
    initiatePayment,
    checkPaymentStatus,
    startPolling,
    stopPolling,
    simulatePaymentSuccess,
    getPaymentHistory,
    detectProvider,
    validatePhoneNumber,
    formatAmount,
    reset,

    // Bank payment methods
    getBanks,
    initiateBankPayment,
    submitBankProof,
    getBankLabel,

    // Resources (for advanced usage)
    initiateResource,
    statusResource,
    historyResource,
    bankInitiateResource,
    bankProofResource,
    banksResource,
  }
}
