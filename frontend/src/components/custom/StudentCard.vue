<!--
  StudentCard.vue
  Carte profil étudiant avec progression.

  Props:
    - student (Object): { id, name, email, year, progress, lastActivity, image }
    - showAlert (Boolean): Afficher alerte si inactif

  Events:
    - @click: Émis au clic

  Example:
    <StudentCard :student="student" showAlert @click="viewStudent" />
-->
<script setup>
import { Card, Badge, Avatar } from 'frappe-ui'
import { computed } from 'vue'
import ProgressBar from './ProgressBar.vue'

const props = defineProps({
  student: {
    type: Object,
    required: true,
  },
  showAlert: {
    type: Boolean,
    default: true,
  },
})

const emit = defineEmits(['click'])

const isInactive = computed(() => {
  if (!props.student.lastActivity) return false
  const lastDate = new Date(props.student.lastActivity)
  const daysSince = Math.floor((Date.now() - lastDate) / (1000 * 60 * 60 * 24))
  return daysSince > 7
})

const lastActivityLabel = computed(() => {
  if (!props.student.lastActivity) return 'Jamais connecté'
  const lastDate = new Date(props.student.lastActivity)
  const daysSince = Math.floor((Date.now() - lastDate) / (1000 * 60 * 60 * 24))
  if (daysSince === 0) return 'Aujourd\'hui'
  if (daysSince === 1) return 'Hier'
  return `Il y a ${daysSince} jours`
})

const yearColors = {
  L1: 'blue',
  L2: 'blue',
  L3: 'blue',
  M1: 'green',
  M2: 'green',
}

const handleClick = () => {
  emit('click', props.student)
}
</script>

<template>
  <Card class="p-4 cursor-pointer hover:shadow-md transition-shadow" @click="handleClick">
    <div class="flex items-start gap-4">
      <!-- Avatar -->
      <Avatar
        :image="student.image"
        :label="student.name"
        size="lg"
        class="shrink-0"
      />

      <!-- Info -->
      <div class="flex-1 min-w-0">
        <div class="flex items-center gap-2 flex-wrap">
          <h3 class="font-semibold text-gray-900 truncate">
            {{ student.name }}
          </h3>
          <Badge :theme="yearColors[student.year] || 'gray'">
            {{ student.year }}
          </Badge>
          <Badge v-if="showAlert && isInactive" theme="red">
            Inactif
          </Badge>
        </div>

        <p class="text-sm text-gray-500 mt-1 truncate">
          {{ student.email }}
        </p>

        <!-- Progression -->
        <div class="mt-3">
          <ProgressBar
            :value="student.progress?.validated || 0"
            :max="student.progress?.total || 12"
            label="EC"
            size="sm"
          />
        </div>

        <!-- Dernière activité -->
        <p class="text-xs text-gray-400 mt-2">
          Dernière activité: {{ lastActivityLabel }}
        </p>
      </div>
    </div>
  </Card>
</template>
