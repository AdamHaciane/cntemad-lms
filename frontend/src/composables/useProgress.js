/**
 * Composable pour calculer et tracker la progression EC.
 *
 * Usage:
 *   const {
 *     enrollments,
 *     progress,
 *     progressByYear,
 *     fetchEnrollments,
 *     updateLessonProgress,
 *     isYearComplete
 *   } = useProgress()
 */
import { ref, computed } from 'vue'
import { createResource } from 'frappe-ui'

export function useProgress() {
  const enrollments = ref([])
  const loading = ref(false)
  const error = ref(null)

  // Resources
  const enrollmentsResource = createResource({
    url: 'cntemad_lms.api.student.get_student_progress',
    auto: false,
    onSuccess(data) {
      enrollments.value = data.enrollments || []
    },
    onError(err) {
      error.value = err.message
    },
  })

  const lessonProgressResource = createResource({
    url: 'cntemad_lms.api.ec.update_lesson_progress',
    auto: false,
  })

  // Progression globale
  const progress = computed(() => {
    if (!enrollments.value.length) {
      return { total: 0, validated: 0, inProgress: 0, paid: 0, percent: 0 }
    }

    const total = enrollments.value.length
    const validated = enrollments.value.filter(
      (e) => e.status?.toLowerCase() === 'validated'
    ).length
    const inProgress = enrollments.value.filter(
      (e) => e.status?.toLowerCase() === 'in_progress' || e.status?.toLowerCase() === 'in progress'
    ).length
    const paid = enrollments.value.filter(
      (e) => e.status?.toLowerCase() === 'paid'
    ).length
    const percent = total > 0 ? Math.round((validated / total) * 100) : 0

    return { total, validated, inProgress, paid, percent }
  })

  // Progression par année
  const progressByYear = computed(() => {
    const byYear = {}
    enrollments.value.forEach((e) => {
      const year = e.year || 'Unknown'
      if (!byYear[year]) {
        byYear[year] = { total: 0, validated: 0, inProgress: 0, percent: 0, ecs: [] }
      }
      byYear[year].total++
      byYear[year].ecs.push(e)

      const status = e.status?.toLowerCase()
      if (status === 'validated') {
        byYear[year].validated++
      } else if (status === 'in_progress' || status === 'in progress') {
        byYear[year].inProgress++
      }
    })

    Object.keys(byYear).forEach((year) => {
      byYear[year].percent = byYear[year].total > 0
        ? Math.round((byYear[year].validated / byYear[year].total) * 100)
        : 0
    })

    return byYear
  })

  // Progression par statut
  const enrollmentsByStatus = computed(() => {
    const byStatus = {
      validated: [],
      in_progress: [],
      paid: [],
      not_paid: [],
    }

    enrollments.value.forEach((e) => {
      const status = e.status?.toLowerCase().replace(' ', '_') || 'not_paid'
      if (byStatus[status]) {
        byStatus[status].push(e)
      } else {
        byStatus.not_paid.push(e)
      }
    })

    return byStatus
  })

  // Charger les inscriptions d'un étudiant
  const fetchEnrollments = async (studentId = null) => {
    loading.value = true
    error.value = null

    try {
      await enrollmentsResource.fetch({ student_id: studentId })
    } finally {
      loading.value = false
    }
  }

  // Mettre à jour la progression d'une leçon
  const updateLessonProgress = async (ecId, lessonId, completed = true) => {
    try {
      await lessonProgressResource.fetch({
        ec_id: ecId,
        lesson_id: lessonId,
        completed,
      })
      return lessonProgressResource.data
    } catch (e) {
      error.value = e.message
      throw e
    }
  }

  // Calculer la progression pour un ensemble d'EC
  const calculateProgress = (ecList, completedECs = []) => {
    const total = ecList.length
    const validated = completedECs.filter(
      (ec) => ec.status?.toLowerCase() === 'validated'
    ).length
    const percent = total > 0 ? Math.round((validated / total) * 100) : 0

    return { total, validated, percent }
  }

  // Calculer la progression des leçons dans un EC
  const calculateLessonProgress = (totalLessons, completedLessons = []) => {
    const total = totalLessons
    const completed = completedLessons.length
    const percent = total > 0 ? Math.round((completed / total) * 100) : 0

    return { total, completed, percent }
  }

  // Mettre à jour le statut d'un EC (local)
  const updateECStatus = (ecId, newStatus) => {
    const enrollment = enrollments.value.find((e) => e.ec === ecId || e.name === ecId)
    if (enrollment) {
      enrollment.status = newStatus
    }
  }

  // Vérifier si année complète (pour certificat)
  const isYearComplete = (year) => {
    const yearData = progressByYear.value[year]
    return yearData && yearData.percent === 100
  }

  // Obtenir les ECs à compléter pour une année
  const getRemainingECsForYear = (year) => {
    const yearData = progressByYear.value[year]
    if (!yearData) return []

    return yearData.ecs.filter(
      (e) => e.status?.toLowerCase() !== 'validated'
    )
  }

  // Obtenir le prochain EC recommandé
  const getNextRecommendedEC = () => {
    // Priorité: In Progress > Paid > Not Paid
    const inProgress = enrollmentsByStatus.value.in_progress[0]
    if (inProgress) return inProgress

    const paid = enrollmentsByStatus.value.paid[0]
    if (paid) return paid

    return null
  }

  return {
    // State
    enrollments,
    loading,
    error,

    // Computed
    progress,
    progressByYear,
    enrollmentsByStatus,

    // Methods
    fetchEnrollments,
    updateLessonProgress,
    calculateProgress,
    calculateLessonProgress,
    updateECStatus,
    isYearComplete,
    getRemainingECsForYear,
    getNextRecommendedEC,

    // Resources
    enrollmentsResource,
    lessonProgressResource,
  }
}
