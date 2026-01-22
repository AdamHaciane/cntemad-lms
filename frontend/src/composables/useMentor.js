/**
 * Composable pour gérer les opérations du mentor.
 *
 * Usage:
 *   const {
 *     dashboard,
 *     mentees,
 *     alerts,
 *     messages,
 *     fetchDashboard,
 *     fetchMentees,
 *     sendMessage
 *   } = useMentor()
 */
import { ref, computed } from 'vue'
import { createResource } from 'frappe-ui'

export function useMentor() {
  const dashboard = ref(null)
  const mentees = ref([])
  const currentMentee = ref(null)
  const messages = ref([])
  const conversations = ref([])
  const alerts = ref([])
  const loading = ref(false)
  const sending = ref(false)
  const error = ref(null)

  // Resources
  const dashboardResource = createResource({
    url: 'cntemad_lms.api.mentor.get_mentor_dashboard',
    auto: false,
    onSuccess(data) {
      dashboard.value = data
      mentees.value = data.mentees || []
      alerts.value = data.alerts || []
    },
    onError(err) {
      error.value = err.message
    },
  })

  const menteesResource = createResource({
    url: 'cntemad_lms.api.mentor.get_my_mentees',
    auto: false,
    onSuccess(data) {
      mentees.value = data || []
    },
    onError(err) {
      error.value = err.message
    },
  })

  const menteeDetailResource = createResource({
    url: 'cntemad_lms.api.mentor.get_mentee_detail',
    auto: false,
    onSuccess(data) {
      currentMentee.value = data
    },
    onError(err) {
      error.value = err.message
    },
  })

  const messagesResource = createResource({
    url: 'cntemad_lms.api.mentor.get_messages',
    auto: false,
    onSuccess(data) {
      if (Array.isArray(data) && data[0]?.student_id) {
        conversations.value = data
      } else {
        messages.value = data || []
      }
    },
    onError(err) {
      error.value = err.message
    },
  })

  const sendMessageResource = createResource({
    url: 'cntemad_lms.api.mentor.send_message',
    auto: false,
  })

  const alertsResource = createResource({
    url: 'cntemad_lms.api.mentor.get_alerts',
    auto: false,
    onSuccess(data) {
      alerts.value = data || []
    },
    onError(err) {
      error.value = err.message
    },
  })

  const dismissAlertResource = createResource({
    url: 'cntemad_lms.api.mentor.dismiss_alert',
    auto: false,
  })

  const menteeStatsResource = createResource({
    url: 'cntemad_lms.api.mentor.get_mentee_stats',
    auto: false,
  })

  // Computed
  const mentor = computed(() => dashboard.value?.mentor || null)
  const stats = computed(() => dashboard.value?.stats || null)
  const recentActivity = computed(() => dashboard.value?.recent_activity || [])

  const activeMentees = computed(() =>
    mentees.value.filter((m) => m.status === 'active')
  )

  const inactiveMentees = computed(() =>
    mentees.value.filter((m) => m.status === 'inactive')
  )

  const unreadCount = computed(() =>
    conversations.value.reduce((acc, c) => acc + (c.unread_count || 0), 0)
  )

  const activeAlerts = computed(() =>
    alerts.value.filter((a) => a.status === 'active')
  )

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

  const fetchMentees = async (status = null, year = null) => {
    loading.value = true
    error.value = null
    try {
      await menteesResource.fetch({ status, year })
      return mentees.value
    } finally {
      loading.value = false
    }
  }

  const fetchMenteeDetail = async (studentId) => {
    loading.value = true
    error.value = null
    try {
      await menteeDetailResource.fetch({ student_id: studentId })
      return currentMentee.value
    } finally {
      loading.value = false
    }
  }

  const fetchMessages = async (studentId = null) => {
    loading.value = true
    error.value = null
    try {
      await messagesResource.fetch({ student_id: studentId })
      return studentId ? messages.value : conversations.value
    } finally {
      loading.value = false
    }
  }

  const sendMessage = async (studentId, content) => {
    sending.value = true
    error.value = null
    try {
      await sendMessageResource.fetch({
        student_id: studentId,
        content,
      })
      // Ajouter le message à la liste locale
      messages.value.push(sendMessageResource.data)
      return sendMessageResource.data
    } catch (e) {
      error.value = e.message
      throw e
    } finally {
      sending.value = false
    }
  }

  const fetchAlerts = async (status = 'active') => {
    loading.value = true
    error.value = null
    try {
      await alertsResource.fetch({ status })
      return alerts.value
    } finally {
      loading.value = false
    }
  }

  const dismissAlert = async (alertId) => {
    try {
      await dismissAlertResource.fetch({ alert_id: alertId })
      // Mettre à jour localement
      const index = alerts.value.findIndex((a) => a.id === alertId)
      if (index > -1) {
        alerts.value[index].status = 'resolved'
      }
      return true
    } catch (e) {
      error.value = e.message
      throw e
    }
  }

  const fetchMenteeStats = async (studentId) => {
    try {
      await menteeStatsResource.fetch({ student_id: studentId })
      return menteeStatsResource.data
    } catch (e) {
      error.value = e.message
      return null
    }
  }

  // Helpers
  const getStatusColor = (status) => {
    return status === 'active' ? 'text-green-600' : 'text-red-600'
  }

  const getStatusLabel = (status) => {
    return status === 'active' ? 'Actif' : 'Inactif'
  }

  const getProgressColor = (progress) => {
    if (progress >= 80) return 'text-green-600'
    if (progress >= 50) return 'text-blue-600'
    if (progress >= 25) return 'text-yellow-600'
    return 'text-red-600'
  }

  const getAlertSeverityColor = (severity) => {
    switch (severity) {
      case 'danger':
        return 'bg-red-50 text-red-700 border-red-200'
      case 'warning':
        return 'bg-yellow-50 text-yellow-700 border-yellow-200'
      case 'info':
        return 'bg-blue-50 text-blue-700 border-blue-200'
      default:
        return 'bg-gray-50 text-gray-700 border-gray-200'
    }
  }

  return {
    // State
    dashboard,
    mentees,
    currentMentee,
    messages,
    conversations,
    alerts,
    loading,
    sending,
    error,

    // Computed
    mentor,
    stats,
    recentActivity,
    activeMentees,
    inactiveMentees,
    unreadCount,
    activeAlerts,

    // Methods
    fetchDashboard,
    fetchMentees,
    fetchMenteeDetail,
    fetchMessages,
    sendMessage,
    fetchAlerts,
    dismissAlert,
    fetchMenteeStats,

    // Helpers
    getStatusColor,
    getStatusLabel,
    getProgressColor,
    getAlertSeverityColor,

    // Resources
    dashboardResource,
    menteesResource,
    menteeDetailResource,
  }
}
