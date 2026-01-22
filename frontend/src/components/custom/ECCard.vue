<!--
  ECCard.vue
  Affiche une carte EC avec prix, durée, statut.

  Props:
    - ec (Object): { id, title, description, price, duration, status, image }
    - compact (Boolean): Mode compact pour listes

  Events:
    - @click: Émis au clic sur la carte

  Example:
    <ECCard
      :ec="{ id: 'EC001', title: 'Algorithmes', price: 50000, status: 'paid' }"
      @click="openEC"
    />
-->
<script setup>
import { Card, Badge, Button } from 'frappe-ui'
import { computed } from 'vue'

const props = defineProps({
  ec: {
    type: Object,
    required: true,
  },
  compact: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['click'])

const statusConfig = {
  not_paid: { label: 'Non payé', variant: 'subtle', color: 'gray' },
  paid: { label: 'Payé', variant: 'subtle', color: 'blue' },
  in_progress: { label: 'En cours', variant: 'subtle', color: 'yellow' },
  validated: { label: 'Validé', variant: 'solid', color: 'green' },
}

const status = computed(() => statusConfig[props.ec.status] || statusConfig.not_paid)

const actionLabel = computed(() => {
  switch (props.ec.status) {
    case 'not_paid': return 'Payer'
    case 'paid':
    case 'in_progress': return 'Continuer'
    case 'validated': return 'Voir'
    default: return 'Voir'
  }
})

const formatPrice = (price) => {
  return new Intl.NumberFormat('fr-MG').format(price) + ' Ar'
}

const handleClick = () => {
  emit('click', props.ec)
}
</script>

<template>
  <Card
    class="cursor-pointer hover:shadow-md transition-shadow"
    :class="compact ? 'p-3' : 'p-4'"
    @click="handleClick"
  >
    <!-- Image (si pas compact) -->
    <div v-if="!compact && ec.image" class="mb-3 -mx-4 -mt-4">
      <img
        :src="ec.image"
        :alt="ec.title"
        class="w-full h-32 object-cover rounded-t-lg"
      />
    </div>

    <!-- Header -->
    <div class="flex justify-between items-start gap-2">
      <h3
        class="font-semibold text-gray-900"
        :class="compact ? 'text-sm line-clamp-1' : 'text-base line-clamp-2'"
      >
        {{ ec.title }}
      </h3>
      <Badge :theme="status.color" class="shrink-0">
        {{ status.label }}
      </Badge>
    </div>

    <!-- Description (si pas compact) -->
    <p
      v-if="!compact && ec.description"
      class="text-sm text-gray-500 mt-2 line-clamp-2"
    >
      {{ ec.description }}
    </p>

    <!-- Footer -->
    <div class="flex justify-between items-center mt-3" :class="compact ? 'mt-2' : 'mt-3'">
      <div class="flex items-center gap-3 text-sm text-gray-600">
        <span class="font-medium text-cntemad-primary">
          {{ formatPrice(ec.price) }}
        </span>
        <span v-if="ec.duration" class="text-gray-400">
          {{ ec.duration }}h
        </span>
      </div>
      <Button
        v-if="!compact"
        size="sm"
        :variant="ec.status === 'not_paid' ? 'solid' : 'outline'"
        @click.stop="handleClick"
      >
        {{ actionLabel }}
      </Button>
    </div>
  </Card>
</template>
