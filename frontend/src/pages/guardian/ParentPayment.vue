<!--
  ParentPayment.vue
  Page de paiement d'EC par un parent pour son enfant.
  Supporte Mobile Money et Virement Bancaire.
-->
<script setup>
import { ref, computed, onMounted } from 'vue'
import { Card, Button, Badge, Dialog, Input, Spinner } from 'frappe-ui'
import {
  ArrowLeft, CreditCard, BookOpen, CheckCircle, Clock,
  Phone, AlertTriangle, User, Building2
} from 'lucide-vue-next'
import { useGuardian } from '@/composables/useGuardian'
import { useRoute, useRouter } from 'vue-router'
import ProviderSelector from '@/components/custom/ProviderSelector.vue'
import BankPaymentForm from '@/components/custom/BankPaymentForm.vue'

const route = useRoute()
const router = useRouter()

const {
  children,
  unpaidEcs,
  loading,
  paying,
  error,
  fetchChildren,
  fetchUnpaidEcs,
  initiatePayment,
  initiateBankPayment,
  submitBankProof,
  formatAmount,
  getProviderLabel,
} = useGuardian()

const studentId = computed(() => route.params.id)
const selectedChild = ref(null)
const selectedEc = ref(null)

// Payment state
const paymentType = ref('mobile') // 'mobile' or 'bank'
const selectedProvider = ref('')
const selectedBank = ref('')
const phoneNumber = ref('')
const step = ref(1) // 1: choisir enfant/EC, 2: paiement mobile, 3: bank info, 4: confirmation
const showConfirmDialog = ref(false)
const paymentResult = ref(null)
const paymentError = ref(null)

const providers = [
  { id: 'mvola', name: 'MVola', prefixes: ['034', '038'], color: 'bg-yellow-500' },
  { id: 'orange_money', name: 'Orange Money', prefixes: ['032', '037'], color: 'bg-orange-500' },
  { id: 'airtel_money', name: 'Airtel Money', prefixes: ['033'], color: 'bg-red-500' },
]

const banks = [
  { id: 'bfv', name: 'BFV-SG', description: 'Société Générale', color: 'bg-blue-700' },
  { id: 'bni', name: 'BNI Madagascar', description: 'Banque Nationale', color: 'bg-emerald-600' },
]

onMounted(async () => {
  await fetchChildren()
  if (studentId.value) {
    selectedChild.value = children.value.find(c => c.id === studentId.value)
    if (selectedChild.value) {
      await fetchUnpaidEcs(studentId.value)
    }
  }
})

const selectChild = async (child) => {
  selectedChild.value = child
  await fetchUnpaidEcs(child.id)
  selectedEc.value = null
}

const selectEc = (ec) => {
  selectedEc.value = ec
  step.value = 2
}

// Handle payment type change from ProviderSelector
const handleTypeChange = (type) => {
  paymentType.value = type
  selectedProvider.value = ''
  selectedBank.value = ''
  phoneNumber.value = ''
}

// Handle provider/bank selection from ProviderSelector
const handleSelection = (id) => {
  if (paymentType.value === 'mobile') {
    selectedProvider.value = id
  } else {
    selectedBank.value = id
  }
}

const detectProvider = () => {
  const prefix = phoneNumber.value.replace(/\s/g, '').substring(0, 3)
  for (const provider of providers) {
    if (provider.prefixes.includes(prefix)) {
      selectedProvider.value = provider.id
      return
    }
  }
}

const isValidPhone = computed(() => {
  const cleaned = phoneNumber.value.replace(/\s/g, '')
  return /^0(32|33|34|37|38)\d{7}$/.test(cleaned)
})

const canProceedMobile = computed(() => {
  return selectedProvider.value && isValidPhone.value
})

const canProceedBank = computed(() => {
  return selectedBank.value
})

const openConfirmDialog = () => {
  paymentError.value = null
  showConfirmDialog.value = true
}

