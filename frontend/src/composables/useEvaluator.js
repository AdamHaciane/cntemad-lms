/**
 * Composable pour gérer les opérations de l'évaluateur.
 *
 * Usage:
 *   const {
 *     dashboard,
 *     pendingCorrections,
 *     pendingCertificates,
 *     fetchDashboard,
 *     submitGrade,
 *     validateCertificate
 *   } = useEvaluator()
 */
import { ref, computed } from 'vue'
import { createResource } from 'frappe-ui'

export function useEvaluator() {
  const dashboard = ref(null)
  const pendingCorrections = ref([])
  const recentCorrections = ref([])
  const pendingCertificates = ref([])
  const currentSubmission = ref(null)
  const gradingRubric = ref(null)
  const loading = ref(false)
  const submitting = ref(false)
  const error = ref(null)

  // Resources
  const dashboardResource = createResource({
    url: 'cntemad_lms.api.evaluator.get_evaluator_dashboard',
    auto: false,
    onSuccess(data) {
      dashboard.value = data
      pendingCorrections.value = data.pending_corrections || []
      recentCorrections.value = data.recent_corrections || []
      pendingCertificates.value = data.pending_certificates || []
    },
    onError(err) {
      error.value = err.message
    },
  })

  const correctionsResource = createResource({
    url: 'cntemad_lms.api.evaluator.get_pending_corrections',
    auto: false,
    onSuccess(data) {
      pendingCorrections.value = data || []
    },
    onError(err) {
      error.value = err.message
    },
  })

  const submissionResource = createResource({
    url: 'cntemad_lms.api.evaluator.get_submission_detail',
    auto: false,
    onSuccess(data) {
      currentSubmission.value = data
    },
    onError(err) {
      error.value = err.message
    },
  })

  const gradeResource = createResource({
    url: 'cntemad_lms.api.evaluator.submit_grade',
    auto: false,
  })

  const certificatesResource = createResource({
    url: 'cntemad_lms.api.evaluator.get_pending_certificates',
    auto: false,
    onSuccess(data) {
      pendingCertificates.value = data || []
    },
    onError(err) {
      error.value = err.message
    },
  })

  const validateCertResource = createResource({
    url: 'cntemad_lms.api.evaluator.validate_certificate',
    auto: false,
  })

  const rubricResource = createResource({
    url: 'cntemad_lms.api.evaluator.get_grading_rubric',
    auto: false,
    onSuccess(data) {
      gradingRubric.value = data
    },
    onError(err) {
      error.value = err.message
    },
  })

  // Computed
  const stats = computed(() => dashboard.value?.stats || null)

  const evaluator = computed(() => dashboard.value?.evaluator || null)

  const pendingCount = computed(() => stats.value?.pending_count || 0)

  const certificatesCount = computed(() => pendingCertificates.value.length)

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

  const fetchPendingCorrections = async (limit = 20, offset = 0) => {
    loading.value = true
    error.value = null
    try {
      await correctionsResource.fetch({ limit, offset })
      return pendingCorrections.value
    } finally {
      loading.value = false
    }
  }

  const fetchSubmissionDetail = async (submissionId) => {
    loading.value = true
    error.value = null
    try {
      await submissionResource.fetch({ submission_id: submissionId })
      return currentSubmission.value
    } finally {
      loading.value = false
    }
  }

  const fetchGradingRubric = async (ecId = null) => {
    try {
      await rubricResource.fetch({ ec_id: ecId })
      return gradingRubric.value
    } catch (e) {
      error.value = e.message
      return null
    }
  }

  const submitGrade = async (submissionId, grade, feedback = null, validateEc = false) => {
    submitting.value = true
    error.value = null
    try {
      await gradeResource.fetch({
        submission_id: submissionId,
        grade,
        feedback,
        validate_ec: validateEc,
      })
      return gradeResource.data
    } catch (e) {
      error.value = e.message
      throw e
    } finally {
      submitting.value = false
    }
  }

  const fetchPendingCertificates = async (limit = 20) => {
    loading.value = true
    error.value = null
    try {
      await certificatesResource.fetch({ limit })
      return pendingCertificates.value
    } finally {
      loading.value = false
    }
  }

  const validateCertificate = async (studentId, year, certificateNumber = null) => {
    submitting.value = true
    error.value = null
    try {
      await validateCertResource.fetch({
        student_id: studentId,
        year,
        certificate_number: certificateNumber,
      })
      return validateCertResource.data
    } catch (e) {
      error.value = e.message
      throw e
    } finally {
      submitting.value = false
    }
  }

  // Grade helpers
  const getGradeLabel = (grade, scale = '0-20') => {
    if (scale === '0-20') {
      if (grade >= 19) return 'Excellent'
      if (grade >= 16) return 'Très bien'
      if (grade >= 13) return 'Bien'
      if (grade >= 10) return 'Assez bien'
      if (grade >= 6) return 'Passable'
      return 'Insuffisant'
    }
    // 0-100 scale
    if (grade >= 90) return 'Excellent'
    if (grade >= 80) return 'Très bien'
    if (grade >= 70) return 'Bien'
    if (grade >= 60) return 'Assez bien'
    if (grade >= 50) return 'Passable'
    return 'Insuffisant'
  }

  const getGradeColor = (grade, scale = '0-20') => {
    const passing = scale === '0-20' ? 10 : 50
    if (grade >= passing * 1.6) return 'text-green-600'
    if (grade >= passing * 1.3) return 'text-blue-600'
    if (grade >= passing) return 'text-yellow-600'
    return 'text-red-600'
  }

  const isPassingGrade = (grade, scale = '0-20') => {
    return grade >= (scale === '0-20' ? 10 : 50)
  }

  return {
    // State
    dashboard,
    pendingCorrections,
    recentCorrections,
    pendingCertificates,
    currentSubmission,
    gradingRubric,
    loading,
    submitting,
    error,

    // Computed
    stats,
    evaluator,
    pendingCount,
    certificatesCount,

    // Methods
    fetchDashboard,
    fetchPendingCorrections,
    fetchSubmissionDetail,
    fetchGradingRubric,
    submitGrade,
    fetchPendingCertificates,
    validateCertificate,

    // Helpers
    getGradeLabel,
    getGradeColor,
    isPassingGrade,

    // Resources
    dashboardResource,
    correctionsResource,
    submissionResource,
    certificatesResource,
  }
}
