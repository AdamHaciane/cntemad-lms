/**
 * Composable pour gérer les filtres avec persistance URL.
 *
 * Usage:
 *   const { filters, setFilter, resetFilters, buildQuery } = useFilters({
 *     year: '',
 *     status: '',
 *     search: ''
 *   })
 */
import { ref, computed, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

export function useFilters(defaultFilters = {}) {
  const route = useRoute()
  const router = useRouter()

  const filters = ref({ ...defaultFilters })

  // Charger les filtres depuis l'URL au montage
  onMounted(() => {
    Object.keys(defaultFilters).forEach((key) => {
      if (route.query[key]) {
        filters.value[key] = route.query[key]
      }
    })
  })

  // Définir un filtre
  const setFilter = (key, value) => {
    filters.value[key] = value
    updateURL()
  }

  // Définir plusieurs filtres
  const setFilters = (newFilters) => {
    Object.assign(filters.value, newFilters)
    updateURL()
  }

  // Réinitialiser tous les filtres
  const resetFilters = () => {
    filters.value = { ...defaultFilters }
    router.replace({ query: {} })
  }

  // Mettre à jour l'URL
  const updateURL = () => {
    const query = {}
    Object.entries(filters.value).forEach(([key, value]) => {
      if (value && value !== defaultFilters[key]) {
        query[key] = value
      }
    })
    router.replace({ query })
  }

  // Vérifier si des filtres sont actifs
  const hasActiveFilters = computed(() => {
    return Object.entries(filters.value).some(
      ([key, value]) => value && value !== defaultFilters[key]
    )
  })

  // Construire la query string pour l'API
  const buildQuery = computed(() => {
    const params = {}
    Object.entries(filters.value).forEach(([key, value]) => {
      if (value) {
        params[key] = value
      }
    })
    return params
  })

  // Filtrer une liste localement
  const filterList = (list, customFilters = null) => {
    const activeFilters = customFilters || filters.value

    return list.filter((item) => {
      return Object.entries(activeFilters).every(([key, value]) => {
        if (!value) return true

        // Recherche textuelle
        if (key === 'search') {
          const searchFields = ['name', 'title', 'email', 'description']
          return searchFields.some((field) =>
            item[field]?.toLowerCase().includes(value.toLowerCase())
          )
        }

        // Filtre exact
        return item[key] === value
      })
    })
  }

  return {
    filters,
    setFilter,
    setFilters,
    resetFilters,
    hasActiveFilters,
    buildQuery,
    filterList,
  }
}
