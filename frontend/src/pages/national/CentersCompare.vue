<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="bg-white border-b sticky top-0 z-10">
      <div class="px-4 py-4">
        <div class="flex items-center gap-3">
          <router-link to="/national/dashboard">
            <Button variant="ghost" class="p-2">
              <ArrowLeft class="w-5 h-5" />
            </Button>
          </router-link>
          <div class="flex-1">
            <h1 class="text-xl font-bold text-gray-900">Comparer les centres</h1>
            <p class="text-sm text-gray-500">
              {{ selectedCenterIds.length }} centre(s) sélectionné(s)
            </p>
          </div>
          <Button
            variant="solid"
            @click="runComparison"
            :disabled="selectedCenterIds.length < 2"
            :loading="loading"
          >
            <BarChart3 class="w-4 h-4 mr-2" />
            Comparer
          </Button>
        </div>
      </div>
    </div>

    <div class="p-4 space-y-6">
      <!-- Center selection -->
      <Card>
        <template #title>Sélectionner les centres à comparer</template>
        <div class="p-4">
          <div class="flex flex-wrap gap-2 mb-4">
            <Badge
              v-for="centerId in selectedCenterIds"
              :key="centerId"
              theme="blue"
              class="cursor-pointer"
              @click="toggleCenter(centerId)"
            >
              {{ getCenterName(centerId) }}
              <X class="w-3 h-3 ml-1" />
            </Badge>
            <span v-if="selectedCenterIds.length === 0" class="text-sm text-gray-500">
              Cliquez sur les centres ci-dessous pour les sélectionner
            </span>
          </div>

          <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-2 max-h-60 overflow-y-auto">
            <button
              v-for="center in allCenters"
              :key="center.name"
              class="p-2 text-left text-sm rounded border transition-colors"
              :class="isSelected(center.name)
                ? 'bg-blue-50 border-blue-500 text-blue-700'
                : 'bg-white border-gray-200 hover:border-blue-300'"
              @click="toggleCenter(center.name)"
            >
              <p class="font-medium truncate">{{ center.center_name }}</p>
              <p class="text-xs text-gray-500 truncate">{{ center.region }}</p>
            </button>
          </div>
        </div>
      </Card>

      <!-- Comparison results -->
      <div v-if="comparison" class="space-y-6">
        <!-- Summary cards -->
        <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
          <Card
            v-for="center in comparison.comparisons"
            :key="center.name"
            class="relative"
          >
            <div class="p-4">
              <div class="flex items-start justify-between mb-4">
                <div>
                  <h3 class="font-semibold text-gray-900">
                    {{ center.center_name }}
                  </h3>
                  <p class="text-sm text-gray-500">{{ center.region }}</p>
                </div>
                <Badge
                  v-if="getRank(center.name) === 1"
                  theme="yellow"
                >
                  #1
                </Badge>
              </div>

              <div class="space-y-3">
                <div class="flex justify-between">
                  <span class="text-sm text-gray-500">Étudiants</span>
                  <span class="font-medium">{{ center.student_count }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-sm text-gray-500">Inscriptions</span>
                  <span class="font-medium">{{ center.total_enrollments }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-sm text-gray-500">Taux validation</span>
                  <span class="font-medium text-green-600">
                    {{ center.validation_rate }}%
                  </span>
                </div>
                <div class="flex justify-between">
                  <span class="text-sm text-gray-500">Revenus</span>
                  <span class="font-medium text-emerald-600">
                    {{ formatAmount(center.revenue) }}
                  </span>
                </div>
              </div>
            </div>
          </Card>
        </div>

        <!-- Comparison charts -->
        <Card>
          <template #title>Comparaison visuelle</template>
          <div class="p-4 space-y-6">
            <!-- Students comparison -->
            <div>
              <p class="text-sm font-medium text-gray-700 mb-2">Étudiants</p>
              <div class="space-y-2">
                <div
                  v-for="center in comparison.comparisons"
                  :key="`students-${center.name}`"
                  class="flex items-center gap-3"
                >
                  <span class="text-sm text-gray-600 w-32 truncate">
                    {{ center.center_name }}
                  </span>
                  <div class="flex-1 bg-gray-200 rounded-full h-4">
                    <div
                      class="bg-blue-500 h-4 rounded-full transition-all"
                      :style="{ width: `${getBarPercent(center.student_count, 'student_count')}%` }"
                    ></div>
                  </div>
                  <span class="text-sm font-medium w-16 text-right">
                    {{ center.student_count }}
                  </span>
                </div>
              </div>
            </div>

            <!-- Validation rate comparison -->
            <div>
              <p class="text-sm font-medium text-gray-700 mb-2">Taux de validation</p>
              <div class="space-y-2">
                <div
                  v-for="center in comparison.comparisons"
                  :key="`validation-${center.name}`"
                  class="flex items-center gap-3"
                >
                  <span class="text-sm text-gray-600 w-32 truncate">
                    {{ center.center_name }}
                  </span>
                  <div class="flex-1 bg-gray-200 rounded-full h-4">
                    <div
                      class="bg-green-500 h-4 rounded-full transition-all"
                      :style="{ width: `${center.validation_rate}%` }"
                    ></div>
                  </div>
                  <span class="text-sm font-medium w-16 text-right">
                    {{ center.validation_rate }}%
                  </span>
                </div>
              </div>
            </div>

            <!-- Revenue comparison -->
            <div>
              <p class="text-sm font-medium text-gray-700 mb-2">Revenus</p>
              <div class="space-y-2">
                <div
                  v-for="center in comparison.comparisons"
                  :key="`revenue-${center.name}`"
                  class="flex items-center gap-3"
                >
                  <span class="text-sm text-gray-600 w-32 truncate">
                    {{ center.center_name }}
                  </span>
                  <div class="flex-1 bg-gray-200 rounded-full h-4">
                    <div
                      class="bg-emerald-500 h-4 rounded-full transition-all"
                      :style="{ width: `${getBarPercent(center.revenue, 'revenue')}%` }"
                    ></div>
                  </div>
                  <span class="text-sm font-medium w-20 text-right">
                    {{ formatAmountShort(center.revenue) }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </Card>

        <!-- Ranking table -->
        <Card>
          <template #title>Classement</template>
          <div class="overflow-x-auto">
            <table class="w-full text-sm">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-4 py-3 text-left font-medium text-gray-600">#</th>
                  <th class="px-4 py-3 text-left font-medium text-gray-600">Centre</th>
                  <th class="px-4 py-3 text-right font-medium text-gray-600">Étudiants</th>
                  <th class="px-4 py-3 text-right font-medium text-gray-600">Validation</th>
                  <th class="px-4 py-3 text-right font-medium text-gray-600">Revenus</th>
                </tr>
              </thead>
              <tbody class="divide-y">
                <tr
                  v-for="(center, index) in comparison.comparisons"
                  :key="center.name"
                  class="hover:bg-gray-50"
                >
                  <td class="px-4 py-3">
                    <span
                      class="w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold text-white"
                      :class="getMedalColor(index)"
                    >
                      {{ index + 1 }}
                    </span>
                  </td>
                  <td class="px-4 py-3">
                    <p class="font-medium text-gray-900">{{ center.center_name }}</p>
                    <p class="text-xs text-gray-500">{{ center.region }}</p>
                  </td>
                  <td class="px-4 py-3 text-right">{{ center.student_count }}</td>
                  <td class="px-4 py-3 text-right">
                    <span :class="getValidationColor(center.validation_rate)">
                      {{ center.validation_rate }}%
                    </span>
                  </td>
                  <td class="px-4 py-3 text-right font-medium text-emerald-600">
                    {{ formatAmount(center.revenue) }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </Card>
      </div>

      <!-- Empty state -->
      <div v-else-if="!loading" class="text-center py-12">
        <BarChart3 class="w-16 h-16 text-gray-300 mx-auto mb-4" />
        <h3 class="text-lg font-medium text-gray-900 mb-2">
          Sélectionnez des centres
        </h3>
        <p class="text-gray-500">
          Choisissez au moins 2 centres pour les comparer
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { Button, Card, Badge } from 'frappe-ui'
import { ArrowLeft, BarChart3, X } from 'lucide-vue-next'
import { useNational } from '@/composables/useNational'

const {
  centers: allCenters,
  comparison,
  loading,
  fetchCenters,
  compareCenters,
  formatAmount
} = useNational()

const selectedCenterIds = ref([])

onMounted(() => {
  fetchCenters()
})

const isSelected = (centerId) => {
  return selectedCenterIds.value.includes(centerId)
}

const toggleCenter = (centerId) => {
  const index = selectedCenterIds.value.indexOf(centerId)
  if (index === -1) {
    if (selectedCenterIds.value.length < 6) {
      selectedCenterIds.value.push(centerId)
    }
  } else {
    selectedCenterIds.value.splice(index, 1)
  }
}

const getCenterName = (centerId) => {
  const center = allCenters.value.find(c => c.name === centerId)
  return center?.center_name || centerId
}

const runComparison = async () => {
  if (selectedCenterIds.value.length >= 2) {
    await compareCenters(selectedCenterIds.value)
  }
}

const getRank = (centerId) => {
  if (!comparison.value?.comparisons) return 0
  const index = comparison.value.comparisons.findIndex(c => c.name === centerId)
  return index + 1
}

const getBarPercent = (value, metric) => {
  if (!comparison.value?.comparisons) return 0
  const max = Math.max(...comparison.value.comparisons.map(c => c[metric]), 1)
  return Math.max((value / max) * 100, 5)
}

const getMedalColor = (index) => {
  const colors = ['bg-yellow-500', 'bg-gray-400', 'bg-amber-600']
  return colors[index] || 'bg-blue-500'
}

const getValidationColor = (rate) => {
  if (rate >= 70) return 'text-green-600'
  if (rate >= 50) return 'text-yellow-600'
  return 'text-red-600'
}

const formatAmountShort = (amount) => {
  if (amount >= 1000000) {
    return (amount / 1000000).toFixed(1) + 'M Ar'
  }
  if (amount >= 1000) {
    return (amount / 1000).toFixed(0) + 'K Ar'
  }
  return amount + ' Ar'
}
</script>
