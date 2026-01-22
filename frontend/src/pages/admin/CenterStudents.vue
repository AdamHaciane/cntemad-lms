<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="bg-white border-b sticky top-0 z-10">
      <div class="px-4 py-4">
        <div class="flex items-center gap-3">
          <router-link to="/admin/dashboard">
            <Button variant="ghost" class="p-2">
              <ArrowLeft class="w-5 h-5" />
            </Button>
          </router-link>
          <div class="flex-1">
            <h1 class="text-xl font-bold text-gray-900">Étudiants</h1>
            <p class="text-sm text-gray-500">
              {{ studentsTotal }} étudiant{{ studentsTotal > 1 ? 's' : '' }}
            </p>
          </div>
          <ExportButton
            @export="handleExport"
            :loading="exporting"
          />
        </div>
      </div>
    </div>

    <!-- Filtres -->
    <div class="p-4 bg-white border-b space-y-3">
      <!-- Recherche -->
      <div class="relative">
        <Search class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
        <Input
          v-model="filters.search"
          placeholder="Rechercher un étudiant..."
          class="pl-10"
          @input="debouncedSearch"
        />
      </div>

      <!-- Filtres rapides -->
      <div class="flex gap-2 overflow-x-auto pb-1">
        <Select
          v-model="filters.year"
          :options="yearOptions"
          placeholder="Année"
          class="min-w-[120px]"
          @update:modelValue="applyFilters"
        />
        <Select
          v-model="filters.status"
          :options="statusOptions"
          placeholder="Statut"
          class="min-w-[120px]"
          @update:modelValue="applyFilters"
        />
      </div>

      <!-- Tags filtres actifs -->
      <div v-if="hasActiveFilters" class="flex flex-wrap gap-2">
        <Badge
          v-if="filters.year"
          variant="subtle"
          theme="blue"
          class="cursor-pointer"
          @click="clearFilter('year')"
        >
          {{ filters.year }}
          <X class="w-3 h-3 ml-1" />
        </Badge>
        <Badge
          v-if="filters.status"
          variant="subtle"
          theme="green"
          class="cursor-pointer"
          @click="clearFilter('status')"
        >
          {{ getStatusLabel(filters.status) }}
          <X class="w-3 h-3 ml-1" />
        </Badge>
        <button
          class="text-xs text-blue-600 underline"
          @click="clearAllFilters"
        >
          Effacer tout
        </button>
      </div>
    </div>

    <!-- Liste étudiants -->
    <div class="p-4">
      <!-- Loading -->
      <div v-if="loading" class="flex justify-center py-8">
        <Spinner class="w-8 h-8" />
      </div>

      <!-- Liste -->
      <div v-else-if="students.length > 0" class="space-y-3">
        <StudentCard
          v-for="student in students"
          :key="student.name"
          :student="student"
          @click="openStudentDetail(student)"
        />

        <!-- Pagination -->
        <div v-if="hasMore" class="pt-4">
          <Button
            variant="outline"
            class="w-full"
            @click="loadMore"
            :loading="loadingMore"
          >
            Charger plus
          </Button>
        </div>
      </div>

      <!-- Vide -->
      <div v-else class="text-center py-12">
        <Users class="w-12 h-12 text-gray-300 mx-auto mb-4" />
        <p class="text-gray-500">Aucun étudiant trouvé</p>
        <p class="text-sm text-gray-400 mt-1">
          Essayez de modifier vos filtres
        </p>
      </div>
    </div>

    <!-- Dialog détail étudiant -->
    <Dialog v-model="showStudentDialog" :options="{ title: selectedStudent?.full_name }">
      <template #body-content>
        <div v-if="selectedStudent" class="space-y-4">
          <!-- Info basiques -->
          <div class="flex items-center gap-4">
            <Avatar
              :label="selectedStudent.full_name"
              :image="selectedStudent.image"
              size="xl"
            />
            <div>
              <p class="font-medium text-gray-900">{{ selectedStudent.full_name }}</p>
              <p class="text-sm text-gray-500">{{ selectedStudent.student_id }}</p>
              <Badge :theme="getStatusTheme(selectedStudent.status)">
                {{ selectedStudent.status }}
              </Badge>
            </div>
          </div>

          <!-- Détails -->
          <div class="divide-y">
            <div class="py-3 flex justify-between">
              <span class="text-gray-500">Email</span>
              <span class="text-gray-900">{{ selectedStudent.email || '-' }}</span>
            </div>
            <div class="py-3 flex justify-between">
              <span class="text-gray-500">Téléphone</span>
              <span class="text-gray-900">{{ selectedStudent.phone || '-' }}</span>
            </div>
            <div class="py-3 flex justify-between">
              <span class="text-gray-500">Année</span>
              <span class="text-gray-900">{{ selectedStudent.year || '-' }}</span>
            </div>
            <div class="py-3 flex justify-between">
              <span class="text-gray-500">EC inscrits</span>
              <span class="text-gray-900">{{ selectedStudent.enrolled_ec || 0 }}</span>
            </div>
            <div class="py-3 flex justify-between">
              <span class="text-gray-500">EC validés</span>
              <span class="text-gray-900">{{ selectedStudent.validated_ec || 0 }}</span>
            </div>
            <div class="py-3 flex justify-between">
              <span class="text-gray-500">Inscription</span>
              <span class="text-gray-900">{{ formatDate(selectedStudent.creation) }}</span>
            </div>
          </div>

          <!-- Progression -->
          <div v-if="selectedStudent.enrolled_ec > 0">
            <p class="text-sm text-gray-500 mb-2">Progression</p>
            <div class="w-full bg-gray-200 rounded-full h-2">
              <div
                class="bg-green-500 h-2 rounded-full transition-all"
                :style="{ width: `${getProgressPercent(selectedStudent)}%` }"
              ></div>
            </div>
            <p class="text-xs text-gray-500 mt-1 text-right">
              {{ getProgressPercent(selectedStudent) }}%
            </p>
          </div>
        </div>
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { Button, Card, Input, Select, Badge, Dialog, Avatar, Spinner } from 'frappe-ui'
import { ArrowLeft, Search, Users, X } from 'lucide-vue-next'
import StudentCard from '@/components/custom/StudentCard.vue'
import ExportButton from '@/components/custom/ExportButton.vue'
import { useCenter } from '@/composables/useCenter'

