<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="bg-white border-b sticky top-0 z-10">
      <div class="px-4 py-4">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-xl font-bold text-gray-900">Mes Cours</h1>
            <p class="text-sm text-gray-500">
              {{ courses.length }} cours • {{ totalECs }} EC • {{ totalStudents }} étudiant(s)
            </p>
          </div>
          <Button variant="solid" @click="showCreateCourse = true">
            <Plus class="w-4 h-4 mr-2" />
            Nouveau cours
          </Button>
        </div>
      </div>
    </div>

    <!-- Content -->
    <div class="p-4">
      <!-- Loading -->
      <div v-if="loading" class="flex justify-center py-12">
        <Spinner class="w-8 h-8" />
      </div>

      <!-- Course list -->
      <div v-else-if="courses.length > 0" class="space-y-4">
        <Card
          v-for="course in courses"
          :key="course.name"
          class="cursor-pointer hover:shadow-md transition-shadow"
          @click="openCourse(course)"
        >
          <div class="p-4">
            <div class="flex items-start gap-4">
              <!-- Image -->
              <div class="w-20 h-20 bg-gray-200 rounded-lg overflow-hidden flex-shrink-0">
                <img
                  v-if="course.image"
                  :src="course.image"
                  :alt="course.title"
                  class="w-full h-full object-cover"
                />
                <div v-else class="w-full h-full flex items-center justify-center">
                  <BookOpen class="w-8 h-8 text-gray-400" />
                </div>
              </div>

              <!-- Info -->
              <div class="flex-1 min-w-0">
                <div class="flex items-start justify-between gap-2">
                  <div>
                    <h3 class="font-semibold text-gray-900">{{ course.title }}</h3>
                    <Badge :theme="course.is_published ? 'green' : 'gray'" class="mt-1">
                      {{ course.is_published ? 'Publié' : 'Brouillon' }}
                    </Badge>
                  </div>
                  <Badge variant="subtle" theme="blue">{{ course.year }}</Badge>
                </div>

                <p class="text-sm text-gray-500 mt-2 line-clamp-2">
                  {{ course.description || 'Pas de description' }}
                </p>

                <!-- Stats -->
                <div class="flex items-center gap-4 mt-3 text-sm text-gray-500">
                  <span class="flex items-center gap-1">
                    <Layers class="w-4 h-4" />
                    {{ course.ec_count }} EC
                  </span>
                  <span class="flex items-center gap-1">
                    <Users class="w-4 h-4" />
                    {{ course.student_count }} étudiant(s)
                  </span>
                </div>
              </div>

              <ChevronRight class="w-5 h-5 text-gray-400 flex-shrink-0" />
            </div>
          </div>
        </Card>
      </div>

      <!-- Empty state -->
      <div v-else class="text-center py-12">
        <BookOpen class="w-16 h-16 text-gray-300 mx-auto mb-4" />
        <h3 class="text-lg font-medium text-gray-900 mb-2">Aucun cours</h3>
        <p class="text-gray-500 mb-4">Créez votre premier cours pour commencer</p>
        <Button variant="solid" @click="showCreateCourse = true">
          <Plus class="w-4 h-4 mr-2" />
          Créer un cours
        </Button>
      </div>
    </div>

    <!-- Create Course Dialog -->
    <Dialog v-model="showCreateCourse" :options="{ title: 'Nouveau cours' }">
      <template #body-content>
        <div class="space-y-4">
          <Input
            v-model="newCourse.title"
            label="Titre du cours"
            placeholder="Introduction à la programmation"
            required
          />
          <Textarea
            v-model="newCourse.description"
            label="Description"
            placeholder="Décrivez votre cours..."
            rows="3"
          />
          <Select
            v-model="newCourse.year"
            :options="yearOptions"
            label="Année"
          />
        </div>
      </template>
      <template #actions>
        <Button variant="outline" @click="showCreateCourse = false">Annuler</Button>
        <Button
          variant="solid"
          @click="createCourse"
          :loading="creating"
          :disabled="!newCourse.title"
        >
          Créer
        </Button>
      </template>
    </Dialog>

    <!-- Course Detail / EC List Dialog -->
    <Dialog
      v-model="showCourseDetail"
      :options="{ title: selectedCourse?.title, size: 'xl' }"
    >
      <template #body-content>
        <div v-if="selectedCourse" class="space-y-4">
          <!-- Course actions -->
          <div class="flex items-center justify-between">
            <Badge :theme="selectedCourse.is_published ? 'green' : 'gray'">
              {{ selectedCourse.is_published ? 'Publié' : 'Brouillon' }}
            </Badge>
            <Button variant="solid" size="sm" @click="openCreateEC">
              <Plus class="w-4 h-4 mr-1" />
              Nouvel EC
            </Button>
          </div>

          <!-- EC List -->
          <div v-if="loadingECs" class="flex justify-center py-8">
            <Spinner class="w-6 h-6" />
          </div>

          <div v-else-if="courseECs.length > 0" class="divide-y">
            <div
              v-for="ec in courseECs"
              :key="ec.name"
              class="py-3 flex items-center gap-3"
            >
              <div class="flex-1">
                <p class="font-medium text-gray-900">{{ ec.title }}</p>
                <div class="flex items-center gap-3 text-sm text-gray-500 mt-1">
                  <span>{{ formatAmount(ec.price) }}</span>
                  <span>{{ ec.student_count }} inscrit(s)</span>
                  <span>{{ ec.validation_rate }}% validé</span>
                </div>
              </div>
              <Badge :theme="ec.is_published ? 'green' : 'gray'" size="sm">
                {{ ec.is_published ? 'Publié' : 'Brouillon' }}
              </Badge>
              <div class="flex items-center gap-1">
                <Button
                  variant="ghost"
                  size="sm"
                  @click="openEditEC(ec)"
                  title="Modifier"
                >
                  <Edit class="w-4 h-4" />
                </Button>
                <Button
                  variant="ghost"
                  size="sm"
                  @click="openECStats(ec)"
                  title="Statistiques"
                >
                  <BarChart class="w-4 h-4" />
                </Button>
              </div>
            </div>
          </div>

          <div v-else class="text-center py-8 text-gray-500">
            Aucun EC dans ce cours
          </div>
        </div>
      </template>
    </Dialog>

    <!-- EC Editor Dialog -->
    <Dialog
      v-model="showECEditor"
      :options="{ title: editingEC?.name ? 'Modifier l\\'EC' : 'Nouvel EC', size: '2xl' }"
    >
      <template #body-content>
        <div class="space-y-6">
          <!-- Tabs -->
          <div class="flex border-b">
            <button
              v-for="tab in ecTabs"
              :key="tab.id"
              class="px-4 py-2 text-sm font-medium border-b-2 transition-colors"
              :class="activeECTab === tab.id
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700'"
              @click="activeECTab = tab.id"
            >
              {{ tab.label }}
            </button>
          </div>

          <!-- Tab content -->
          <div v-show="activeECTab === 'info'" class="space-y-4">
            <Input
              v-model="editingEC.title"
              label="Titre de l'EC"
              placeholder="Algorithmes et structures de données"
              required
            />
            <Textarea
              v-model="editingEC.description"
              label="Description"
              placeholder="Ce que l'étudiant va apprendre..."
              rows="3"
            />
            <div class="grid grid-cols-2 gap-4">
              <Input
                v-model.number="editingEC.price"
                type="number"
                label="Prix (Ariary)"
                min="0"
              />
              <Input
                v-model.number="editingEC.duration_hours"
                type="number"
                label="Durée (heures)"
                min="0"
              />
            </div>
            <div class="flex items-center gap-2">
              <input
                type="checkbox"
                v-model="editingEC.is_published"
                id="ec-published"
                class="rounded"
              />
              <label for="ec-published" class="text-sm text-gray-700">
                Publier cet EC
              </label>
            </div>
          </div>

          <div v-show="activeECTab === 'content'" class="space-y-4">
            <ContentEditor v-model="editingEC.content" />
          </div>

          <div v-show="activeECTab === 'media'" class="space-y-4">
            <p class="text-sm text-gray-500">
              Ajoutez des fichiers PDF ou vidéos pour enrichir le contenu.
            </p>
            <MediaUpload
              v-model="editingEC.media"
              accept="pdf,video"
              :multiple="true"
            />
          </div>

          <div v-show="activeECTab === 'quiz'" class="space-y-4">
            <QuizBuilder v-model="editingEC.quiz" />
          </div>
        </div>
      </template>
      <template #actions>
        <Button variant="outline" @click="showECEditor = false">Annuler</Button>
        <Button
          variant="solid"
          @click="saveEC"
          :loading="savingEC"
          :disabled="!editingEC.title"
        >
          Enregistrer
        </Button>
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Button, Card, Badge, Input, Textarea, Select, Dialog, Spinner } from 'frappe-ui'
import {
  Plus,
  BookOpen,
  Layers,
  Users,
  ChevronRight,
  Edit,
  BarChart
} from 'lucide-vue-next'
import ContentEditor from '@/components/custom/ContentEditor.vue'
import MediaUpload from '@/components/custom/MediaUpload.vue'
import QuizBuilder from '@/components/custom/QuizBuilder.vue'
import { useTeacher } from '@/composables/useTeacher'

