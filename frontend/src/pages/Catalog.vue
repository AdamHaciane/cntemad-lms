<!--
  Catalog.vue
  Page catalogue des EC disponibles à l'achat.

  Utilise:
    - ECCard component
    - FilterBar component
    - useFilters composable
-->
<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { Card, Button, Spinner, Input } from 'frappe-ui'
import { createResource } from 'frappe-ui'
import { useFilters } from '@/composables/useFilters'
import ECCard from '@/components/custom/ECCard.vue'
import FilterBar from '@/components/custom/FilterBar.vue'

const router = useRouter()

// Filters
const { filters, setFilter, resetFilters, hasActiveFilters } = useFilters({
  year: '',
  course: '',
  search: '',
  sort_by: 'title',
})

// Pagination
const page = ref(1)
const limit = 12

// Data
const ecs = ref([])
const total = ref(0)
const hasMore = ref(false)
const loading = ref(false)

// Resources
const catalogResource = createResource({
  url: 'cntemad_lms.api.ec.get_available_ecs',
  auto: false,
  onSuccess(data) {
    if (page.value === 1) {
      ecs.value = data.ecs
    } else {
      ecs.value = [...ecs.value, ...data.ecs]
    }
    total.value = data.total
    hasMore.value = data.has_more
  },
})

const yearsResource = createResource({
  url: 'cntemad_lms.api.ec.get_years',
  auto: true,
})

const coursesResource = createResource({
  url: 'cntemad_lms.api.ec.get_courses_for_filter',
  auto: true,
})

// Computed
const filterConfig = computed(() => [
  {
    key: 'search',
    label: 'Rechercher un EC...',
    type: 'search',
  },
  {
    key: 'year',
    label: 'Année',
    type: 'select',
    options: yearsResource.data || [],
  },
  {
    key: 'course',
    label: 'Cours',
    type: 'select',
    options: coursesResource.data || [],
  },
])

const sortOptions = [
  { value: 'title', label: 'Alphabétique' },
  { value: 'price', label: 'Prix' },
  { value: 'created', label: 'Récents' },
]

// Methods
const fetchECs = async () => {
  loading.value = true
  await catalogResource.fetch({
    year: filters.value.year || null,
    course: filters.value.course || null,
    search: filters.value.search || null,
    sort_by: filters.value.sort_by || 'title',
    limit: limit,
    offset: (page.value - 1) * limit,
  })
  loading.value = false
}

const loadMore = () => {
  page.value++
  fetchECs()
}

const handleFilterChange = () => {
  page.value = 1
  fetchECs()
}

const handleECClick = (ec) => {
  router.push(`/ec/${ec.name || ec.id}`)
}

const navigateTo = (path) => {
  router.push(path)
}

// Watch filters
watch(
  () => filters.value,
  () => {
    handleFilterChange()
  },
  { deep: true }
)

// Mount
onMounted(() => {
  fetchECs()
})
</script>

