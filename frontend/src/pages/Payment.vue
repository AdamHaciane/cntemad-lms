<script setup>
import { ref } from 'vue'
import { Card, Button, Input, Select } from 'frappe-ui'

const provider = ref('mvola')
const phone = ref('')
const amount = ref(50000)

const providers = [
  { label: 'MVola (Telma)', value: 'mvola' },
  { label: 'Orange Money', value: 'orange_money' },
  { label: 'Airtel Money', value: 'airtel_money' },
]

const handlePayment = () => {
  // TODO: Implement payment
  console.log('Payment:', { provider: provider.value, phone: phone.value, amount: amount.value })
}
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <header class="bg-white border-b px-4 py-4">
      <div class="max-w-md mx-auto">
        <h1 class="text-xl font-bold">Paiement</h1>
      </div>
    </header>

    <main class="px-4 py-6">
      <div class="max-w-md mx-auto space-y-6">
        <!-- Amount Card -->
        <Card class="p-6 text-center">
          <div class="text-sm text-gray-500 mb-2">Montant à payer</div>
          <div class="text-4xl font-bold text-cntemad-primary">
            {{ amount.toLocaleString() }} Ar
          </div>
          <div class="text-sm text-gray-500 mt-2">EC: Algorithmes - Module 1</div>
        </Card>

        <!-- Payment Form -->
        <Card class="p-6">
          <form @submit.prevent="handlePayment" class="space-y-4">
            <div>
              <label class="block text-sm font-medium mb-2">
                Mode de paiement
              </label>
              <div class="grid grid-cols-3 gap-2">
                <button
                  v-for="p in providers"
                  :key="p.value"
                  type="button"
                  @click="provider = p.value"
                  class="p-3 border rounded-lg text-center text-sm transition-colors"
                  :class="provider === p.value
                    ? 'border-cntemad-primary bg-blue-50 text-cntemad-primary'
                    : 'border-gray-200 hover:border-gray-300'"
                >
                  {{ p.label }}
                </button>
              </div>
            </div>

            <div>
              <label class="block text-sm font-medium mb-2">
                Numéro de téléphone
              </label>
              <Input
                v-model="phone"
                type="tel"
                placeholder="034 XX XXX XX"
                class="w-full"
              />
              <p class="text-xs text-gray-500 mt-1">
                Vous recevrez une demande de confirmation sur ce numéro
              </p>
            </div>

            <Button
              type="submit"
              variant="solid"
              class="w-full bg-cntemad-primary"
              :disabled="!phone"
            >
              Payer {{ amount.toLocaleString() }} Ar
            </Button>
          </form>
        </Card>

        <!-- Info -->
        <div class="text-center text-sm text-gray-500">
          <p>Paiement sécurisé</p>
          <p>En cas de problème, contactez votre centre</p>
        </div>
      </div>
    </main>
  </div>
</template>
