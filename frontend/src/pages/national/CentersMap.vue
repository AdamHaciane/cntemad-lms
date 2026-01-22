<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="bg-white border-b sticky top-0 z-20">
      <div class="px-4 py-4">
        <div class="flex items-center gap-3">
          <router-link to="/national/dashboard">
            <Button variant="ghost" class="p-2">
              <ArrowLeft class="w-5 h-5" />
            </Button>
          </router-link>
          <div class="flex-1">
            <h1 class="text-xl font-bold text-gray-900">Carte des centres</h1>
            <p class="text-sm text-gray-500">
              {{ mapData?.centers?.length || 0 }} centres CNTEMAD
            </p>
          </div>
          <Button variant="outline" @click="toggleView">
            <component :is="viewMode === 'map' ? List : Map" class="w-4 h-4 mr-2" />
            {{ viewMode === 'map' ? 'Liste' : 'Carte' }}
          </Button>
        </div>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="flex justify-center py-12">
      <Spinner class="w-8 h-8" />
    </div>

    <!-- Map View -->
    <div v-else-if="viewMode === 'map'" class="relative">
      <!-- Map container -->
      <div ref="mapContainer" class="w-full h-[calc(100vh-80px)]"></div>

      <!-- Selected center panel -->
      <div
        v-if="selectedCenter"
        class="absolute bottom-4 left-4 right-4 md:left-auto md:right-4 md:w-80 bg-white rounded-lg shadow-lg z-10"
      >
        <div class="p-4">
          <div class="flex items-start justify-between">
            <div>
              <h3 class="font-semibold text-gray-900">
                {{ selectedCenter.center_name }}
              </h3>
              <p class="text-sm text-gray-500">{{ selectedCenter.region }}</p>
            </div>
            <button
              class="text-gray-400 hover:text-gray-600"
              @click="selectedCenter = null"
            >
              <X class="w-5 h-5" />
            </button>
          </div>

          <div class="mt-4 grid grid-cols-2 gap-4">
            <div class="text-center p-2 bg-gray-50 rounded">
              <p class="text-xl font-bold text-blue-600">
                {{ selectedCenter.student_count }}
              </p>
              <p class="text-xs text-gray-500">Étudiants</p>
            </div>
            <div class="text-center p-2 bg-gray-50 rounded">
              <p class="text-xl font-bold text-green-600">
                {{ formatAmount(selectedCenter.revenue) }}
              </p>
              <p class="text-xs text-gray-500">Revenus</p>
            </div>
          </div>

          <router-link
            :to="`/national/center/${selectedCenter.name}`"
            class="block mt-4"
          >
            <Button variant="solid" class="w-full">
              Voir détails
            </Button>
          </router-link>
        </div>
      </div>

      <!-- Legend -->
      <div class="absolute top-4 right-4 bg-white rounded-lg shadow p-3 z-10">
        <p class="text-xs font-medium text-gray-700 mb-2">Taille = Étudiants</p>
        <div class="flex items-center gap-2 text-xs text-gray-500">
          <span class="w-3 h-3 bg-blue-500 rounded-full"></span>
          <span>Centre actif</span>
        </div>
      </div>
    </div>

    <!-- List View -->
    <div v-else class="p-4">
      <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
        <Card
          v-for="center in sortedCenters"
          :key="center.name"
          class="cursor-pointer hover:shadow-md transition-shadow"
          @click="selectCenter(center)"
        >
          <div class="p-4">
            <div class="flex items-start justify-between">
              <div>
                <h3 class="font-semibold text-gray-900">
                  {{ center.center_name }}
                </h3>
                <p class="text-sm text-gray-500">{{ center.region }}</p>
              </div>
              <MapPin class="w-5 h-5 text-blue-500" />
            </div>

            <div class="mt-4 flex items-center justify-between text-sm">
              <div class="flex items-center gap-1 text-gray-600">
                <Users class="w-4 h-4" />
                {{ center.student_count }}
              </div>
              <span class="font-medium text-green-600">
                {{ formatAmount(center.revenue) }}
              </span>
            </div>

            <div class="mt-2">
              <div class="flex items-center justify-between text-xs text-gray-500 mb-1">
                <span>Validation</span>
                <span>{{ center.validation_rate }}%</span>
              </div>
              <div class="w-full bg-gray-200 rounded-full h-1.5">
                <div
                  class="bg-green-500 h-1.5 rounded-full"
                  :style="{ width: `${center.validation_rate}%` }"
                ></div>
              </div>
            </div>
          </div>
        </Card>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'
