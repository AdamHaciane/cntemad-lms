/**
 * Composable pour exporter des données en différents formats.
 *
 * Usage:
 *   const { exportCSV, exportPDF, loading } = useExport()
 *   await exportCSV(data, 'students')
 */
import { ref } from 'vue'

export function useExport() {
  const loading = ref(false)
  const error = ref(null)

  /**
   * Exporter en CSV
   * @param {Array} data - Données à exporter
   * @param {String} filename - Nom du fichier (sans extension)
   * @param {Array} columns - Colonnes à inclure [{ key, label }]
   */
  const exportCSV = async (data, filename = 'export', columns = null) => {
    loading.value = true
    error.value = null

    try {
      if (!data || !data.length) {
        throw new Error('Aucune donnée à exporter')
      }

      // Déterminer les colonnes
      const cols = columns || Object.keys(data[0]).map((key) => ({
        key,
        label: key.charAt(0).toUpperCase() + key.slice(1).replace(/_/g, ' '),
      }))

      // Construire le CSV
      const headers = cols.map((c) => `"${c.label}"`).join(',')
      const rows = data.map((row) =>
        cols.map((c) => {
          const value = row[c.key]
          if (value === null || value === undefined) return '""'
          return `"${String(value).replace(/"/g, '""')}"`
        }).join(',')
      )

      const csvContent = [headers, ...rows].join('\n')

      // Télécharger
      downloadFile(csvContent, `${filename}.csv`, 'text/csv;charset=utf-8;')
    } catch (e) {
      error.value = e.message
      throw e
    } finally {
      loading.value = false
    }
  }

  /**
   * Exporter en PDF via API backend
   * @param {String} reportType - Type de rapport
   * @param {Object} params - Paramètres du rapport
   * @param {String} filename - Nom du fichier
   */
  const exportPDF = async (reportType, params = {}, filename = 'report') => {
    loading.value = true
    error.value = null

    try {
      // TODO: Implémenter avec l'API Frappe
      // const res = await frappe.call({
      //   method: 'cntemad_lms.api.reports.generate_pdf',
      //   args: { report_type: reportType, params }
      // })
      // downloadFile(res.message.data, `${filename}.pdf`, 'application/pdf')

      console.log('PDF export - implement with Frappe API')
    } catch (e) {
      error.value = e.message
      throw e
    } finally {
      loading.value = false
    }
  }

  /**
   * Exporter en JSON
   * @param {Array|Object} data - Données à exporter
   * @param {String} filename - Nom du fichier
   */
  const exportJSON = async (data, filename = 'export') => {
    loading.value = true

    try {
      const jsonContent = JSON.stringify(data, null, 2)
      downloadFile(jsonContent, `${filename}.json`, 'application/json')
    } finally {
      loading.value = false
    }
  }

  /**
   * Télécharger un fichier
   */
  const downloadFile = (content, filename, mimeType) => {
    const blob = new Blob([content], { type: mimeType })
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = filename
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    URL.revokeObjectURL(url)
  }

  /**
   * Formater une date pour l'export
   */
  const formatDate = (date) => {
    if (!date) return ''
    return new Date(date).toLocaleDateString('fr-FR')
  }

  /**
   * Formater un montant pour l'export
   */
  const formatAmount = (amount) => {
    if (amount === null || amount === undefined) return ''
    return new Intl.NumberFormat('fr-MG').format(amount) + ' Ar'
  }

  return {
    loading,
    error,
    exportCSV,
    exportPDF,
    exportJSON,
    formatDate,
    formatAmount,
  }
}
