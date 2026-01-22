<template>
  <div class="media-upload">
    <!-- Drop zone -->
    <div
      class="border-2 border-dashed rounded-lg p-6 text-center transition-colors"
      :class="[
        isDragging ? 'border-blue-500 bg-blue-50' : 'border-gray-300 hover:border-gray-400',
        disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'
      ]"
      @click="openFilePicker"
      @dragover.prevent="onDragOver"
      @dragleave.prevent="onDragLeave"
      @drop.prevent="onDrop"
    >
      <input
        ref="fileInput"
        type="file"
        class="hidden"
        :accept="acceptedTypes"
        :multiple="multiple"
        @change="onFileSelect"
        :disabled="disabled"
      />

      <div v-if="!uploading && files.length === 0">
        <Upload class="w-10 h-10 text-gray-400 mx-auto mb-3" />
        <p class="text-gray-600 font-medium">
          {{ placeholder || 'Déposez vos fichiers ici' }}
        </p>
        <p class="text-sm text-gray-400 mt-1">
          ou cliquez pour sélectionner
        </p>
        <p class="text-xs text-gray-400 mt-2">
          {{ acceptedTypesLabel }}
        </p>
        <p v-if="maxSize" class="text-xs text-gray-400">
          Max {{ formatSize(maxSize) }}
        </p>
      </div>

      <!-- Uploading -->
      <div v-else-if="uploading" class="py-4">
        <Spinner class="w-8 h-8 mx-auto mb-3" />
        <p class="text-gray-600">Envoi en cours...</p>
        <div class="w-full max-w-xs mx-auto mt-3 bg-gray-200 rounded-full h-2">
          <div
            class="bg-blue-500 h-2 rounded-full transition-all"
            :style="{ width: `${uploadProgress}%` }"
          ></div>
        </div>
        <p class="text-xs text-gray-500 mt-1">{{ uploadProgress }}%</p>
      </div>
    </div>

    <!-- File list -->
    <div v-if="files.length > 0 && !uploading" class="mt-4 space-y-2">
      <div
        v-for="(file, index) in files"
        :key="index"
        class="flex items-center gap-3 p-3 bg-gray-50 rounded-lg"
      >
        <component
          :is="getFileIcon(file)"
          class="w-8 h-8 text-gray-500"
        />
        <div class="flex-1 min-w-0">
          <p class="text-sm font-medium text-gray-900 truncate">
            {{ file.name }}
          </p>
          <p class="text-xs text-gray-500">
            {{ formatSize(file.size) }}
          </p>
        </div>
        <Badge v-if="file.uploaded" theme="green">Envoyé</Badge>
        <Badge v-else-if="file.error" theme="red">Erreur</Badge>
        <button
          type="button"
          class="p-1 text-gray-400 hover:text-red-500 transition-colors"
          @click.stop="removeFile(index)"
        >
          <X class="w-5 h-5" />
        </button>
      </div>
    </div>

    <!-- Actions -->
    <div v-if="files.length > 0 && !autoUpload && !allUploaded" class="mt-4 flex gap-2">
      <Button
        variant="solid"
        @click="uploadFiles"
        :loading="uploading"
      >
        <Upload class="w-4 h-4 mr-2" />
        Envoyer {{ files.length }} fichier{{ files.length > 1 ? 's' : '' }}
      </Button>
      <Button variant="outline" @click="clearFiles">
        Annuler
      </Button>
    </div>

    <!-- Uploaded files preview -->
    <div v-if="uploadedUrls.length > 0" class="mt-4">
      <p class="text-sm font-medium text-gray-700 mb-2">Fichiers envoyés:</p>
      <div class="space-y-2">
        <div
          v-for="(url, index) in uploadedUrls"
          :key="index"
          class="flex items-center gap-2 p-2 bg-green-50 rounded border border-green-200"
        >
          <CheckCircle class="w-5 h-5 text-green-500" />
          <a
            :href="url"
            target="_blank"
            class="text-sm text-blue-600 hover:underline truncate flex-1"
          >
            {{ url }}
          </a>
          <button
            type="button"
            class="p-1 text-gray-400 hover:text-red-500"
            @click="removeUploadedUrl(index)"
          >
            <X class="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Button, Badge, Spinner } from 'frappe-ui'
import {
  Upload,
  X,
  FileText,
  Video,
  Image as ImageIcon,
  File,
  CheckCircle
} from 'lucide-vue-next'