import { Button, Card, Spinner } from 'frappe-ui'
import { ArrowLeft, Map, List, X, MapPin, Users } from 'lucide-vue-next'
import { useNational } from '@/composables/useNational'

// Try to import Leaflet dynamically
let L = null

const { mapData, loading, fetchMapData, formatAmount } = useNational()

const mapContainer = ref(null)
const mapInstance = ref(null)
const viewMode = ref('map')
const selectedCenter = ref(null)

const sortedCenters = computed(() => {
  if (!mapData.value?.centers) return []
  return [...mapData.value.centers].sort((a, b) => b.revenue - a.revenue)
})

onMounted(async () => {
  await fetchMapData()

  // Try to load Leaflet
  try {
    L = await import('leaflet')
    await import('leaflet/dist/leaflet.css')

    // Fix default marker icon
    delete L.Icon.Default.prototype._getIconUrl
    L.Icon.Default.mergeOptions({
      iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png',
      iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png',
      shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
    })

    nextTick(() => {
      initMap()
    })
  } catch (e) {
    console.warn('Leaflet not available, using list view')
    viewMode.value = 'list'
  }
})

onUnmounted(() => {
  if (mapInstance.value) {
    mapInstance.value.remove()
  }
})

watch(viewMode, (newMode) => {
  if (newMode === 'map' && L && !mapInstance.value) {
    nextTick(() => {
      initMap()
    })
  }
})

const initMap = () => {
  if (!mapContainer.value || !L || mapInstance.value) return

  // Initialize map centered on Madagascar
  mapInstance.value = L.map(mapContainer.value).setView([-18.8792, 47.5079], 6)

  // Add tile layer
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
  }).addTo(mapInstance.value)

  // Add markers for each center
  if (mapData.value?.centers) {
    addMarkers()
  }
}

const addMarkers = () => {
  if (!mapInstance.value || !L || !mapData.value?.centers) return

  const maxStudents = Math.max(...mapData.value.centers.map(c => c.student_count), 1)

  mapData.value.centers.forEach(center => {
    if (!center.latitude || !center.longitude) return

    // Calculate marker size based on student count
    const size = Math.max(20, Math.min(50, (center.student_count / maxStudents) * 50))

    // Create custom icon
    const icon = L.divIcon({
      className: 'custom-marker',
      html: `
        <div style="
          width: ${size}px;
          height: ${size}px;
          background: rgba(59, 130, 246, 0.8);
          border: 2px solid white;
          border-radius: 50%;
          box-shadow: 0 2px 8px rgba(0,0,0,0.3);
          display: flex;
          align-items: center;
          justify-content: center;
          color: white;
          font-size: ${size / 3}px;
          font-weight: bold;
        ">
          ${center.student_count > 99 ? '99+' : center.student_count}
        </div>
      `,
      iconSize: [size, size],
      iconAnchor: [size / 2, size / 2]
    })

    const marker = L.marker([center.latitude, center.longitude], { icon })
      .addTo(mapInstance.value)

    marker.on('click', () => {
      selectedCenter.value = center
    })

    // Tooltip
    marker.bindTooltip(center.center_name, {
      permanent: false,
      direction: 'top'
    })
  })

  // Fit bounds if centers have coordinates
  const validCenters = mapData.value.centers.filter(c => c.latitude && c.longitude)
  if (validCenters.length > 0) {
    const bounds = L.latLngBounds(validCenters.map(c => [c.latitude, c.longitude]))
    mapInstance.value.fitBounds(bounds, { padding: [50, 50] })
  }
}

const toggleView = () => {
  viewMode.value = viewMode.value === 'map' ? 'list' : 'map'
}

const selectCenter = (center) => {
  selectedCenter.value = center

  if (viewMode.value === 'map' && mapInstance.value && center.latitude && center.longitude) {
    mapInstance.value.setView([center.latitude, center.longitude], 10)
  }
}
</script>

<style>
.custom-marker {
  background: transparent !important;
  border: none !important;
}
</style>
