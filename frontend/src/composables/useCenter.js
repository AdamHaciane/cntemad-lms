/**
 * Composable pour gérer les données d'un centre régional (admin).
 *
 * Usage:
 *   const {
 *     center,
 *     dashboard,
 *     students,
 *     payments,
 *     fetchDashboard,
 *     fetchStudents,
 *     fetchPayments,
 *     exportStudents
 *   } = useCenter()
 */
import { ref, computed } from 'vue'
import { createResource } from 'frappe-ui'

export function useCenter() {
  const center = ref(null)
  const dashboard = ref(null)
  const students = ref([])
  const studentsTotal = ref(0)
  const payments = ref([])
  const paymentsTotal = ref(0)
  const paymentStats = ref({})
  const loading = ref(false)
  const error = ref(null)

  // Resources
  const centerResource = createResource({
    url: 'cntemad_lms.api.center.get_my_center',
    auto: false,
    onSuccess(data) {
      center.value = data
    },
    onError(err) {
      error.value = err.message
    },
  })

  const dashboardResource = createResource({
    url: 'cntemad_lms.api.center.get_center_dashboard',
    auto: false,
    onSuccess(data) {
      dashboard.value = data
      center.value = data.center
    },
    onError(err) {
      error.value = err.message
    },
  })

  const studentsResource = createResource({
    url: 'cntemad_lms.api.center.get_center_students',
    auto: false,
    onSuccess(data) {
      students.value = data.students || []
      studentsTotal.value = data.total || 0
    },
    onError(err) {
      error.value = err.message
    },
  })

  const paymentsResource = createResource({
    url: 'cntemad_lms.api.center.get_center_payments',
    auto: false,
    onSuccess(data) {
      payments.value = data.payments || []
      paymentsTotal.value = data.total || 0
      paymentStats.value = data.stats || {}
    },
    onError(err) {
      error.value = err.message
    },
  })

  const exportResource = createResource({
    url: 'cntemad_lms.api.center.export_students',
    auto: false,
  })

  // KPIs calculés
  const kpis = computed(() => {
    if (!dashboard.value?.kpis) return null
    return dashboard.value.kpis
  })

  const trends = computed(() => {
    return dashboard.value?.trends || []
  })

  const alerts = computed(() => {
    return dashboard.value?.alerts || []
  })

  const recentActivity = computed(() => {
    return dashboard.value?.recent_activity || []
  })

  // Formatage montant
  const formatAmount = (amount) => {
    return new Intl.NumberFormat('fr-MG', {
      style: 'decimal',
      minimumFractionDigits: 0,
    }).format(amount) + ' Ar'
  }

  // Charger le centre de l'admin connecté
  const fetchMyCenter = async () => {
    loading.value = true
    error.value = null
    try {
      await centerResource.fetch()
      return center.value
    } finally {
      loading.value = false
    }
  }

  // Charger le dashboard complet
  const fetchDashboard = async (centerId = null) => {
    loading.value = true
    error.value = null
    try {
      await dashboardResource.fetch({ center_id: centerId })
      return dashboard.value
    } finally {
      loading.value = false
    }
  }

  // Charger les étudiants
  const fetchStudents = async (filters = {}) => {
    loading.value = true
    error.value = null
    try {
      await studentsResource.fetch({
        center_id: center.value?.name,
        ...filters,
      })
      return { students: students.value, total: studentsTotal.value }
    } finally {
      loading.value = false
    }
  }

  // Charger les paiements
  const fetchPayments = async (filters = {}) => {
    loading.value = true
    error.value = null
    try {
      await paymentsResource.fetch({
        center_id: center.value?.name,
        ...filters,
      })
      return { payments: payments.value, total: paymentsTotal.value, stats: paymentStats.value }
    } finally {
      loading.value = false
    }
  }

  // Exporter les étudiants
  const exportStudents = async (format = 'csv') => {
    try {
      await exportResource.fetch({
        center_id: center.value?.name,
        format,
      })

      const result = exportResource.data
      if (result?.data) {
        // Download CSV
        const blob = new Blob([result.data], { type: 'text/csv;charset=utf-8;' })
        const link = document.createElement('a')
        link.href = URL.createObjectURL(blob)
        link.download = result.filename || 'export.csv'
        link.click()
        URL.revokeObjectURL(link.href)
      }

      return result
    } catch (e) {
      error.value = e.message
      throw e
    }
  }

  // Stats par statut de paiement
  const getPaymentStatsByStatus = (status) => {
    return paymentStats.value[status] || { count: 0, total: 0 }
  }

  return {
    // State
    center,
    dashboard,
    students,
    studentsTotal,
    payments,
    paymentsTotal,
    paymentStats,
    loading,
    error,

    // Computed
    kpis,
    trends,
    alerts,
    recentActivity,

    // Methods
    fetchMyCenter,
    fetchDashboard,
    fetchStudents,
    fetchPayments,
    exportStudents,
    formatAmount,
    getPaymentStatsByStatus,

    // Resources
    centerResource,
    dashboardResource,
    studentsResource,
    paymentsResource,
  }
}