<template>
  <div class="min-h-screen bg-gray-50 pb-20 md:pb-6">
    <!-- Header -->
    <header class="bg-white border-b px-4 py-4 sticky top-0 z-10">
      <div class="max-w-6xl mx-auto">
        <div class="flex justify-between items-center mb-4">
          <div>
            <h1 class="text-xl font-bold text-gray-900">Catalogue EC</h1>
            <p class="text-sm text-gray-500">{{ total }} EC disponibles</p>
          </div>
          <Button variant="outline" size="sm" @click="navigateTo('/dashboard')">
            ← Retour
          </Button>
        </div>

        <!-- Search -->
        <Input
          v-model="filters.search"
          placeholder="Rechercher un EC..."
          type="search"
          class="w-full"
        />
      </div>
    </header>

    <main class="px-4 py-6">
      <div class="max-w-6xl mx-auto">
        <!-- Filters -->
        <div class="flex flex-wrap gap-3 mb-6">
          <!-- Year filter -->
          <select
            v-model="filters.year"
            class="px-3 py-2 border border-gray-300 rounded-lg text-sm bg-white"
          >
            <option value="">Toutes les années</option>
            <option
              v-for="year in yearsResource.data"
              :key="year.value"
              :value="year.value"
            >
              {{ year.label }}
            </option>
          </select>

          <!-- Course filter -->
          <select
            v-model="filters.course"
            class="px-3 py-2 border border-gray-300 rounded-lg text-sm bg-white"
          >
            <option value="">Tous les cours</option>
            <option
              v-for="course in coursesResource.data"
              :key="course.value"
              :value="course.value"
            >
              {{ course.label }}
            </option>
          </select>

          <!-- Sort -->
          <select
            v-model="filters.sort_by"
            class="px-3 py-2 border border-gray-300 rounded-lg text-sm bg-white"
          >
            <option
              v-for="opt in sortOptions"
              :key="opt.value"
              :value="opt.value"
            >
              {{ opt.label }}
            </option>
          </select>

          <!-- Reset -->
          <Button
            v-if="hasActiveFilters"
            variant="ghost"
            size="sm"
            @click="resetFilters"
          >
            Réinitialiser
          </Button>
        </div>

        <!-- Loading initial -->
        <div v-if="loading && page === 1" class="flex justify-center py-20">
          <Spinner class="w-8 h-8" />
        </div>

        <!-- No results -->
        <Card v-else-if="ecs.length === 0" class="p-8 text-center">
          <div class="text-4xl mb-4">🔍</div>
          <h3 class="font-semibold text-gray-900">Aucun EC trouvé</h3>
          <p class="text-sm text-gray-500 mt-2">
            Essayez de modifier vos filtres
          </p>
          <Button variant="outline" class="mt-4" @click="resetFilters">
            Réinitialiser les filtres
          </Button>
        </Card>

        <!-- EC Grid -->
        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <ECCard
            v-for="ec in ecs"
            :key="ec.name"
            :ec="{
              id: ec.name,
              title: ec.title,
              description: ec.description,
              price: ec.price,
              duration: ec.duration_hours,
              status: ec.user_status || 'not_paid',
              image: ec.image,
            }"
            @click="handleECClick(ec)"
          />
        </div>

        <!-- Load more -->
        <div v-if="hasMore && !loading" class="text-center mt-8">
          <Button variant="outline" @click="loadMore">
            Charger plus
          </Button>
        </div>

        <!-- Loading more -->
        <div v-if="loading && page > 1" class="flex justify-center py-8">
          <Spinner class="w-6 h-6" />
        </div>
      </div>
    </main>

    <!-- Bottom Navigation (Mobile) -->
    <nav class="fixed bottom-0 left-0 right-0 bg-white border-t md:hidden safe-area-bottom">
      <div class="flex justify-around py-2">
        <button
          class="flex flex-col items-center p-2 text-gray-500"
          @click="navigateTo('/dashboard')"
        >
          <span class="text-xl">🏠</span>
          <span class="text-xs">Accueil</span>
        </button>
        <button
          class="flex flex-col items-center p-2 text-gray-500"
          @click="navigateTo('/courses')"
        >
          <span class="text-xl">📚</span>
          <span class="text-xs">Cours</span>
        </button>
        <button
          class="flex flex-col items-center p-2 text-cntemad-primary"
          @click="navigateTo('/catalog')"
        >
          <span class="text-xl">🛒</span>
          <span class="text-xs font-medium">Catalogue</span>
        </button>
        <button
          class="flex flex-col items-center p-2 text-gray-500"
          @click="navigateTo('/profile')"
        >
          <span class="text-xl">👤</span>
          <span class="text-xs">Profil</span>
        </button>
      </div>
    </nav>
  </div>
</template>

<style scoped>
.safe-area-bottom {
  padding-bottom: env(safe-area-inset-bottom);
}
</style>