const props = defineProps({
  accept: {
    type: String,
    default: 'pdf,video,image' // pdf, video, image, or comma-separated
  },
  multiple: {
    type: Boolean,
    default: true
  },
  maxSize: {
    type: Number,
    default: 50 * 1024 * 1024 // 50MB
  },
  autoUpload: {
    type: Boolean,
    default: false
  },
  placeholder: {
    type: String,
    default: ''
  },
  disabled: {
    type: Boolean,
    default: false
  },
  modelValue: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['update:modelValue', 'upload', 'error'])

const fileInput = ref(null)
const files = ref([])
const isDragging = ref(false)
const uploading = ref(false)
const uploadProgress = ref(0)
const uploadedUrls = ref([...props.modelValue])

const acceptedTypes = computed(() => {
  const types = props.accept.split(',').map(t => t.trim().toLowerCase())
  const mimeTypes = []

  types.forEach(type => {
    if (type === 'pdf') mimeTypes.push('.pdf,application/pdf')
    if (type === 'video') mimeTypes.push('video/*')
    if (type === 'image') mimeTypes.push('image/*')
    if (type === 'doc') mimeTypes.push('.doc,.docx,application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document')
  })

  return mimeTypes.join(',')
})

const acceptedTypesLabel = computed(() => {
  const types = props.accept.split(',').map(t => t.trim().toLowerCase())
  const labels = []

  types.forEach(type => {
    if (type === 'pdf') labels.push('PDF')
    if (type === 'video') labels.push('Vidéo')
    if (type === 'image') labels.push('Image')
    if (type === 'doc') labels.push('Word')
  })

  return `Formats acceptés: ${labels.join(', ')}`
})

const allUploaded = computed(() => {
  return files.value.length > 0 && files.value.every(f => f.uploaded)
})

const openFilePicker = () => {
  if (!props.disabled) {
    fileInput.value?.click()
  }
}

const onDragOver = () => {
  if (!props.disabled) {
    isDragging.value = true
  }
}

const onDragLeave = () => {
  isDragging.value = false
}

const onDrop = (e) => {
  isDragging.value = false
  if (props.disabled) return

  const droppedFiles = Array.from(e.dataTransfer.files)
  addFiles(droppedFiles)
}

const onFileSelect = (e) => {
  const selectedFiles = Array.from(e.target.files)
  addFiles(selectedFiles)
  e.target.value = '' // Reset input
}

const addFiles = (newFiles) => {
  for (const file of newFiles) {
    // Check size
    if (file.size > props.maxSize) {
      emit('error', {
        file,
        message: `Fichier trop volumineux (max ${formatSize(props.maxSize)})`
      })
      continue
    }

    // Add to list
    files.value.push({
      file,
      name: file.name,
      size: file.size,
      type: file.type,
      uploaded: false,
      error: false,
      url: null
    })
  }

  if (props.autoUpload && files.value.length > 0) {
    uploadFiles()
  }
}

const removeFile = (index) => {
  files.value.splice(index, 1)
}

const clearFiles = () => {
  files.value = []
}

const uploadFiles = async () => {
  uploading.value = true
  uploadProgress.value = 0

  const toUpload = files.value.filter(f => !f.uploaded)
  const total = toUpload.length
  let completed = 0

  for (const fileObj of toUpload) {
    try {
      const url = await uploadFile(fileObj.file)
      fileObj.uploaded = true
      fileObj.url = url
      uploadedUrls.value.push(url)
      emit('update:modelValue', uploadedUrls.value)
      emit('upload', { file: fileObj.file, url })
    } catch (e) {
      fileObj.error = true
      emit('error', { file: fileObj.file, message: e.message })
    }

    completed++
    uploadProgress.value = Math.round((completed / total) * 100)
  }

  uploading.value = false
}

const uploadFile = async (file) => {
  const formData = new FormData()
  formData.append('file', file)
  formData.append('is_private', '0')
  formData.append('folder', 'Home')

  const response = await fetch('/api/method/upload_file', {
    method: 'POST',
    body: formData,
    headers: {
      'X-Frappe-CSRF-Token': window.csrf_token || ''
    }
  })

  if (!response.ok) {
    throw new Error('Échec de l\'envoi')
  }

  const data = await response.json()
  return data.message?.file_url || data.file_url
}

const removeUploadedUrl = (index) => {
  uploadedUrls.value.splice(index, 1)
  emit('update:modelValue', uploadedUrls.value)
}

const getFileIcon = (file) => {
  const type = file.type || ''
  if (type.includes('pdf')) return FileText
  if (type.includes('video')) return Video
  if (type.includes('image')) return ImageIcon
  return File
}

const formatSize = (bytes) => {
  if (bytes < 1024) return bytes + ' B'
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
  return (bytes / (1024 * 1024)).toFixed(1) + ' MB'
}

// Expose methods
defineExpose({
  getUrls: () => uploadedUrls.value,
  clear: () => {
    files.value = []
    uploadedUrls.value = []
    emit('update:modelValue', [])
  }
})
</script>
