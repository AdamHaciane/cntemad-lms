<!--
  StatusBadge.vue
  Badge de statut réutilisable avec configurations prédéfinies.

  Props:
    - status (String): Clé du statut
    - size (String): Taille sm, md, lg

  Example:
    <StatusBadge status="validated" />
    <StatusBadge status="pending" size="lg" />
-->
<script setup>
import { Badge } from 'frappe-ui'
import { computed } from 'vue'

const props = defineProps({
  status: {
    type: String,
    required: true,
  },
  size: {
    type: String,
    default: 'md',
    validator: (v) => ['sm', 'md', 'lg'].includes(v),
  },
})

const statusMap = {
  // Paiement
  pending: { label: 'En attente', theme: 'yellow' },
  processing: { label: 'Traitement', theme: 'blue' },
  success: { label: 'Réussi', theme: 'green' },
  failed: { label: 'Échoué', theme: 'red' },

  // EC
  not_started: { label: 'Non commencé', theme: 'gray' },
  in_progress: { label: 'En cours', theme: 'blue' },
  completed: { label: 'Terminé', theme: 'green' },
  validated: { label: 'Validé', theme: 'green' },

  // Étudiant
  active: { label: 'Actif', theme: 'green' },
  inactive: { label: 'Inactif', theme: 'gray' },
  suspended: { label: 'Suspendu', theme: 'red' },
  graduated: { label: 'Diplômé', theme: 'blue' },

  // Général
  draft: { label: 'Brouillon', theme: 'gray' },
  published: { label: 'Publié', theme: 'green' },
  archived: { label: 'Archivé', theme: 'gray' },

  // Paiement EC
  paid: { label: 'Payé', theme: 'green' },
  not_paid: { label: 'Non payé', theme: 'gray' },
}

const config = computed(() => {
  return statusMap[props.status] || { label: props.status, theme: 'gray' }
})

const sizeClass = computed(() => ({
  sm: 'text-xs px-2 py-0.5',
  md: 'text-sm px-2.5 py-0.5',
  lg: 'text-base px-3 py-1',
}[props.size]))
</script>

<template>
  <Badge :theme="config.theme" :class="sizeClass">
    {{ config.label }}
  </Badge>
</template>
