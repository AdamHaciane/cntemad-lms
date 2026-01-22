<!--
  ProviderSelector.vue
  Sélection du provider de paiement (mobile money ou virement bancaire).

  Props:
    - modelValue (String): Provider sélectionné (v-model)
    - providers (Array): Liste des providers mobile money (optionnel)
    - banks (Array): Liste des banques (optionnel)
    - disabled (Boolean): Désactiver la sélection
    - showBankOption (Boolean): Afficher l'option virement bancaire (default: true)

  Events:
    - @update:modelValue(provider): Émis à la sélection
    - @select(provider): Émis à la sélection
    - @type-change(type): Émis au changement de type ('mobile' ou 'bank')

  Example:
    <ProviderSelector v-model="selectedProvider" @type-change="handleTypeChange" />
-->
<script setup>
import { ref, computed, watch } from 'vue'

const DEFAULT_PROVIDERS = [
  {
    id: 'mvola',
    name: 'MVola',
    operator: 'Telma',
    prefixes: ['034', '038'],
    color: 'bg-yellow-500',
  },
  {
    id: 'orange_money',
    name: 'Orange Money',
    operator: 'Orange',
    prefixes: ['032', '037'],
    color: 'bg-orange-500',
  },
  {
    id: 'airtel_money',
    name: 'Airtel Money',
    operator: 'Airtel',
    prefixes: ['033'],
    color: 'bg-red-600',
  },
]

const DEFAULT_BANKS = [
  {
    id: 'bfv',
    name: 'BFV-SG',
    description: 'Société Générale',
    color: 'bg-blue-700',
  },
  {
    id: 'bni',
    name: 'BNI Madagascar',
    description: 'Banque Nationale',
    color: 'bg-emerald-600',
  },
]

const props = defineProps({
  modelValue: {
    type: String,
    default: '',
  },
  providers: {
    type: Array,
    default: () => DEFAULT_PROVIDERS,
  },
  banks: {
    type: Array,
    default: () => DEFAULT_BANKS,
  },
  disabled: {
    type: Boolean,
    default: false,
  },
  showBankOption: {
    type: Boolean,
    default: true,
  },
})

const emit = defineEmits(['update:modelValue', 'select', 'type-change'])

// Payment type: 'mobile' or 'bank'
const paymentType = ref('mobile')

const providerList = computed(() => {
  return props.providers.map((p) => {
    const defaultProvider = DEFAULT_PROVIDERS.find((d) => d.id === p.id)
    return {
      ...defaultProvider,
      ...p,
    }
  })
})

const bankList = computed(() => {
  return props.banks.map((b) => {
    const defaultBank = DEFAULT_BANKS.find((d) => d.id === b.id)
    return {
      ...defaultBank,
      ...b,
    }
  })
})

// Determine initial payment type based on current value
watch(
  () => props.modelValue,
  (newValue) => {
    if (newValue && newValue.startsWith('bank_')) {
      paymentType.value = 'bank'
    } else if (newValue) {
      paymentType.value = 'mobile'
    }
  },
  { immediate: true }
)

const setPaymentType = (type) => {
  if (props.disabled) return
  paymentType.value = type
  emit('update:modelValue', '') // Clear selection when changing type
  emit('type-change', type)
}

const selectProvider = (provider) => {
  if (props.disabled) return
  emit('update:modelValue', provider.id)
  emit('select', provider.id)
}

const selectBank = (bank) => {
  if (props.disabled) return
  emit('update:modelValue', bank.id)
  emit('select', bank.id)
}

const isSelected = (id) => props.modelValue === id
</script>

