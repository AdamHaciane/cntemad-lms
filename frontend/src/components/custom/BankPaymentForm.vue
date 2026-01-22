<!--
  BankPaymentForm.vue
  Formulaire de paiement par virement bancaire.

  Affiche:
    - Coordonnées bancaires CNTEMAD (RIB, SWIFT)
    - Référence unique à mentionner
    - Montant à payer
    - Formulaire de soumission de preuve

  Props:
    - payment (Object): Données du paiement initié
    - loading (Boolean): État de chargement

  Events:
    - @submit-proof({ proofType, proofValue }): Émis à la soumission de preuve
    - @back: Retour à l'étape précédente

  Example:
    <BankPaymentForm
      :payment="currentPayment"
      :loading="loading"
      @submit-proof="handleSubmitProof"
    />
-->
<script setup>
import { ref, computed } from 'vue'
import { Card, Button, Input, Dialog } from 'frappe-ui'

const props = defineProps({
  payment: {
    type: Object,
    required: true,
  },
  loading: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['submit-proof', 'back'])

// State
const step = ref('info') // 'info' | 'proof'
const proofType = ref('reference') // 'reference' | 'receipt'
const proofValue = ref('')
const showConfirmDialog = ref(false)

// Computed
const bankInfo = computed(() => props.payment?.bank || {})
const reference = computed(() => props.payment?.reference || props.payment?.bank_reference || '')
const amount = computed(() => props.payment?.amount || 0)
const ecTitle = computed(() => props.payment?.ec_title || props.payment?.ec || '')

const formattedAmount = computed(() => {
  return new Intl.NumberFormat('fr-MG').format(amount.value) + ' Ar'
})

const canSubmitProof = computed(() => {
  if (!proofValue.value) return false
  if (proofType.value === 'reference') {
    return proofValue.value.trim().length >= 5
  }
  return proofValue.value.trim().length > 0
})

// Methods
const copyToClipboard = (text) => {
  navigator.clipboard.writeText(text)
  // Could add a toast notification here
}

const proceedToProof = () => {
  step.value = 'proof'
}

const goBackToInfo = () => {
  step.value = 'info'
}

const confirmSubmit = () => {
  showConfirmDialog.value = true
}

const submitProof = () => {
  showConfirmDialog.value = false
  emit('submit-proof', {
    proofType: proofType.value,
    proofValue: proofValue.value.trim(),
  })
}
</script>

<template>
  <div class="space-y-6">
    <!-- Step 1: Bank Info & Instructions -->
    <template v-if="step === 'info'">
      <!-- Amount Card -->
      <Card class="p-6 text-center bg-gradient-to-br from-blue-50 to-blue-100 border-blue-200">
        <div class="text-sm text-blue-600 mb-1">Montant à virer</div>
        <div class="text-4xl font-bold text-blue-700">{{ formattedAmount }}</div>
        <div class="text-sm text-blue-600 mt-2">{{ ecTitle }}</div>
      </Card>

      <!-- Bank Details Card -->
      <Card class="p-6">
        <h3 class="font-semibold text-gray-900 mb-4 flex items-center gap-2">
          <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
          </svg>
          Coordonnées bancaires CNTEMAD
        </h3>

        <div class="space-y-4">
          <!-- Bank Name -->
          <div class="flex justify-between items-center py-2 border-b border-gray-100">
            <span class="text-gray-500">Banque</span>
            <span class="font-medium text-gray-900">{{ bankInfo.name }}</span>
          </div>

          <!-- RIB -->
          <div class="flex justify-between items-start py-2 border-b border-gray-100">
            <span class="text-gray-500">RIB</span>
            <div class="text-right flex items-center gap-2">
              <span class="font-mono font-medium text-gray-900">{{ bankInfo.rib }}</span>
              <button
                type="button"
                class="p-1 hover:bg-gray-100 rounded"
                @click="copyToClipboard(bankInfo.rib)"
                title="Copier"
              >
                <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                </svg>
              </button>
            </div>
          </div>

          <!-- Account Name -->
          <div class="flex justify-between items-center py-2 border-b border-gray-100">
            <span class="text-gray-500">Titulaire</span>
            <span class="font-medium text-gray-900">{{ bankInfo.account_name }}</span>
          </div>

          <!-- SWIFT -->
          <div class="flex justify-between items-center py-2 border-b border-gray-100">
            <span class="text-gray-500">Code SWIFT</span>
            <span class="font-mono font-medium text-gray-900">{{ bankInfo.swift }}</span>
          </div>
        </div>
      </Card>

      <!-- Reference Card (Important!) -->
      <Card class="p-6 bg-amber-50 border-amber-200">
        <h3 class="font-semibold text-amber-900 mb-2 flex items-center gap-2">
          <svg class="w-5 h-5 text-amber-600" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
          </svg>
          Référence à mentionner
        </h3>
        <p class="text-sm text-amber-800 mb-3">
          Indiquez cette référence dans le libellé de votre virement pour faciliter le traitement.
        </p>
        <div class="flex items-center gap-2 bg-white rounded-lg p-3 border border-amber-300">
          <span class="font-mono font-bold text-lg text-amber-900 flex-1">{{ reference }}</span>
          <button
            type="button"
            class="p-2 hover:bg-amber-100 rounded-lg transition-colors"
            @click="copyToClipboard(reference)"
            title="Copier la référence"
          >
            <svg class="w-5 h-5 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
            </svg>
          </button>
        </div>
      </Card>

      <!-- Instructions -->
      <Card class="p-6">
        <h3 class="font-semibold text-gray-900 mb-4">Instructions</h3>
        <ol class="space-y-3 text-sm text-gray-600">
          <li class="flex gap-3">
            <span class="flex-shrink-0 w-6 h-6 bg-blue-100 text-blue-700 rounded-full flex items-center justify-center font-medium text-xs">1</span>
            <span>Rendez-vous dans votre banque ou connectez-vous à votre espace bancaire en ligne.</span>
          </li>
          <li class="flex gap-3">
            <span class="flex-shrink-0 w-6 h-6 bg-blue-100 text-blue-700 rounded-full flex items-center justify-center font-medium text-xs">2</span>
            <span>Effectuez un virement de <strong>{{ formattedAmount }}</strong> vers le compte CNTEMAD.</span>
          </li>
          <li class="flex gap-3">
            <span class="flex-shrink-0 w-6 h-6 bg-blue-100 text-blue-700 rounded-full flex items-center justify-center font-medium text-xs">3</span>
            <span>Mentionnez la référence <strong class="font-mono">{{ reference }}</strong> dans le libellé.</span>
          </li>
          <li class="flex gap-3">
            <span class="flex-shrink-0 w-6 h-6 bg-blue-100 text-blue-700 rounded-full flex items-center justify-center font-medium text-xs">4</span>
            <span>Conservez votre reçu de virement pour la confirmation.</span>
          </li>
        </ol>
      </Card>

      <!-- Action Button -->
      <div class="flex gap-3">
        <Button variant="outline" class="flex-1" @click="$emit('back')">
          Retour
        </Button>
        <Button variant="solid" theme="green" class="flex-1" @click="proceedToProof">
          J'ai effectué le virement
        </Button>
      </div>
    </template>

    <!-- Step 2: Proof Submission -->
    <template v-else-if="step === 'proof'">
      <Card class="p-6">
        <h3 class="font-semibold text-gray-900 mb-4">Confirmer votre virement</h3>
        <p class="text-sm text-gray-600 mb-6">
          Comment souhaitez-vous confirmer votre paiement ?
        </p>

        <!-- Proof Type Selection -->
        <div class="space-y-3 mb-6">
          <label
            class="flex items-start gap-3 p-4 border-2 rounded-lg cursor-pointer transition-colors"
            :class="proofType === 'reference' ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-gray-300'"
          >
            <input
              type="radio"
              v-model="proofType"
              value="reference"
              class="mt-1"
            />
            <div>
              <div class="font-medium text-gray-900">Numéro de référence bancaire</div>
              <div class="text-sm text-gray-500">Entrez le numéro de transaction fourni par votre banque</div>
            </div>
          </label>

          <label
            class="flex items-start gap-3 p-4 border-2 rounded-lg cursor-pointer transition-colors"
            :class="proofType === 'receipt' ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-gray-300'"
          >
            <input
              type="radio"
              v-model="proofType"
              value="receipt"
              class="mt-1"
            />
            <div>
              <div class="font-medium text-gray-900">Photo du reçu</div>
              <div class="text-sm text-gray-500">Téléchargez une photo ou scan de votre reçu de virement</div>
            </div>
          </label>
        </div>

        <!-- Proof Input -->
        <div class="mb-6">
          <label class="block text-sm font-medium mb-2">
            {{ proofType === 'reference' ? 'Numéro de référence' : 'URL de l\'image' }}
          </label>
          <Input
            v-if="proofType === 'reference'"
            v-model="proofValue"
            placeholder="Ex: TRF-2024012200123456"
            class="w-full"
          />
          <div v-else>
            <Input
              v-model="proofValue"
              placeholder="Collez l'URL de votre image"
              class="w-full"
            />
            <p class="text-xs text-gray-500 mt-1">
              Téléchargez votre image sur un service comme Imgur, puis collez le lien ici.
            </p>
          </div>
        </div>

        <!-- Summary -->
        <div class="bg-gray-50 rounded-lg p-4 mb-6">
          <div class="text-sm text-gray-600 space-y-2">
            <div class="flex justify-between">
              <span>EC</span>
              <span class="font-medium text-gray-900">{{ ecTitle }}</span>
            </div>
            <div class="flex justify-between">
              <span>Montant</span>
              <span class="font-medium text-gray-900">{{ formattedAmount }}</span>
            </div>
            <div class="flex justify-between">
              <span>Référence CNTEMAD</span>
              <span class="font-mono text-gray-900">{{ reference }}</span>
            </div>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="flex gap-3">
          <Button variant="outline" class="flex-1" @click="goBackToInfo">
            Retour
          </Button>
          <Button
            variant="solid"
            theme="green"
            class="flex-1"
            :disabled="!canSubmitProof"
            :loading="loading"
            @click="confirmSubmit"
          >
            Soumettre ma preuve
          </Button>
        </div>
      </Card>
    </template>

    <!-- Confirmation Dialog -->
    <Dialog v-model="showConfirmDialog" :options="{ title: 'Confirmer la soumission' }">
      <template #body-content>
        <div class="space-y-4">
          <p class="text-gray-600">
            Êtes-vous sûr de vouloir soumettre cette preuve de paiement ?
          </p>
          <div class="bg-gray-50 rounded-lg p-4 text-sm space-y-2">
            <div class="flex justify-between">
              <span class="text-gray-500">Type de preuve</span>
              <span>{{ proofType === 'reference' ? 'Référence bancaire' : 'Photo du reçu' }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-500">Valeur</span>
              <span class="font-mono truncate max-w-[200px]">{{ proofValue }}</span>
            </div>
          </div>
          <div class="p-3 bg-blue-50 rounded-lg text-sm text-blue-700">
            <p>
              Votre centre CNTEMAD vérifiera votre paiement et vous notifiera par email une fois validé.
            </p>
          </div>
        </div>
      </template>
      <template #actions>
        <Button variant="outline" @click="showConfirmDialog = false">
          Annuler
        </Button>
        <Button variant="solid" theme="green" @click="submitProof" :loading="loading">
          Confirmer
        </Button>
      </template>
    </Dialog>
  </div>
</template>
