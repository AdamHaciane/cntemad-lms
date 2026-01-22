/**
 * Composable pour gérer les données enseignant.
 *
 * Usage:
 *   const {
 *     courses,
 *     currentEC,
 *     ecStats,
 *     fetchMyCourses,
 *     fetchCourseECs,
 *     saveEC,
 *     saveQuiz
 *   } = useTeacher()
 */
import { ref, computed } from 'vue'
import { createResource } from 'frappe-ui'

export function useTeacher() {
  const courses = ref([])
  const courseECs = ref([])
  const currentCourse = ref(null)
  const currentEC = ref(null)
  const ecStats = ref(null)
  const loading = ref(false)
  const saving = ref(false)
  const error = ref(null)

  // Resources
  const coursesResource = createResource({
    url: 'cntemad_lms.api.teacher.get_my_courses',
    auto: false,
    onSuccess(data) {
      courses.value = data.courses || []
    },
    onError(err) {
      error.value = err.message
    },
  })

  const courseECsResource = createResource({
    url: 'cntemad_lms.api.teacher.get_course_ecs',
    auto: false,
    onSuccess(data) {
      courseECs.value = data.ecs || []
      currentCourse.value = data.course
    },
    onError(err) {
      error.value = err.message
    },
  })

  const ecEditResource = createResource({
    url: 'cntemad_lms.api.teacher.get_ec_for_edit',
    auto: false,
    onSuccess(data) {
      currentEC.value = data
    },
    onError(err) {
      error.value = err.message
    },
  })

  const saveECResource = createResource({
    url: 'cntemad_lms.api.teacher.save_ec',
    auto: false,
  })

  const saveContentResource = createResource({
    url: 'cntemad_lms.api.teacher.save_ec_content',
    auto: false,
  })

  const saveQuizResource = createResource({
    url: 'cntemad_lms.api.teacher.save_quiz',
    auto: false,
  })

  const ecStatsResource = createResource({
    url: 'cntemad_lms.api.teacher.get_ec_stats',
    auto: false,
    onSuccess(data) {
      ecStats.value = data
    },
    onError(err) {
      error.value = err.message
    },
  })

  const deleteECResource = createResource({
    url: 'cntemad_lms.api.teacher.delete_ec',
    auto: false,
  })

  // Computed
  const totalStudents = computed(() => {
    return courses.value.reduce((sum, c) => sum + (c.student_count || 0), 0)
  })

  const totalECs = computed(() => {
    return courses.value.reduce((sum, c) => sum + (c.ec_count || 0), 0)
  })

  const publishedCourses = computed(() => {
    return courses.value.filter((c) => c.is_published)
  })

  // Methods
  const fetchMyCourses = async () => {
    loading.value = true
    error.value = null
    try {
      await coursesResource.fetch()
      return courses.value
    } finally {
      loading.value = false
    }
  }

  const fetchCourseECs = async (courseId) => {
    loading.value = true
    error.value = null
    try {
      await courseECsResource.fetch({ course_id: courseId })
      return { ecs: courseECs.value, course: currentCourse.value }
    } finally {
      loading.value = false
    }
  }

  const fetchECForEdit = async (ecId) => {
    loading.value = true
    error.value = null
    try {
      await ecEditResource.fetch({ ec_id: ecId })
      return currentEC.value
    } finally {
      loading.value = false
    }
  }

  const saveEC = async (ecData) => {
    saving.value = true
    error.value = null
    try {
      await saveECResource.fetch(ecData)
      return saveECResource.data
    } catch (e) {
      error.value = e.message
      throw e
    } finally {
      saving.value = false
    }
  }

  const saveECContent = async (ecId, lessons) => {
    saving.value = true
    error.value = null
    try {
      await saveContentResource.fetch({
        ec_id: ecId,
        lessons: JSON.stringify(lessons),
      })
      return saveContentResource.data
    } catch (e) {
      error.value = e.message
      throw e
    } finally {
      saving.value = false
    }
  }

  const saveQuiz = async (ecId, quizData) => {
    saving.value = true
    error.value = null
    try {
      await saveQuizResource.fetch({
        ec_id: ecId,
        quiz_data: JSON.stringify(quizData),
      })
      return saveQuizResource.data
    } catch (e) {
      error.value = e.message
      throw e
    } finally {
      saving.value = false
    }
  }

  const fetchECStats = async (ecId) => {
    loading.value = true
    error.value = null
    try {
      await ecStatsResource.fetch({ ec_id: ecId })
      return ecStats.value
    } finally {
      loading.value = false
    }
  }

  const deleteEC = async (ecId) => {
    saving.value = true
    error.value = null
    try {
      await deleteECResource.fetch({ ec_id: ecId })
      return deleteECResource.data
    } catch (e) {
      error.value = e.message
      throw e
    } finally {
      saving.value = false
    }
  }

  // Format helpers
  const formatAmount = (amount) => {
    return new Intl.NumberFormat('fr-MG', {
      style: 'decimal',
      minimumFractionDigits: 0,
    }).format(amount) + ' Ar'
  }

  return {
    // State
    courses,
    courseECs,
    currentCourse,
    currentEC,
    ecStats,
    loading,
    saving,
    error,

    // Computed
    totalStudents,
    totalECs,
    publishedCourses,

    // Methods
    fetchMyCourses,
    fetchCourseECs,
    fetchECForEdit,
    saveEC,
    saveECContent,
    saveQuiz,
    fetchECStats,
    deleteEC,
    formatAmount,

    // Resources
    coursesResource,
    courseECsResource,
    ecEditResource,
    saveECResource,
    ecStatsResource,
  }
}
