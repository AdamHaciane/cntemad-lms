<!--
  CorrectionDetail.vue
  Page de correction détaillée d'une soumission.
  Permet de visualiser le travail, noter et donner un feedback.
-->
<script setup>
import { ref, computed, onMounted } from 'vue'
import { Card, Button, Badge, Dialog, Spinner } from 'frappe-ui'
import {
  ArrowLeft, User, BookOpen, Calendar, Clock, FileText,
  Download, CheckCircle, XCircle, AlertTriangle, Send
} from 'lucide-vue-next'
import { useEvaluator } from '@/composables/useEvaluator'
import { useRoute, useRouter } from 'vue-router'
import GradeInput from '@/components/custom/GradeInput.vue'
import FeedbackEditor from '@/components/custom/FeedbackEditor.vue'

const route = useRoute()
const router = useRouter()

const {
  currentSubmission,
  gradingRubric,
  loading,
  submitting,
  error,
  fetchSubmissionDetail,
  fetchGradingRubric,
  submitGrade,
  getGradeLabel,
  getGradeColor,
  isPassingGrade,
} = useEvaluator()

const grade = ref(10)
const feedback = ref('')
const validateEc = ref(false)
const showConfirmDialog = ref(false)
const showSuccessDialog = ref(false)
const submissionError = ref(null)

const submissionId = computed(() => route.params.id)

onMounted(async () => {
  if (submissionId.value) {
    await fetchSubmissionDetail(submissionId.value)
    if (currentSubmission.value?.ec_id) {
      await fetchGradingRubric(currentSubmission.value.ec_id)
    }
  }
})

