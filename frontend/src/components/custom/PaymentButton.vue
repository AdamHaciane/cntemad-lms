<!--
  PaymentButton.vue
  Bouton de paiement avec montant formaté et état loading.

  Props:
    - amount (Number): Montant en Ariary
    - provider (String): Provider sélectionné
    - loading (Boolean): État de chargement
    - disabled (Boolean): Désactiver le bouton

  Events:
    - @pay: Émis au clic

  Example:
    <PaymentButton :amount="150000" provider="mvola" @pay="handlePayment" />
-->
<script setup>
import { Button, Spinner } from 'frappe-ui'
import { computed } from 'vue'

const props = defineProps({
  amount: {
    type: Number,
    required: true,
  },
  provider: {
    type: String,
    default: null,
  },
  loading: {
    type: Boolean,
    default: false,
  },
  disabled: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['pay'])

const formattedAmount = computed(() => {
  return new Intl.NumberFormat('fr-MG').format(props.amount) + ' Ar'
})

const isDisabled = computed(() => {
  return props.disabled || props.loading || !props.provider || props.amount <= 0
})

const handleClick = () => {
  if (!isDisabled.value) {
    emit('pay')
  }
}
</script>

<template>
  <Button
    variant="solid"
    size="lg"
    class="w-full"
    :disabled="isDisabled"
    @click="handleClick"
  >
    <template v-if="loading">
      <Spinner class="w-5 h-5 mr-2" />
      Traitement en cours...
    </template>
    <template v-else>
      <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z" />
      </svg>
      Payer {{ formattedAmount }}
    </template>
  </Button>
</template>
