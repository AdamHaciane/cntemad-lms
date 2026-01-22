/**
 * Composable pour gérer les données admin national CNTEMAD.
 *
 * Usage:
 *   const {
 *     dashboard,
 *     centers,
 *     mapData,
 *     fetchDashboard,
 *     fetchCenters,
 *     compareCenters,
 *     exportReport
 *   } = useNational()
 */
import { ref, computed } from 'vue'
import { createResource } from 'frappe-ui'

export function useNational() {
  const dashboard = ref(null)
  const centers = ref([])
  const centerDetail = ref(null)
  const comparison = ref(null)
  const mapData = ref(null)
  const loading = ref(false)
  const exporting = ref(false)
  const error = ref(null)

  // Resources
  const dashboardResource = createResource({
    url: 'cntemad_lms.api.national.get_national_dashboard',
    auto: false,
    onSuccess(data) {
      dashboard.value = data
    },
    onError(err) {
      error.value = err.message
    },
  })

  const centersResource = createResource({
    url: 'cntemad_lms.api.national.get_all_centers',
    auto: false,
    onSuccess(data) {
      centers.value = data.centers || []
    },
    onError(err) {
      error.value = err.message
    },
  })

  const centerDetailResource = createResource({
    url: 'cntemad_lms.api.national.get_center_detail',
    auto: false,
    onSuccess(data) {
      centerDetail.value = data
    },
    onError(err) {
      error.value = err.message
    },
  })

  const compareResource = createResource({
    url: 'cntemad_lms.api.national.compare_centers',
    auto: false,
    onSuccess(data) {
      comparison.value = data
    },
    onError(err) {
      error.value = err.message
    },
  })

  const mapResource = createResource({
    url: 'cntemad_lms.api.national.get_centers_map_data',
    auto: false,
    onSuccess(data) {
      mapData.value = data
    },
    onError(err) {
      error.value = err.message
    },
  })

  const exportResource = createResource({
    url: 'cntemad_lms.api.national.export_national_report',
    auto: false,
  })

  // Computed
  const kpis = computed(() => dashboard.value?.kpis || null)

  const trends = computed(() => dashboard.value?.trends || [])

  const alerts = computed(() => dashboard.value?.alerts || [])

  const topCenters = computed(() => dashboard.value?.top_centers || [])

  const recentActivity = computed(() => dashboard.value?.recent_activity || [])

  const centersSummary = computed(() => dashboard.value?.centers_summary || [])

  // Methods
  const fetchDashboard = async () => {
    loading.value = true
    error.value = null
    try {
      await dashboardResource.fetch()
      return dashboard.value
    } finally {
      loading.value = false
    }
  }

  const fetchCenters = async () => {
    loading.value = true
    error.value = null
    try {
      await centersResource.fetch()
      return centers.value
    } finally {
      loading.value = false
    }
  }

  const fetchCenterDetail = async (centerId) => {
    loading.value = true
    error.value = null
    try {
      await centerDetailResource.fetch({ center_id: centerId })
      return centerDetail.value
    } finally {
      loading.value = false
    }
  }

  const compareCenters = async (centerIds) => {
    loading.value = true
    error.value = null
    try {
      await compareResource.fetch({
        center_ids: JSON.stringify(centerIds),
      })
      return comparison.value
    } finally {
      loading.value = false
    }
  }

  const fetchMapData = async () => {
    loading.value = true
    error.value = null
    try {
      await mapResource.fetch()
      return mapData.value
    } finally {
      loading.value = false
    }
  }

  const exportReport = async (reportType, dateFrom = null, dateTo = null, format = 'csv') => {
    exporting.value = true
    error.value = null
    try {
      await exportResource.fetch({
        report_type: reportType,
        date_from: dateFrom,
        date_to: dateTo,
        format,
      })

      const result = exportResource.data
      if (result?.data) {
        // Download file
        const blob = new Blob([result.data], { type: 'text/csv;charset=utf-8;' })
        const link = document.createElement('a')
        link.href = URL.createObjectURL(blob)
        link.download = result.filename || `report_${reportType}.csv`
        link.click()
        URL.revokeObjectURL(link.href)
      }

      return result
    } catch (e) {
      error.value = e.message
      throw e
    } finally {
      exporting.value = false
    }
  }

  // Format helpers
  const formatAmount = (amount) => {
    return new Intl.NumberFormat('fr-MG', {
      style: 'decimal',
      minimumFractionDigits: 0,
    }).format(amount) + ' Ar'
  }

  const formatNumber = (num) => {
    return new Intl.NumberFormat('fr-MG').format(num)
  }

  // Get center by ID
  const getCenterById = (centerId) => {
    return centers.value.find((c) => c.name === centerId) || null
  }

  // Sort centers by metric
  const sortCentersBy = (metric, ascending = false) => {
    return [...centers.value].sort((a, b) => {
      const diff = (a[metric] || 0) - (b[metric] || 0)
      return ascending ? diff : -diff
    })
  }

  return {
    // State
    dashboard,
    centers,
    centerDetail,
    comparison,
    mapData,
    loading,
    exporting,
    error,

    // Computed
    kpis,
    trends,
    alerts,
    topCenters,
    recentActivity,
    centersSummary,

    // Methods
    fetchDashboard,
    fetchCenters,
    fetchCenterDetail,
    compareCenters,
    fetchMapData,
    exportReport,
    formatAmount,
    formatNumber,
    getCenterById,
    sortCentersBy,

    // Resources
    dashboardResource,
    centersResource,
    centerDetailResource,
    compareResource,
    mapResource,
  }
}
