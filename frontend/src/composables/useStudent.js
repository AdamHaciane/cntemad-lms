/**
 * Composable pour gérer les données étudiant connecté.
 *
 * Usage:
 *   const { student, progress, loading, fetchDashboard } = useStudent()
 */
import { ref, computed, onMounted } from 'vue'
import { createResource } from 'frappe-ui'

export function useStudent() {
  const student = ref(null)
  const progress = ref(null)
  const recentActivities = ref([])
  const pendingPayments = ref([])
  const enrollments = ref([])
  const loading = ref(false)
  const error = ref(null)

  // Resource pour le dashboard
  const dashboardResource = createResource({
    url: 'cntemad_lms.api.student.get_student_dashboard',
    auto: false,
    onSuccess(data) {
      student.value = data.student
      progress.value = data.progress
      recentActivities.value = data.recent_activities || []
      pendingPayments.value = data.pending_payments || []
      enrollments.value = data.progress?.enrollments || []
    },
    onError(err) {
      error.value = err.message
    },
  })

  // Resource pour la progression
  const progressResource = createResource({
    url: 'cntemad_lms.api.student.get_student_progress',
    auto: false,
    onSuccess(data) {
      progress.value = data
      enrollments.value = data.enrollments || []
    },
    onError(err) {
      error.value = err.message
    },
  })

  // Computed
  const isLoggedIn = computed(() => !!student.value)

  const progressPercent = computed(() => {
    return progress.value?.progress_percent || 0
  })

  const validatedEC = computed(() => {
    return progress.value?.validated_ec || 0
  })

  const totalEC = computed(() => {
    return progress.value?.total_ec || 0
  })

  const currentYear = computed(() => {
    return student.value?.current_year || progress.value?.current_year || 'L1'
  })

  const hasPendingPayments = computed(() => {
    return pendingPayments.value.length > 0
  })

  // Enrollments par statut
  const enrollmentsByStatus = computed(() => {
    const byStatus = {
      validated: [],
      in_progress: [],
      not_started: [],
      not_paid: [],
    }
    enrollments.value.forEach((e) => {
      const status = e.status?.toLowerCase().replace(' ', '_') || 'not_started'
      if (byStatus[status]) {
        byStatus[status].push(e)
      }
    })
    return byStatus
  })

  // Methods
  const fetchDashboard = async (studentId = null) => {
    loading.value = true
    error.value = null

    try {
      await dashboardResource.fetch({
        student_id: studentId,
      })
    } finally {
      loading.value = false
    }
  }

  const fetchProgress = async (studentId) => {
    loading.value = true
    error.value = null

    try {
      await progressResource.fetch({
        student_id: studentId,
      })
    } finally {
      loading.value = false
    }
  }

  const refreshData = async () => {
    if (student.value?.name) {
      await fetchProgress(student.value.name)
    } else {
      await fetchDashboard()
    }
  }

  return {
    // State
    student,
    progress,
    recentActivities,
    pendingPayments,
    enrollments,
    loading,
    error,

    // Computed
    isLoggedIn,
    progressPercent,
    validatedEC,
    totalEC,
    currentYear,
    hasPendingPayments,
    enrollmentsByStatus,

    // Methods
    fetchDashboard,
    fetchProgress,
    refreshData,

    // Resources (for advanced usage)
    dashboardResource,
    progressResource,
  }
}
