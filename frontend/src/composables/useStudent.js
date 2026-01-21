/**
 * Composable pour gérer les données étudiant.
 *
 * Usage:
 *   const { student, progress, loading, fetchProgress } = useStudent()
 */
import { ref, computed } from 'vue'

export function useStudent() {
  const student = ref(null)
  const progress = ref(null)
  const loading = ref(false)
  const error = ref(null)

  const isLoggedIn = computed(() => !!student.value)

  const fetchStudent = async () => {
    loading.value = true
    error.value = null

    try {
      // TODO: Use frappe.call
      // const res = await frappe.call({
      //   method: 'cntemad_lms.api.student.get_student_dashboard'
      // })
      // student.value = res.message.student
      // progress.value = res.message.progress
    } catch (e) {
      error.value = e.message
    } finally {
      loading.value = false
    }
  }

  const fetchProgress = async (studentId) => {
    loading.value = true

    try {
      // TODO: Use frappe.call
      // const res = await frappe.call({
      //   method: 'cntemad_lms.api.student.get_student_progress',
      //   args: { student_id: studentId }
      // })
      // progress.value = res.message
    } catch (e) {
      error.value = e.message
    } finally {
      loading.value = false
    }
  }

  return {
    student,
    progress,
    loading,
    error,
    isLoggedIn,
    fetchStudent,
    fetchProgress,
  }
}
