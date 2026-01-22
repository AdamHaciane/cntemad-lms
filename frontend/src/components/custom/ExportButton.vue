<!--
  ExportButton.vue
  Bouton d'export avec choix de format.

  Props:
    - data (Array): Données à exporter
    - filename (String): Nom du fichier
    - formats (Array): Formats disponibles ['csv', 'pdf', 'excel']

  Example:
    <ExportButton :data="students" filename="etudiants" :formats="['csv', 'pdf']" />
-->
<script setup>
import { Button, Dropdown } from 'frappe-ui'
import { ref } from 'vue'

const props = defineProps({
  data: {
    type: Array,
    required: true,
  },
  filename: {
    type: String,
    default: 'export',
  },
  formats: {
    type: Array,
    default: () => ['csv', 'pdf'],
  },
})

const loading = ref(false)

const formatLabels = {
  csv: { label: 'CSV', icon: '📄' },
  pdf: { label: 'PDF', icon: '📕' },
  excel: { label: 'Excel', icon: '📊' },
}

const exportToCSV = () => {
  if (!props.data.length) return

  const headers = Object.keys(props.data[0])
  const csvContent = [
    headers.join(','),
    ...props.data.map((row) =>
      headers.map((h) => `"${row[h] || ''}"`.replace(/"/g, '""')).join(',')
    ),
  ].join('\n')

  downloadFile(csvContent, `${props.filename}.csv`, 'text/csv')
}

const exportToPDF = async () => {
  // Pour PDF, on utilise généralement l'API backend
  // Placeholder - à implémenter avec Frappe print format
  console.log('PDF export - use backend API')
}

const downloadFile = (content, filename, mimeType) => {
  const blob = new Blob([content], { type: mimeType })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = filename
  link.click()
  URL.revokeObjectURL(url)
}

const handleExport = async (format) => {
  loading.value = true
  try {
    switch (format) {
      case 'csv':
        exportToCSV()
        break
      case 'pdf':
        await exportToPDF()
        break
      case 'excel':
        exportToCSV() // Fallback to CSV
        break
    }
  } finally {
    loading.value = false
  }
}

const dropdownOptions = props.formats.map((f) => ({
  label: formatLabels[f]?.label || f.toUpperCase(),
  icon: formatLabels[f]?.icon,
  onClick: () => handleExport(f),
}))
</script>

<template>
  <Dropdown :options="dropdownOptions" placement="bottom-end">
    <template #default="{ open }">
      <Button variant="outline" :loading="loading" @click="open">
        <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
        </svg>
        Exporter
      </Button>
    </template>
  </Dropdown>
</template>