<template>
  <div class="space-y-4">
    <!-- Payment Type Tabs -->
    <div v-if="showBankOption" class="flex rounded-lg bg-gray-100 p-1">
      <button
        type="button"
        class="flex-1 flex items-center justify-center gap-2 py-2.5 px-4 rounded-md text-sm font-medium transition-all"
        :class="[
          paymentType === 'mobile'
            ? 'bg-white text-gray-900 shadow-sm'
            : 'text-gray-600 hover:text-gray-900',
          disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'
        ]"
        :disabled="disabled"
        @click="setPaymentType('mobile')"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z" />
        </svg>
        Mobile Money
      </button>
      <button
        type="button"
        class="flex-1 flex items-center justify-center gap-2 py-2.5 px-4 rounded-md text-sm font-medium transition-all"
        :class="[
          paymentType === 'bank'
            ? 'bg-white text-gray-900 shadow-sm'
            : 'text-gray-600 hover:text-gray-900',
          disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'
        ]"
        :disabled="disabled"
        @click="setPaymentType('bank')"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
        </svg>
        Virement Bancaire
      </button>
    </div>

    <!-- Mobile Money Providers -->
    <div v-if="paymentType === 'mobile'" class="grid grid-cols-1 sm:grid-cols-3 gap-3">
      <button
        v-for="provider in providerList"
        :key="provider.id"
        type="button"
        class="flex items-center gap-3 p-4 rounded-lg border-2 transition-all"
        :class="[
          isSelected(provider.id)
            ? 'border-cntemad-primary bg-cntemad-primary/5'
            : 'border-gray-200 hover:border-gray-300',
          disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'
        ]"
        :disabled="disabled"
        @click="selectProvider(provider)"
      >
        <!-- Logo placeholder -->
        <div
          class="w-10 h-10 rounded-full flex items-center justify-center text-white font-bold text-sm"
          :class="provider.color || 'bg-gray-500'"
        >
          {{ provider.name?.charAt(0) || '?' }}
        </div>

        <div class="text-left flex-1">
          <div class="font-medium text-gray-900">{{ provider.name }}</div>
          <div class="text-xs text-gray-500">
            {{ provider.operator || provider.prefixes?.join(', ') }}
          </div>
        </div>

        <!-- Check icon if selected -->
        <div v-if="isSelected(provider.id)" class="flex-shrink-0">
          <svg class="w-5 h-5 text-cntemad-primary" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
          </svg>
        </div>
      </button>
    </div>

    <!-- Bank Transfer Options -->
    <div v-else class="grid grid-cols-1 sm:grid-cols-2 gap-3">
      <button
        v-for="bank in bankList"
        :key="bank.id"
        type="button"
        class="flex items-center gap-3 p-4 rounded-lg border-2 transition-all"
        :class="[
          isSelected(bank.id)
            ? 'border-cntemad-primary bg-cntemad-primary/5'
            : 'border-gray-200 hover:border-gray-300',
          disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'
        ]"
        :disabled="disabled"
        @click="selectBank(bank)"
      >
        <!-- Bank icon -->
        <div
          class="w-10 h-10 rounded-full flex items-center justify-center text-white font-bold text-sm"
          :class="bank.color || 'bg-blue-600'"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
          </svg>
        </div>

        <div class="text-left flex-1">
          <div class="font-medium text-gray-900">{{ bank.name }}</div>
          <div class="text-xs text-gray-500">
            {{ bank.description || 'Virement bancaire' }}
          </div>
        </div>

        <!-- Check icon if selected -->
        <div v-if="isSelected(bank.id)" class="flex-shrink-0">
          <svg class="w-5 h-5 text-cntemad-primary" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
          </svg>
        </div>
      </button>

      <!-- Bank transfer info -->
      <div class="sm:col-span-2 mt-2 p-3 bg-blue-50 rounded-lg text-sm text-blue-800">
        <p class="flex items-start gap-2">
          <svg class="w-5 h-5 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
          </svg>
          <span>
            Le virement bancaire nécessite une validation manuelle par votre centre CNTEMAD.
            L'accès au contenu sera activé après vérification du paiement.
          </span>
        </p>
      </div>
    </div>
  </div>
</template>