const confirmPayment = async () => {
  try {
    if (paymentType.value === 'mobile') {
      paymentResult.value = await initiatePayment(
        selectedChild.value.id,
        selectedEc.value.id,
        selectedProvider.value,
        phoneNumber.value.replace(/\s/g, '')
      )
      showConfirmDialog.value = false
      step.value = 4 // Mobile confirmation
    } else {
      paymentResult.value = await initiateBankPayment(
        selectedChild.value.id,
        selectedEc.value.id,
        selectedBank.value
      )
      showConfirmDialog.value = false
      step.value = 3 // Bank info
    }
  } catch (e) {
    paymentError.value = e.message || 'Erreur lors du paiement'
  }
}

const handleSubmitBankProof = async ({ proofType, proofValue }) => {
  try {
    await submitBankProof(
      paymentResult.value.payment_id,
      proofType,
      proofValue
    )
    step.value = 4 // Confirmation
  } catch (e) {
    paymentError.value = e.message || 'Erreur lors de la soumission de la preuve'
  }
}

const goBack = () => {
  if (step.value === 4) {
    step.value = paymentType.value === 'bank' ? 3 : 2
  } else if (step.value === 3) {
    step.value = 2
  } else if (step.value > 1) {
    step.value--
    if (step.value === 1) {
      selectedEc.value = null
    }
  } else {
    router.push('/parent/dashboard')
  }
}

const goToDashboard = () => {
  router.push('/parent/dashboard')
}

const resetAndPayAnother = () => {
  selectedEc.value = null
  phoneNumber.value = ''
  selectedProvider.value = ''
  selectedBank.value = ''
  paymentResult.value = null
  paymentType.value = 'mobile'
  step.value = 1
}

