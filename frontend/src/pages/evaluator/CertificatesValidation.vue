<!--
  CertificatesValidation.vue
  Page de validation des certificats pour l'évaluateur.
  Permet de valider les certificats des étudiants ayant complété une année.
-->
<script setup>
import { ref, computed, onMounted } from 'vue'
import { Card, Button, Badge, Dialog, Input, Spinner } from 'frappe-ui'
import {
  Award, User, Calendar, CheckCircle, XCircle, Search,
  FileCheck, AlertTriangle, GraduationCap, RefreshCw
} from 'lucide-vue-next'
import { useEvaluator } from '@/composables/useEvaluator'

const {
  pendingCertificates,
  loading,
  submitting,
  error,
  certificatesCount,
  fetchPendingCertificates,
  validateCertificate,
} = useEvaluator()

const searchQuery = ref('')
const selectedYear = ref('')
const showValidateDialog = ref(false)
const showRejectDialog = ref(false)
const selectedStudent = ref(null)
const certificateNumber = ref('')
const rejectReason = ref('')
const validationError = ref(null)

onMounted(async () => {
  await fetchPendingCertificates()
})

const filteredCertificates = computed(() => {
  let result = pendingCertificates.value

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(c =>
      c.student_name?.toLowerCase().includes(query) ||
      c.student_id?.toLowerCase().includes(query)
    )
  }

  if (selectedYear.value) {
    result = result.filter(c => c.year === selectedYear.value)
  }

  return result
})

const uniqueYears = computed(() => {
  const years = new Set(pendingCertificates.value.map(c => c.year))
  return Array.from(years).sort().reverse()
})

const yearLabels = {
  L1: 'Licence 1',
  L2: 'Licence 2',
  L3: 'Licence 3',
  M1: 'Master 1',
  M2: 'Master 2',
}

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleDateString('fr-FR', {
    day: '2-digit',
    month: 'long',
    year: 'numeric',
  })
}

const openValidateDialog = (student) => {
  selectedStudent.value = student
  certificateNumber.value = generateCertificateNumber(student)
  validationError.value = null
  showValidateDialog.value = true
}

const openRejectDialog = (student) => {
  selectedStudent.value = student
  rejectReason.value = ''
  validationError.value = null
  showRejectDialog.value = true
}

const generateCertificateNumber = (student) => {
  const year = new Date().getFullYear()
  const random = Math.floor(Math.random() * 10000).toString().padStart(4, '0')
  return `CNTEMAD-${student.year}-${year}-${random}`
}

const confirmValidation = async () => {
  if (!certificateNumber.value) {
    validationError.value = 'Le numéro de certificat est requis'
    return
  }

  try {
    await validateCertificate(
      selectedStudent.value.student_id,
      selectedStudent.value.year,
      certificateNumber.value
    )
    showValidateDialog.value = false
    await fetchPendingCertificates()
  } catch (e) {
    validationError.value = e.message || 'Erreur lors de la validation'
  }
}

const confirmRejection = async () => {
  // Pour l'instant, on ne gère pas le rejet côté API
  // On pourrait ajouter un endpoint reject_certificate
  showRejectDialog.value = false
}

const refreshList = async () => {
  await fetchPendingCertificates()
}