const router = useRouter()

const {
  courses,
  courseECs,
  totalStudents,
  totalECs,
  loading,
  fetchMyCourses,
  fetchCourseECs,
  saveEC: saveECApi,
  saveQuiz: saveQuizApi,
  formatAmount
} = useTeacher()

// State
const showCreateCourse = ref(false)
const showCourseDetail = ref(false)
const showECEditor = ref(false)
const creating = ref(false)
const loadingECs = ref(false)
const savingEC = ref(false)

const selectedCourse = ref(null)
const activeECTab = ref('info')

const newCourse = ref({
  title: '',
  description: '',
  year: 'L1'
})

const editingEC = ref({
  name: null,
  title: '',
  description: '',
  price: 0,
  duration_hours: 0,
  content: '',
  media: [],
  quiz: {
    title: '',
    passing_percentage: 70,
    max_attempts: 3,
    time_limit: 0,
    questions: []
  },
  is_published: false
})

const yearOptions = [
  { label: 'Licence 1', value: 'L1' },
  { label: 'Licence 2', value: 'L2' },
  { label: 'Licence 3', value: 'L3' },
  { label: 'Master 1', value: 'M1' },
  { label: 'Master 2', value: 'M2' }
]

const ecTabs = [
  { id: 'info', label: 'Informations' },
  { id: 'content', label: 'Contenu' },
  { id: 'media', label: 'Médias' },
  { id: 'quiz', label: 'Quiz' }
]