const currentProviderLabel = computed(() => {
  if (paymentType.value === 'mobile') {
    return getProviderLabel(selectedProvider.value)
  } else {
    const bank = banks.find(b => b.id === selectedBank.value)
    return bank?.name || selectedBank.value
  }
})
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="bg-white border-b sticky top-0 z-10">
      <div class="max-w-3xl mx-auto px-4 py-4">
        <div class="flex items-center gap-4">
          <Button variant="ghost" @click="goBack">
            <ArrowLeft class="w-5 h-5" />
          </Button>
          <div class="flex-1">
            <h1 class="text-lg font-bold text-gray-900">Payer un EC</h1>
            <p class="text-sm text-gray-500">
              <template v-if="selectedChild">Pour {{ selectedChild.name }}</template>
              <template v-else>Choisissez un enfant</template>
            </p>
          </div>
        </div>
      </div>
    </div>

    <div class="max-w-3xl mx-auto px-4 py-6">
      <!-- Loading -->
      <div v-if="loading && children.length === 0" class="flex justify-center py-12">
        <Spinner class="w-8 h-8" />
      </div>

      <!-- Step 1: Choisir enfant et EC -->
      <template v-else-if="step === 1">
        <!-- Sélection enfant -->
        <div v-if="!selectedChild" class="mb-6">
          <h2 class="text-lg font-semibold mb-4">Choisir un enfant</h2>
          <div class="grid gap-3">
            <Card
              v-for="child in children"
              :key="child.id"
              class="p-4 cursor-pointer hover:shadow-md transition-shadow"
              @click="selectChild(child)"
            >
              <div class="flex items-center gap-4">
                <div class="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center">
                  <User class="w-6 h-6 text-blue-600" />
                </div>
                <div class="flex-1">
                  <div class="font-semibold">{{ child.name }}</div>
                  <div class="text-sm text-gray-500">{{ child.year }} - {{ child.center }}</div>
                </div>
                <Badge theme="blue">{{ child.validated_ecs }}/{{ child.total_ecs }} EC</Badge>
              </div>
            </Card>
          </div>
        </div>

        <!-- EC non payés -->
        <div v-else>
          <div class="flex items-center justify-between mb-4">
            <h2 class="text-lg font-semibold">EC disponibles</h2>
            <Button variant="subtle" size="sm" @click="selectedChild = null">
              Changer d'enfant
            </Button>
          </div>

          <div v-if="loading" class="flex justify-center py-8">
            <Spinner class="w-6 h-6" />
          </div>

          <div v-else-if="unpaidEcs.length === 0" class="text-center py-8">
            <CheckCircle class="w-12 h-12 text-green-400 mx-auto mb-3" />
            <p class="text-gray-600">Tous les EC sont déjà payés !</p>
          </div>

          <div v-else class="grid gap-3">
            <Card
              v-for="ec in unpaidEcs"
              :key="ec.id"
              class="p-4 cursor-pointer hover:shadow-md transition-shadow"
              @click="selectEc(ec)"
            >
              <div class="flex items-start justify-between">
                <div class="flex-1">
                  <div class="font-semibold text-gray-900">{{ ec.title }}</div>
                  <div class="text-sm text-gray-500 mt-1">{{ ec.description }}</div>
                  <div class="flex items-center gap-4 mt-2 text-xs text-gray-500">
                    <span class="flex items-center gap-1">
                      <Clock class="w-3 h-3" />
                      {{ ec.duration }}
                    </span>
                    <span class="flex items-center gap-1">
                      <BookOpen class="w-3 h-3" />
                      {{ ec.lessons }} leçons
                    </span>
                  </div>
                </div>
                <div class="text-right">
                  <div class="text-lg font-bold text-blue-600">{{ formatAmount(ec.price) }}</div>
                </div>
              </div>
            </Card>
          </div>
        </div>
      </template>

      <!-- Step 2: Choix mode de paiement -->
      <template v-else-if="step === 2">
        <Card class="p-4 mb-6">
          <div class="flex items-center gap-4 mb-4">
            <BookOpen class="w-8 h-8 text-blue-600" />
            <div>
              <div class="font-semibold">{{ selectedEc.title }}</div>
              <div class="text-sm text-gray-500">Pour {{ selectedChild.name }}</div>
            </div>
            <div class="ml-auto text-xl font-bold text-blue-600">
              {{ formatAmount(selectedEc.price) }}
            </div>
          </div>
        </Card>

        <!-- Mode de paiement -->
        <Card class="p-6 mb-6">
          <h3 class="font-semibold mb-4">Mode de paiement</h3>
          <ProviderSelector
            :model-value="paymentType === 'mobile' ? selectedProvider : selectedBank"
            :providers="providers"
            :banks="banks"
            :show-bank-option="true"
            @update:model-value="handleSelection"
            @type-change="handleTypeChange"
          />
        </Card>

        <!-- Numéro téléphone (Mobile Money) -->
        <Card v-if="paymentType === 'mobile' && selectedProvider" class="p-6 mb-6">
          <h3 class="font-semibold mb-3">Numéro de téléphone</h3>
          <div class="relative">
            <Phone class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input
              v-model="phoneNumber"
              type="tel"
              placeholder="034 XX XXX XX"
              class="w-full pl-12 pr-4 py-3 border rounded-lg text-lg focus:ring-2 focus:ring-blue-500"
              :class="{ 'border-red-500': phoneNumber && !isValidPhone }"
              @input="detectProvider"
            />
          </div>
          <p v-if="phoneNumber && !isValidPhone" class="text-sm text-red-500 mt-1">
            Numéro invalide. Format: 03X XX XXX XX
          </p>
        </Card>

        <!-- Bouton payer -->
        <Button
          variant="solid"
          size="lg"
          class="w-full"
          :disabled="paymentType === 'mobile' ? !canProceedMobile : !canProceedBank"
          @click="openConfirmDialog"
        >
          <template v-if="paymentType === 'mobile'">
            <CreditCard class="w-5 h-5 mr-2" />
            Payer {{ formatAmount(selectedEc.price) }}
          </template>
          <template v-else>
            <Building2 class="w-5 h-5 mr-2" />
            Continuer
          </template>
        </Button>
      </template>

      <!-- Step 3: Bank Info & Proof (Bank only) -->
      <template v-else-if="step === 3">
        <BankPaymentForm
          :payment="paymentResult"
          :loading="paying"
          @submit-proof="handleSubmitBankProof"
          @back="goBack"
        />
      </template>

      <!-- Step 4: Confirmation -->
      <template v-else-if="step === 4">
        <div class="text-center py-8">
          <div class="w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-4"
               :class="paymentType === 'bank' ? 'bg-amber-100' : 'bg-green-100'">
            <template v-if="paymentType === 'bank'">
              <Clock class="w-10 h-10 text-amber-600" />
            </template>
            <template v-else>
              <CheckCircle class="w-10 h-10 text-green-600" />
            </template>
          </div>

          <h2 class="text-xl font-bold text-gray-900 mb-2">
            <template v-if="paymentType === 'bank'">
              En attente de validation
            </template>
            <template v-else>
              Paiement initié !
            </template>
          </h2>

          <p class="text-gray-600 mb-6">
            <template v-if="paymentType === 'bank'">
              Votre preuve de paiement a été soumise. Le centre CNTEMAD la vérifiera
              et vous notifiera par email.
            </template>
            <template v-else>
              Une demande de paiement a été envoyée sur le numéro {{ phoneNumber }}.
              Validez le paiement sur votre téléphone.
            </template>
          </p>

          <Card class="p-4 mb-6 text-left">
            <div class="space-y-2 text-sm">
              <div class="flex justify-between">
                <span class="text-gray-500">EC</span>
                <span class="font-medium">{{ selectedEc.title }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-500">Pour</span>
                <span class="font-medium">{{ selectedChild.name }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-500">Montant</span>
                <span class="font-bold text-green-600">{{ formatAmount(selectedEc.price) }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-500">Mode</span>
                <span class="font-medium">{{ currentProviderLabel }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-500">Référence</span>
                <span class="font-mono">{{ paymentResult?.bank_reference || paymentResult?.payment_id || paymentResult?.id }}</span>
              </div>
            </div>
          </Card>

          <div class="flex gap-3">
            <Button variant="subtle" class="flex-1" @click="resetAndPayAnother">
              Payer un autre EC
            </Button>
            <Button variant="solid" class="flex-1" @click="goToDashboard">
              Retour au dashboard
            </Button>
          </div>
        </div>
      </template>
    </div>

    <!-- Dialog Confirmation -->
    <Dialog v-model="showConfirmDialog" :options="{ title: 'Confirmer le paiement' }">
      <template #body-content>
        <div class="space-y-4">
          <div class="p-4 bg-blue-50 rounded-lg">
            <div class="text-center">
              <div class="text-2xl font-bold text-blue-600 mb-1">
                {{ formatAmount(selectedEc?.price || 0) }}
              </div>
              <div class="text-sm text-blue-700">{{ selectedEc?.title }}</div>
            </div>
          </div>

          <div class="text-sm space-y-2">
            <div class="flex justify-between">
              <span class="text-gray-500">Pour</span>
              <span>{{ selectedChild?.name }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-500">Mode</span>
              <span>{{ currentProviderLabel }}</span>
            </div>
            <div v-if="paymentType === 'mobile'" class="flex justify-between">
              <span class="text-gray-500">Téléphone</span>
              <span>{{ phoneNumber }}</span>
            </div>
          </div>

          <div v-if="paymentError" class="p-3 bg-red-50 text-red-700 rounded-lg text-sm flex items-center gap-2">
            <AlertTriangle class="w-4 h-4" />
            {{ paymentError }}
          </div>

          <div class="p-3 bg-yellow-50 rounded-lg text-sm text-yellow-800">
            <template v-if="paymentType === 'mobile'">
              ⚠️ Gardez votre téléphone à portée de main pour confirmer le paiement.
            </template>
            <template v-else>
              ℹ️ Vous recevrez les coordonnées bancaires et une référence unique à mentionner dans votre virement.
            </template>
          </div>
        </div>
      </template>
      <template #actions>
        <Button variant="subtle" @click="showConfirmDialog = false">Annuler</Button>
        <Button variant="solid" @click="confirmPayment" :loading="paying">
          Confirmer
        </Button>
      </template>
    </Dialog>
  </div>
</template>
