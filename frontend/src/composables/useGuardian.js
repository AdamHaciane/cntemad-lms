/**
 * Composable pour gérer les opérations du parent/tuteur.
 *
 * Usage:
 *   const {
 *     children,
 *     notifications,
 *     fetchDashboard,
 *     fetchChildProgress,
 *     initiatePayment
 *   } = useGuardian()
 */
import { ref, computed } from 'vue'
import { createResource } from 'frappe-ui'

export function useGuardian() {
  const dashboard = ref(null)
  const children = ref([])
  const currentChild = ref(null)
  const childPayments = ref([])
  const unpaidEcs = ref([])
  const notifications = ref([])
  const paymentSummary = ref(null)
  const loading = ref(false)
  const paying = ref(false)
  const error = ref(null)

  // Resources
  const dashboardResource = createResource({
    url: 'cntemad_lms.api.guardian.get_guardian_dashboard',
    auto: false,
    onSuccess(data) {
      dashboard.value = data
      children.value = data.children || []
      notifications.value = data.notifications || []
    },
    onError(err) {
      error.value = err.message
    },
  })

  const childrenResource = createResource({
    url: 'cntemad_lms.api.guardian.get_my_children',
    auto: false,
    onSuccess(data) {
      children.value = data || []
    },
    onError(err) {
      error.value = err.message
    },
  })

  const childProgressResource = createResource({
    url: 'cntemad_lms.api.guardian.get_child_progress',
    auto: false,
    onSuccess(data) {
      currentChild.value = data
    },
    onError(err) {
      error.value = err.message
    },
  })

  const childPaymentsResource = createResource({
    url: 'cntemad_lms.api.guardian.get_child_payments',
    auto: false,
    onSuccess(data) {
      childPayments.value = data || []
    },
    onError(err) {
      error.value = err.message
    },
  })

  const unpaidEcsResource = createResource({
    url: 'cntemad_lms.api.guardian.get_unpaid_ecs',
    auto: false,
    onSuccess(data) {
      unpaidEcs.value = data || []
    },
    onError(err) {
      error.value = err.message
    },
  })

  const paymentResource = createResource({
    url: 'cntemad_lms.api.guardian.initiate_payment_for_child',
    auto: false,
  })

  const notificationsResource = createResource({
    url: 'cntemad_lms.api.guardian.get_notifications',
    auto: false,
    onSuccess(data) {
      notifications.value = data || []
    },
    onError(err) {
      error.value = err.message
    },
  })

  const markReadResource = createResource({
    url: 'cntemad_lms.api.guardian.mark_notification_read',
    auto: false,
  })

  const paymentSummaryResource = createResource({
    url: 'cntemad_lms.api.guardian.get_payment_summary',
    auto: false,
    onSuccess(data) {
      paymentSummary.value = data
    },
    onError(err) {
      error.value = err.message
    },
  })

  // Computed
  const guardian = computed(() => dashboard.value?.guardian || null)
  const stats = computed(() => dashboard.value?.stats || null)
  const recentActivity = computed(() => dashboard.value?.recent_activity || [])

  const unreadNotifications = computed(() =>
    notifications.value.filter((n) => !n.read)
  )

  const unreadCount = computed(() => unreadNotifications.value.length)

  const totalChildren = computed(() => children.value.length)

  const avgProgress = computed(() => {
    if (children.value.length === 0) return 0
    const sum = children.value.reduce((acc, c) => acc + (c.progress || 0), 0)
    return sum / children.value.length
  })

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

  const fetchChildren = async () => {
    loading.value = true
    error.value = null
    try {
      await childrenResource.fetch()
      return children.value
    } finally {
      loading.value = false
    }
  }

  const fetchChildProgress = async (studentId) => {
    loading.value = true
    error.value = null
    try {
      await childProgressResource.fetch({ student_id: studentId })
      return currentChild.value
    } finally {
      loading.value = false
    }
  }

  const fetchChildPayments = async (studentId) => {
    loading.value = true
    error.value = null
    try {
      await childPaymentsResource.fetch({ student_id: studentId })
      return childPayments.value
    } finally {
      loading.value = false
    }
  }

  const fetchUnpaidEcs = async (studentId) => {
    loading.value = true
    error.value = null
    try {
      await unpaidEcsResource.fetch({ student_id: studentId })
      return unpaidEcs.value
    } finally {
      loading.value = false
    }
  }

  const initiatePayment = async (studentId, ecId, provider, phoneNumber) => {
    paying.value = true
    error.value = null
    try {
      await paymentResource.fetch({
        student_id: studentId,
        ec_id: ecId,
        provider,
        phone_number: phoneNumber,
      })
      return paymentResource.data
    } catch (e) {
      error.value = e.message
      throw e
    } finally {
      paying.value = false
    }
  }

  const fetchNotifications = async (unreadOnly = false) => {
    loading.value = true
    error.value = null
    try {
      await notificationsResource.fetch({ unread_only: unreadOnly })
      return notifications.value
    } finally {
      loading.value = false
    }
  }

  const markNotificationRead = async (notificationId) => {
    try {
      await markReadResource.fetch({ notification_id: notificationId })
      // Mettre à jour localement
      const index = notifications.value.findIndex((n) => n.id === notificationId)
      if (index > -1) {
        notifications.value[index].read = true
      }
      return true
    } catch (e) {
      error.value = e.message
      throw e
    }
  }

  const fetchPaymentSummary = async () => {
    try {
      await paymentSummaryResource.fetch()
      return paymentSummary.value
    } catch (e) {
      error.value = e.message
      return null
    }
  }

  // Helpers
  const getProgressColor = (progress) => {
    if (progress >= 80) return 'text-green-600'
    if (progress >= 50) return 'text-blue-600'
    if (progress >= 25) return 'text-yellow-600'
    return 'text-red-600'
  }

  const getProgressBgColor = (progress) => {
    if (progress >= 80) return 'bg-green-500'
    if (progress >= 50) return 'bg-blue-500'
    if (progress >= 25) return 'bg-yellow-500'
    return 'bg-red-500'
  }

  const formatAmount = (amount) => {
    return new Intl.NumberFormat('fr-MG').format(amount) + ' Ar'
  }

  const getProviderLabel = (provider) => {
    const labels = {
      mvola: 'MVola',
      orange_money: 'Orange Money',
      airtel_money: 'Airtel Money',
    }
    return labels[provider] || provider
  }

  const getNotificationIcon = (type) => {
    switch (type) {
      case 'success':
        return 'check-circle'
      case 'warning':
        return 'alert-triangle'
      case 'info':
        return 'info'
      case 'error':
        return 'x-circle'
      default:
        return 'bell'
    }
  }

  const getNotificationColor = (type) => {
    switch (type) {
      case 'success':
        return 'text-green-600 bg-green-50'
      case 'warning':
        return 'text-yellow-600 bg-yellow-50'
      case 'info':
        return 'text-blue-600 bg-blue-50'
      case 'error':
        return 'text-red-600 bg-red-50'
      default:
        return 'text-gray-600 bg-gray-50'
    }
  }

  return {
    // State
    dashboard,
    children,
    currentChild,
    childPayments,
    unpaidEcs,
    notifications,
    paymentSummary,
    loading,
    paying,
    error,

    // Computed
    guardian,
    stats,
    recentActivity,
    unreadNotifications,
    unreadCount,
    totalChildren,
    avgProgress,

    // Methods
    fetchDashboard,
    fetchChildren,
    fetchChildProgress,
    fetchChildPayments,
    fetchUnpaidEcs,
    initiatePayment,
    fetchNotifications,
    markNotificationRead,
    fetchPaymentSummary,

    // Helpers
    getProgressColor,
    getProgressBgColor,
    formatAmount,
    getProviderLabel,
    getNotificationIcon,
    getNotificationColor,

    // Resources
    dashboardResource,
    childrenResource,
  }
}