onMounted(() => {
  fetchMyCourses()
})

const openCourse = async (course) => {
  selectedCourse.value = course
  showCourseDetail.value = true
  loadingECs.value = true
  try {
    await fetchCourseECs(course.name)
  } finally {
    loadingECs.value = false
  }
}

const createCourse = async () => {
  // For now, we'll just close the dialog
  // Course creation would need a separate API
  creating.value = true
  try {
    // await createCourseApi(newCourse.value)
    showCreateCourse.value = false
    newCourse.value = { title: '', description: '', year: 'L1' }
    fetchMyCourses()
  } finally {
    creating.value = false
  }
}

const openCreateEC = () => {
  editingEC.value = {
    name: null,
    course: selectedCourse.value?.name,
    title: '',
    description: '',
    price: 0,
    duration_hours: 0,
    content: '',
    media: [],
    quiz: {
      title: '',
      passing_percentage: 70,
      max_attempts: 3,
      time_limit: 0,
      questions: []
    },
    is_published: false
  }
  activeECTab.value = 'info'
  showECEditor.value = true
}

const openEditEC = (ec) => {
  editingEC.value = {
    name: ec.name,
    course: selectedCourse.value?.name,
    title: ec.title,
    description: ec.description || '',
    price: ec.price || 0,
    duration_hours: ec.duration_hours || 0,
    content: ec.content || '',
    media: [],
    quiz: ec.quiz || {
      title: '',
      passing_percentage: 70,
      max_attempts: 3,
      time_limit: 0,
      questions: []
    },
    is_published: ec.is_published
  }
  activeECTab.value = 'info'
  showECEditor.value = true
}

const openECStats = (ec) => {
  router.push(`/teacher/ec/${ec.name}/stats`)
}

const saveEC = async () => {
  savingEC.value = true
  try {
    // Save EC info
    const result = await saveECApi({
      ec_id: editingEC.value.name,
      title: editingEC.value.title,
      description: editingEC.value.description,
      course: editingEC.value.course,
      price: editingEC.value.price,
      duration_hours: editingEC.value.duration_hours,
      content: editingEC.value.content,
      is_published: editingEC.value.is_published
    })

    // Save quiz if has questions
    if (editingEC.value.quiz?.questions?.length > 0) {
      await saveQuizApi(result.name, editingEC.value.quiz)
    }

    showECEditor.value = false
    // Refresh EC list
    await fetchCourseECs(selectedCourse.value.name)
  } finally {
    savingEC.value = false
  }
}
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