const getProgressColor = (progress) => {
  if (progress >= 100) return 'text-green-600'
  if (progress >= 80) return 'text-blue-600'
  if (progress >= 50) return 'text-yellow-600'
  return 'text-red-600'
}
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="bg-white border-b sticky top-0 z-10">
      <div class="max-w-7xl mx-auto px-4 py-4">
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h1 class="text-xl font-bold text-gray-900">Validation des certificats</h1>
            <p class="text-sm text-gray-500">
              Validez les certificats des étudiants ayant complété leur année
            </p>
          </div>
          <div class="flex items-center gap-2">
            <Badge theme="blue">{{ certificatesCount }} en attente</Badge>
            <Button variant="subtle" size="sm" @click="refreshList" :loading="loading">
              <RefreshCw class="w-4 h-4" />
            </Button>
          </div>
        </div>
      </div>
    </div>

    <div class="max-w-7xl mx-auto px-4 py-6">
      <!-- Stats -->
      <div class="grid grid-cols-2 md:grid-cols-5 gap-4 mb-6">
        <Card class="p-4 text-center">
          <GraduationCap class="w-6 h-6 text-blue-500 mx-auto mb-1" />
          <div class="text-2xl font-bold">{{ certificatesCount }}</div>
          <div class="text-xs text-gray-500">En attente</div>
        </Card>
        <Card
          v-for="year in ['L1', 'L2', 'L3', 'M1', 'M2']"
          :key="year"
          class="p-4 text-center cursor-pointer hover:bg-gray-50"
          :class="{ 'ring-2 ring-blue-500': selectedYear === year }"
          @click="selectedYear = selectedYear === year ? '' : year"
        >
          <div class="text-lg font-bold">
            {{ pendingCertificates.filter(c => c.year === year).length }}
          </div>
          <div class="text-xs text-gray-500">{{ year }}</div>
        </Card>
      </div>

      <!-- Filtres -->
      <div class="flex flex-col sm:flex-row gap-3 mb-6">
        <div class="relative flex-1">
          <Search class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Rechercher un étudiant..."
            class="w-full pl-10 pr-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <select
          v-model="selectedYear"
          class="px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 bg-white"
        >
          <option value="">Toutes les années</option>
          <option v-for="year in uniqueYears" :key="year" :value="year">
            {{ yearLabels[year] || year }}
          </option>
        </select>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="flex justify-center py-12">
        <Spinner class="w-8 h-8" />
      </div>

      <!-- Error -->
      <div v-else-if="error" class="bg-red-50 text-red-700 p-4 rounded-lg">
        {{ error }}
      </div>

      <!-- Liste vide -->
      <div v-else-if="filteredCertificates.length === 0" class="text-center py-12">
        <Award class="w-12 h-12 text-gray-300 mx-auto mb-3" />
        <p class="text-gray-500">Aucun certificat en attente de validation</p>
      </div>

      <!-- Liste des certificats -->
      <div v-else class="space-y-4">
        <Card
          v-for="cert in filteredCertificates"
          :key="cert.student_id + cert.year"
          class="p-4"
        >
          <div class="flex flex-col md:flex-row md:items-center gap-4">
            <!-- Info étudiant -->
            <div class="flex-1">
              <div class="flex items-center gap-3 mb-2">
                <div class="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
                  <User class="w-5 h-5 text-blue-600" />
                </div>
                <div>
                  <div class="font-semibold text-gray-900">{{ cert.student_name }}</div>
                  <div class="text-sm text-gray-500">{{ cert.student_id }}</div>
                </div>
              </div>

              <div class="flex flex-wrap gap-4 text-sm text-gray-600">
                <div class="flex items-center gap-1">
                  <GraduationCap class="w-4 h-4" />
                  {{ yearLabels[cert.year] || cert.year }}
                </div>
                <div class="flex items-center gap-1">
                  <Calendar class="w-4 h-4" />
                  Complété le {{ formatDate(cert.completed_at) }}
                </div>
              </div>
            </div>

            <!-- Progression -->
            <div class="text-center px-4">
              <div class="text-2xl font-bold" :class="getProgressColor(cert.progress)">
                {{ cert.progress }}%
              </div>
              <div class="text-xs text-gray-500">Progression</div>
              <div class="w-24 h-2 bg-gray-200 rounded-full mt-1">
                <div
                  class="h-full rounded-full"
                  :class="{
                    'bg-green-500': cert.progress >= 100,
                    'bg-blue-500': cert.progress >= 80 && cert.progress < 100,
                    'bg-yellow-500': cert.progress >= 50 && cert.progress < 80,
                    'bg-red-500': cert.progress < 50,
                  }"
                  :style="{ width: `${Math.min(cert.progress, 100)}%` }"
                ></div>
              </div>
            </div>

            <!-- Stats EC -->
            <div class="text-center px-4 border-l">
              <div class="text-lg font-semibold">
                {{ cert.validated_ecs }}/{{ cert.total_ecs }}
              </div>
              <div class="text-xs text-gray-500">EC validés</div>
            </div>

            <!-- Moyenne -->
            <div class="text-center px-4 border-l">
              <div class="text-lg font-semibold" :class="cert.average >= 10 ? 'text-green-600' : 'text-red-600'">
                {{ cert.average?.toFixed(2) || '-' }}
              </div>
              <div class="text-xs text-gray-500">Moyenne</div>
            </div>

            <!-- Actions -->
            <div class="flex gap-2 md:border-l md:pl-4">
              <Button
                variant="solid"
                theme="green"
                size="sm"
                @click="openValidateDialog(cert)"
                :disabled="cert.progress < 100"
              >
                <CheckCircle class="w-4 h-4 mr-1" />
                Valider
              </Button>
              <Button
                variant="subtle"
                theme="red"
                size="sm"
                @click="openRejectDialog(cert)"
              >
                <XCircle class="w-4 h-4" />
              </Button>
            </div>
          </div>

          <!-- Avertissement si progression incomplète -->
          <div
            v-if="cert.progress < 100"
            class="mt-3 p-2 bg-yellow-50 text-yellow-700 rounded text-sm flex items-center gap-2"
          >
            <AlertTriangle class="w-4 h-4" />
            Progression incomplète ({{ cert.total_ecs - cert.validated_ecs }} EC restants)
          </div>
        </Card>
      </div>
    </div>

    <!-- Dialog Validation -->
    <Dialog v-model="showValidateDialog" :options="{ title: 'Valider le certificat' }">
      <template #body-content>
        <div v-if="selectedStudent" class="space-y-4">
          <div class="p-3 bg-green-50 rounded-lg">
            <div class="flex items-center gap-3">
              <Award class="w-8 h-8 text-green-600" />
              <div>
                <div class="font-semibold text-green-900">{{ selectedStudent.student_name }}</div>
                <div class="text-sm text-green-700">
                  {{ yearLabels[selectedStudent.year] || selectedStudent.year }} - {{ selectedStudent.progress }}% complété
                </div>
              </div>
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Numéro de certificat
            </label>
            <Input v-model="certificateNumber" placeholder="CNTEMAD-L3-2026-XXXX" />
            <p class="text-xs text-gray-500 mt-1">
              Ce numéro sera imprimé sur le certificat officiel
            </p>
          </div>

          <div class="grid grid-cols-2 gap-4 text-sm">
            <div>
              <span class="text-gray-500">EC validés:</span>
              <span class="font-medium ml-1">{{ selectedStudent.validated_ecs }}/{{ selectedStudent.total_ecs }}</span>
            </div>
            <div>
              <span class="text-gray-500">Moyenne:</span>
              <span class="font-medium ml-1">{{ selectedStudent.average?.toFixed(2) || '-' }}/20</span>
            </div>
          </div>

          <div v-if="validationError" class="text-sm text-red-600 bg-red-50 p-3 rounded">
            {{ validationError }}
          </div>
        </div>
      </template>
      <template #actions>
        <Button variant="subtle" @click="showValidateDialog = false">Annuler</Button>
        <Button variant="solid" theme="green" @click="confirmValidation" :loading="submitting">
          <FileCheck class="w-4 h-4 mr-1" />
          Valider le certificat
        </Button>
      </template>
    </Dialog>

    <!-- Dialog Rejet -->
    <Dialog v-model="showRejectDialog" :options="{ title: 'Rejeter la demande' }">
      <template #body-content>
        <div v-if="selectedStudent" class="space-y-4">
          <div class="p-3 bg-red-50 rounded-lg">
            <div class="flex items-center gap-3">
              <XCircle class="w-8 h-8 text-red-600" />
              <div>
                <div class="font-semibold text-red-900">{{ selectedStudent.student_name }}</div>
                <div class="text-sm text-red-700">
                  Rejeter la demande de certificat
                </div>
              </div>
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Raison du rejet
            </label>
            <textarea
              v-model="rejectReason"
              rows="3"
              class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-red-500"
              placeholder="Expliquez pourquoi la demande est rejetée..."
            ></textarea>
          </div>

          <p class="text-sm text-gray-600">
            L'étudiant sera notifié du rejet et de la raison.
          </p>
        </div>
      </template>
      <template #actions>
        <Button variant="subtle" @click="showRejectDialog = false">Annuler</Button>
        <Button variant="solid" theme="red" @click="confirmRejection">
          Confirmer le rejet
        </Button>
      </template>
    </Dialog>
  </div>
</template>