const {
  students,
  studentsTotal,
  loading,
  fetchStudents,
  exportStudents
} = useCenter()

const filters = ref({
  search: '',
  year: '',
  status: ''
})

const showStudentDialog = ref(false)
const selectedStudent = ref(null)
const loadingMore = ref(false)
const exporting = ref(false)
const currentOffset = ref(0)
const pageSize = 20

const yearOptions = [
  { label: 'Toutes', value: '' },
  { label: 'Licence 1', value: 'L1' },
  { label: 'Licence 2', value: 'L2' },
  { label: 'Licence 3', value: 'L3' },
  { label: 'Master 1', value: 'M1' },
  { label: 'Master 2', value: 'M2' }
]

const statusOptions = [
  { label: 'Tous', value: '' },
  { label: 'Actif', value: 'active' },
  { label: 'Inactif', value: 'inactive' }
]

const hasActiveFilters = computed(() => {
  return filters.value.year || filters.value.status || filters.value.search
})

const hasMore = computed(() => {
  return students.value.length < studentsTotal.value
})

onMounted(() => {
  loadStudents()
})

const loadStudents = async () => {
  currentOffset.value = 0
  await fetchStudents({
    ...filters.value,
    limit: pageSize,
    offset: 0
  })
}

const loadMore = async () => {
  loadingMore.value = true
  currentOffset.value += pageSize
  try {
    await fetchStudents({
      ...filters.value,
      limit: pageSize,
      offset: currentOffset.value,
      append: true
    })
  } finally {
    loadingMore.value = false
  }
}

let searchTimeout = null
const debouncedSearch = () => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    loadStudents()
  }, 300)
}

const applyFilters = () => {
  loadStudents()
}

const clearFilter = (key) => {
  filters.value[key] = ''
  loadStudents()
}

const clearAllFilters = () => {
  filters.value = { search: '', year: '', status: '' }
  loadStudents()
}

const openStudentDetail = (student) => {
  selectedStudent.value = student
  showStudentDialog.value = true
}

const handleExport = async (format) => {
  exporting.value = true
  try {
    await exportStudents(format)
  } finally {
    exporting.value = false
  }
}

const getStatusLabel = (status) => {
  const labels = { active: 'Actif', inactive: 'Inactif' }
  return labels[status] || status
}

const getStatusTheme = (status) => {
  if (!status) return 'gray'
  const s = status.toLowerCase()
  if (s === 'active' || s === 'actif') return 'green'
  return 'gray'
}

const getProgressPercent = (student) => {
  if (!student.enrolled_ec) return 0
  return Math.round((student.validated_ec / student.enrolled_ec) * 100)
}

const formatDate = (date) => {
  if (!date) return '-'
  return new Date(date).toLocaleDateString('fr-FR')
}
</script>