const isPassing = computed(() => isPassingGrade(grade.value))

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleDateString('fr-FR', {
    day: '2-digit',
    month: 'long',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

const getFileIcon = (filename) => {
  if (!filename) return FileText
  const ext = filename.split('.').pop()?.toLowerCase()
  // Simplified - could expand with more icons
  return FileText
}

const openConfirmDialog = () => {
  submissionError.value = null
  showConfirmDialog.value = true
}

const confirmSubmission = async () => {
  try {
    await submitGrade(
      submissionId.value,
      grade.value,
      feedback.value,
      validateEc.value
    )
    showConfirmDialog.value = false
    showSuccessDialog.value = true
  } catch (e) {
    submissionError.value = e.message || 'Erreur lors de la soumission'
  }
}

const goBack = () => {
  router.push('/evaluator/corrections')
}

const goToNext = () => {
  showSuccessDialog.value = false
  router.push('/evaluator/corrections')
}

const downloadFile = (url) => {
  window.open(url, '_blank')
}
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="bg-white border-b sticky top-0 z-10">
      <div class="max-w-7xl mx-auto px-4 py-4">
        <div class="flex items-center gap-4">
          <Button variant="ghost" @click="goBack">
            <ArrowLeft class="w-5 h-5" />
          </Button>
          <div class="flex-1">
            <h1 class="text-lg font-bold text-gray-900">Correction</h1>
            <p class="text-sm text-gray-500" v-if="currentSubmission">
              {{ currentSubmission.ec_title }}
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="flex justify-center py-12">
      <Spinner class="w-8 h-8" />
    </div>

    <!-- Error -->
    <div v-else-if="error" class="max-w-7xl mx-auto px-4 py-6">
      <div class="bg-red-50 text-red-700 p-4 rounded-lg">
        {{ error }}
      </div>
    </div>

    <!-- Content -->
    <div v-else-if="currentSubmission" class="max-w-7xl mx-auto px-4 py-6">
      <div class="grid lg:grid-cols-3 gap-6">
        <!-- Colonne principale: Travail étudiant -->
        <div class="lg:col-span-2 space-y-6">
          <!-- Info soumission -->
          <Card class="p-4">
            <div class="flex items-start justify-between">
              <div>
                <div class="flex items-center gap-2 mb-2">
                  <User class="w-5 h-5 text-gray-400" />
                  <span class="font-semibold text-lg">{{ currentSubmission.student_name }}</span>
                </div>
                <div class="text-sm text-gray-600">{{ currentSubmission.student_id }}</div>
              </div>
              <Badge v-if="currentSubmission.days_pending > 5" theme="orange">
                {{ currentSubmission.days_pending }}j d'attente
              </Badge>
            </div>

            <div class="grid grid-cols-2 gap-4 mt-4 text-sm">
              <div class="flex items-center gap-2 text-gray-600">
                <BookOpen class="w-4 h-4" />
                {{ currentSubmission.ec_title }}
              </div>
              <div class="flex items-center gap-2 text-gray-600">
                <Calendar class="w-4 h-4" />
                {{ formatDate(currentSubmission.submitted_at) }}
              </div>
            </div>
          </Card>

          <!-- Consignes / Sujet -->
          <Card v-if="currentSubmission.assignment_instructions" class="p-4">
            <h3 class="font-semibold text-gray-900 mb-2">Consignes de l'exercice</h3>
            <div class="text-sm text-gray-700 prose prose-sm max-w-none"
              v-html="currentSubmission.assignment_instructions">
            </div>
          </Card>

          <!-- Travail soumis -->
          <Card class="p-4">
            <h3 class="font-semibold text-gray-900 mb-4">Travail soumis</h3>

            <!-- Fichiers attachés -->
            <div v-if="currentSubmission.files?.length > 0" class="space-y-2 mb-4">
              <div
                v-for="file in currentSubmission.files"
                :key="file.name"
                class="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
              >
                <div class="flex items-center gap-3">
                  <FileText class="w-5 h-5 text-gray-400" />
                  <div>
                    <div class="font-medium text-gray-900">{{ file.name }}</div>
                    <div class="text-xs text-gray-500">{{ file.size }}</div>
                  </div>
                </div>
                <Button variant="subtle" size="sm" @click="downloadFile(file.url)">
                  <Download class="w-4 h-4" />
                </Button>
              </div>
            </div>

            <!-- Contenu texte -->
            <div v-if="currentSubmission.content" class="prose prose-sm max-w-none">
              <div v-html="currentSubmission.content"></div>
            </div>

            <!-- PDF Viewer -->
            <div v-if="currentSubmission.pdf_url" class="mt-4">
              <iframe
                :src="currentSubmission.pdf_url"
                class="w-full h-96 border rounded"
                title="Document PDF"
              ></iframe>
            </div>

            <!-- Aucun contenu -->
            <div v-if="!currentSubmission.files?.length && !currentSubmission.content && !currentSubmission.pdf_url"
              class="text-center py-8 text-gray-500">
              <FileText class="w-12 h-12 mx-auto mb-2 opacity-50" />
              Aucun contenu soumis
            </div>
          </Card>

          <!-- Barème de notation (si disponible) -->
          <Card v-if="gradingRubric" class="p-4">
            <h3 class="font-semibold text-gray-900 mb-4">Barème de notation</h3>
            <div class="space-y-3">
              <div
                v-for="criterion in gradingRubric.criteria"
                :key="criterion.id"
                class="flex items-start justify-between p-3 bg-gray-50 rounded"
              >
                <div>
                  <div class="font-medium">{{ criterion.name }}</div>
                  <div class="text-sm text-gray-600">{{ criterion.description }}</div>
                </div>
                <Badge>{{ criterion.max_points }} pts</Badge>
              </div>
            </div>
            <div class="mt-4 pt-4 border-t flex justify-between font-semibold">
              <span>Total</span>
              <span>{{ gradingRubric.total_points }} points</span>
            </div>
          </Card>
        </div>

        <!-- Colonne latérale: Notation -->
        <div class="space-y-6">
          <!-- Note -->
          <Card class="p-4 sticky top-20">
            <h3 class="font-semibold text-gray-900 mb-4">Notation</h3>

            <div class="mb-6">
              <label class="block text-sm font-medium text-gray-700 mb-2">Note</label>
              <GradeInput
                v-model="grade"
                scale="0-20"
                :show-slider="true"
                :show-quick-grades="true"
                :show-pass-status="true"
              />
            </div>

            <div class="mb-6">
              <label class="block text-sm font-medium text-gray-700 mb-2">Feedback</label>
              <FeedbackEditor
                v-model="feedback"
                :show-templates="true"
                placeholder="Rédigez votre feedback pour l'étudiant..."
              />
            </div>

            <!-- Option validation EC -->
            <div class="mb-6 p-3 bg-gray-50 rounded-lg">
              <label class="flex items-start gap-3 cursor-pointer">
                <input
                  type="checkbox"
                  v-model="validateEc"
                  class="mt-1 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                />
                <div>
                  <div class="font-medium text-gray-900">Valider l'EC</div>
                  <div class="text-xs text-gray-500">
                    Marquer cet EC comme validé pour l'étudiant (si note suffisante)
                  </div>
                </div>
              </label>
            </div>

            <!-- Résumé -->
            <div class="p-3 rounded-lg mb-4" :class="isPassing ? 'bg-green-50' : 'bg-red-50'">
              <div class="flex items-center gap-2">
                <CheckCircle v-if="isPassing" class="w-5 h-5 text-green-600" />
                <XCircle v-else class="w-5 h-5 text-red-600" />
                <span class="font-medium" :class="isPassing ? 'text-green-700' : 'text-red-700'">
                  {{ grade }}/20 - {{ getGradeLabel(grade) }}
                </span>
              </div>
              <p class="text-sm mt-1" :class="isPassing ? 'text-green-600' : 'text-red-600'">
                {{ isPassing ? 'Note suffisante pour validation' : 'Note insuffisante' }}
              </p>
            </div>

            <!-- Bouton soumettre -->
            <Button
              variant="solid"
              class="w-full"
              :loading="submitting"
              @click="openConfirmDialog"
            >
              <Send class="w-4 h-4 mr-2" />
              Soumettre la correction
            </Button>
          </Card>
        </div>
      </div>
    </div>

    <!-- Dialog Confirmation -->
    <Dialog v-model="showConfirmDialog" :options="{ title: 'Confirmer la correction' }">
      <template #body-content>
        <div class="space-y-4">
          <div class="flex items-center gap-3 p-3 rounded-lg" :class="isPassing ? 'bg-green-50' : 'bg-orange-50'">
            <CheckCircle v-if="isPassing" class="w-6 h-6 text-green-600" />
            <AlertTriangle v-else class="w-6 h-6 text-orange-600" />
            <div>
              <div class="font-medium">Note attribuée: {{ grade }}/20</div>
              <div class="text-sm text-gray-600">{{ getGradeLabel(grade) }}</div>
            </div>
          </div>

          <div v-if="validateEc && isPassing" class="flex items-center gap-2 text-sm text-blue-700 bg-blue-50 p-3 rounded">
            <CheckCircle class="w-4 h-4" />
            L'EC sera marqué comme validé
          </div>

          <div v-if="submissionError" class="text-sm text-red-600 bg-red-50 p-3 rounded">
            {{ submissionError }}
          </div>

          <p class="text-sm text-gray-600">
            Cette action est définitive. L'étudiant sera notifié de sa note et du feedback.
          </p>
        </div>
      </template>
      <template #actions>
        <Button variant="subtle" @click="showConfirmDialog = false">Annuler</Button>
        <Button variant="solid" @click="confirmSubmission" :loading="submitting">
          Confirmer
        </Button>
      </template>
    </Dialog>

    <!-- Dialog Succès -->
    <Dialog v-model="showSuccessDialog" :options="{ title: 'Correction enregistrée' }">
      <template #body-content>
        <div class="text-center py-4">
          <CheckCircle class="w-16 h-16 text-green-500 mx-auto mb-4" />
          <p class="text-lg font-medium text-gray-900">Correction soumise avec succès</p>
          <p class="text-sm text-gray-600 mt-2">
            L'étudiant a été notifié de sa note.
          </p>
        </div>
      </template>
      <template #actions>
        <Button variant="solid" @click="goToNext" class="w-full">
          Retour à la file d'attente
        </Button>
      </template>
    </Dialog>
  </div>
</template>
