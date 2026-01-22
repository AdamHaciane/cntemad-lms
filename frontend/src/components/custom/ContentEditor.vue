<template>
  <div class="content-editor">
    <!-- Toolbar -->
    <div class="border rounded-t-lg bg-gray-50 p-2 flex flex-wrap gap-1">
      <!-- Text formatting -->
      <div class="flex gap-1 border-r pr-2 mr-2">
        <button
          type="button"
          class="toolbar-btn"
          :class="{ active: isBold }"
          @click="toggleBold"
          title="Gras"
        >
          <Bold class="w-4 h-4" />
        </button>
        <button
          type="button"
          class="toolbar-btn"
          :class="{ active: isItalic }"
          @click="toggleItalic"
          title="Italique"
        >
          <Italic class="w-4 h-4" />
        </button>
        <button
          type="button"
          class="toolbar-btn"
          :class="{ active: isUnderline }"
          @click="toggleUnderline"
          title="Souligné"
        >
          <Underline class="w-4 h-4" />
        </button>
      </div>

      <!-- Headings -->
      <div class="flex gap-1 border-r pr-2 mr-2">
        <button
          type="button"
          class="toolbar-btn"
          :class="{ active: isH1 }"
          @click="setHeading(1)"
          title="Titre 1"
        >
          <Heading1 class="w-4 h-4" />
        </button>
        <button
          type="button"
          class="toolbar-btn"
          :class="{ active: isH2 }"
          @click="setHeading(2)"
          title="Titre 2"
        >
          <Heading2 class="w-4 h-4" />
        </button>
        <button
          type="button"
          class="toolbar-btn"
          :class="{ active: isH3 }"
          @click="setHeading(3)"
          title="Titre 3"
        >
          <Heading3 class="w-4 h-4" />
        </button>
      </div>

      <!-- Lists -->
      <div class="flex gap-1 border-r pr-2 mr-2">
        <button
          type="button"
          class="toolbar-btn"
          :class="{ active: isBulletList }"
          @click="toggleBulletList"
          title="Liste à puces"
        >
          <List class="w-4 h-4" />
        </button>
        <button
          type="button"
          class="toolbar-btn"
          :class="{ active: isOrderedList }"
          @click="toggleOrderedList"
          title="Liste numérotée"
        >
          <ListOrdered class="w-4 h-4" />
        </button>
      </div>

      <!-- Media -->
      <div class="flex gap-1 border-r pr-2 mr-2">
        <button
          type="button"
          class="toolbar-btn"
          @click="insertLink"
          title="Lien"
        >
          <Link class="w-4 h-4" />
        </button>
        <button
          type="button"
          class="toolbar-btn"
          @click="insertImage"
          title="Image"
        >
          <ImageIcon class="w-4 h-4" />
        </button>
        <button
          type="button"
          class="toolbar-btn"
          @click="insertVideo"
          title="Vidéo YouTube"
        >
          <Youtube class="w-4 h-4" />
        </button>
      </div>

      <!-- Block -->
      <div class="flex gap-1">
        <button
          type="button"
          class="toolbar-btn"
          :class="{ active: isBlockquote }"
          @click="toggleBlockquote"
          title="Citation"
        >
          <Quote class="w-4 h-4" />
        </button>
        <button
          type="button"
          class="toolbar-btn"
          :class="{ active: isCodeBlock }"
          @click="toggleCodeBlock"
          title="Code"
        >
          <Code class="w-4 h-4" />
        </button>
        <button
          type="button"
          class="toolbar-btn"
          @click="insertHR"
          title="Séparateur"
        >
          <Minus class="w-4 h-4" />
        </button>
      </div>

      <!-- Undo/Redo -->
      <div class="flex gap-1 ml-auto">
        <button
          type="button"
          class="toolbar-btn"
          @click="undo"
          title="Annuler"
        >
          <Undo class="w-4 h-4" />
        </button>
        <button
          type="button"
          class="toolbar-btn"
          @click="redo"
          title="Rétablir"
        >
          <Redo class="w-4 h-4" />
        </button>
      </div>
    </div>

    <!-- Editor area -->
    <div
      ref="editorRef"
      class="editor-content border border-t-0 rounded-b-lg p-4 min-h-[300px] focus:outline-none prose prose-sm max-w-none"
      contenteditable="true"
      @input="onInput"
      @keydown="onKeydown"
      @paste="onPaste"
      v-html="internalContent"
    ></div>

    <!-- Link Dialog -->
    <Dialog v-model="showLinkDialog" :options="{ title: 'Insérer un lien' }">
      <template #body-content>
        <div class="space-y-4">
          <Input
            v-model="linkUrl"
            label="URL"
            placeholder="https://..."
          />
          <Input
            v-model="linkText"
            label="Texte (optionnel)"
            placeholder="Texte du lien"
          />
        </div>
      </template>
      <template #actions>
        <Button variant="outline" @click="showLinkDialog = false">Annuler</Button>
        <Button variant="solid" @click="confirmLink">Insérer</Button>
      </template>
    </Dialog>

    <!-- Image Dialog -->
    <Dialog v-model="showImageDialog" :options="{ title: 'Insérer une image' }">
      <template #body-content>
        <div class="space-y-4">
          <Input
            v-model="imageUrl"
            label="URL de l'image"
            placeholder="https://..."
          />
          <Input
            v-model="imageAlt"
            label="Texte alternatif"
            placeholder="Description de l'image"
          />
        </div>
      </template>
      <template #actions>
        <Button variant="outline" @click="showImageDialog = false">Annuler</Button>
        <Button variant="solid" @click="confirmImage">Insérer</Button>
      </template>
    </Dialog>

    <!-- Video Dialog -->
    <Dialog v-model="showVideoDialog" :options="{ title: 'Insérer une vidéo YouTube' }">
      <template #body-content>
        <div class="space-y-4">
          <Input
            v-model="videoUrl"
            label="URL YouTube"
            placeholder="https://youtube.com/watch?v=..."
          />
        </div>
      </template>
      <template #actions>
        <Button variant="outline" @click="showVideoDialog = false">Annuler</Button>
        <Button variant="solid" @click="confirmVideo">Insérer</Button>
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, nextTick } from 'vue'
import { Button, Input, Dialog } from 'frappe-ui'
import {
  Bold,
  Italic,
  Underline,
  Heading1,
  Heading2,
  Heading3,
  List,
  ListOrdered,
  Link,
  Image as ImageIcon,
  Youtube,
  Quote,
  Code,
  Minus,
  Undo,
  Redo
} from 'lucide-vue-next'

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:modelValue'])

const editorRef = ref(null)
const internalContent = ref(props.modelValue)

// Dialogs
const showLinkDialog = ref(false)
const showImageDialog = ref(false)
const showVideoDialog = ref(false)

const linkUrl = ref('')
const linkText = ref('')
const imageUrl = ref('')
const imageAlt = ref('')
const videoUrl = ref('')

// Active states
const isBold = ref(false)
const isItalic = ref(false)
const isUnderline = ref(false)
const isH1 = ref(false)
const isH2 = ref(false)
const isH3 = ref(false)
const isBulletList = ref(false)
const isOrderedList = ref(false)
const isBlockquote = ref(false)
const isCodeBlock = ref(false)

// Watch for external changes
watch(() => props.modelValue, (newVal) => {
  if (newVal !== editorRef.value?.innerHTML) {
    internalContent.value = newVal
  }
})

onMounted(() => {
  updateActiveStates()
  document.addEventListener('selectionchange', updateActiveStates)
})

const onInput = () => {
  emit('update:modelValue', editorRef.value?.innerHTML || '')
  updateActiveStates()
}

const onKeydown = (e) => {
  // Handle Tab for indentation
  if (e.key === 'Tab') {
    e.preventDefault()
    document.execCommand('insertText', false, '    ')
  }
}

const onPaste = (e) => {
  e.preventDefault()
  const text = e.clipboardData.getData('text/plain')
  document.execCommand('insertText', false, text)
}

const updateActiveStates = () => {
  isBold.value = document.queryCommandState('bold')
  isItalic.value = document.queryCommandState('italic')
  isUnderline.value = document.queryCommandState('underline')

  const selection = window.getSelection()
  if (selection.rangeCount > 0) {
    const parent = selection.getRangeAt(0).commonAncestorContainer
    const element = parent.nodeType === 3 ? parent.parentElement : parent

    isH1.value = !!element.closest('h1')
    isH2.value = !!element.closest('h2')
    isH3.value = !!element.closest('h3')
    isBulletList.value = !!element.closest('ul')
    isOrderedList.value = !!element.closest('ol')
    isBlockquote.value = !!element.closest('blockquote')
    isCodeBlock.value = !!element.closest('pre')
  }
}

// Formatting commands
const toggleBold = () => {
  document.execCommand('bold')
  editorRef.value?.focus()
  updateActiveStates()
}

const toggleItalic = () => {
  document.execCommand('italic')
  editorRef.value?.focus()
  updateActiveStates()
}

const toggleUnderline = () => {
  document.execCommand('underline')
  editorRef.value?.focus()
  updateActiveStates()
}

const setHeading = (level) => {
  document.execCommand('formatBlock', false, `h${level}`)
  editorRef.value?.focus()
  updateActiveStates()
}

const toggleBulletList = () => {
  document.execCommand('insertUnorderedList')
  editorRef.value?.focus()
  updateActiveStates()
}

const toggleOrderedList = () => {
  document.execCommand('insertOrderedList')
  editorRef.value?.focus()
  updateActiveStates()
}

const toggleBlockquote = () => {
  document.execCommand('formatBlock', false, 'blockquote')
  editorRef.value?.focus()
  updateActiveStates()
}

const toggleCodeBlock = () => {
  document.execCommand('formatBlock', false, 'pre')
  editorRef.value?.focus()
  updateActiveStates()
}

const insertHR = () => {
  document.execCommand('insertHorizontalRule')
  editorRef.value?.focus()
}

const undo = () => {
  document.execCommand('undo')
  editorRef.value?.focus()
}

const redo = () => {
  document.execCommand('redo')
  editorRef.value?.focus()
}

// Link
const insertLink = () => {
  const selection = window.getSelection()
  linkText.value = selection.toString()
  linkUrl.value = ''
  showLinkDialog.value = true
}

const confirmLink = () => {
  if (!linkUrl.value) return

  const text = linkText.value || linkUrl.value
  const html = `<a href="${linkUrl.value}" target="_blank" rel="noopener">${text}</a>`
  document.execCommand('insertHTML', false, html)

  showLinkDialog.value = false
  editorRef.value?.focus()
}

// Image
const insertImage = () => {
  imageUrl.value = ''
  imageAlt.value = ''
  showImageDialog.value = true
}

const confirmImage = () => {
  if (!imageUrl.value) return

  const html = `<img src="${imageUrl.value}" alt="${imageAlt.value || ''}" class="max-w-full rounded" />`
  document.execCommand('insertHTML', false, html)

  showImageDialog.value = false
  editorRef.value?.focus()
}

// Video
const insertVideo = () => {
  videoUrl.value = ''
  showVideoDialog.value = true
}

const confirmVideo = () => {
  if (!videoUrl.value) return

  // Extract YouTube video ID
  const match = videoUrl.value.match(/(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\s]+)/)
  const videoId = match ? match[1] : null

  if (videoId) {
    const html = `
      <div class="video-embed my-4">
        <iframe
          src="https://www.youtube.com/embed/${videoId}"
          class="w-full aspect-video rounded"
          allowfullscreen
        ></iframe>
      </div>
    `
    document.execCommand('insertHTML', false, html)
  }

  showVideoDialog.value = false
  editorRef.value?.focus()
}

// Expose methods
defineExpose({
  getContent: () => editorRef.value?.innerHTML || '',
  setContent: (html) => {
    internalContent.value = html
    nextTick(() => {
      if (editorRef.value) {
        editorRef.value.innerHTML = html
      }
    })
  },
  focus: () => editorRef.value?.focus()
})
</script>

<style scoped>
.toolbar-btn {
  @apply p-2 rounded hover:bg-gray-200 text-gray-600 transition-colors;
}

.toolbar-btn.active {
  @apply bg-blue-100 text-blue-600;
}

.editor-content {
  @apply bg-white;
}

.editor-content:focus {
  @apply ring-2 ring-blue-500 ring-offset-1;
}

/* Prose styles for content */
.editor-content :deep(h1) {
  @apply text-2xl font-bold mt-4 mb-2;
}

.editor-content :deep(h2) {
  @apply text-xl font-bold mt-3 mb-2;
}

.editor-content :deep(h3) {
  @apply text-lg font-semibold mt-2 mb-1;
}

.editor-content :deep(ul) {
  @apply list-disc pl-6 my-2;
}

.editor-content :deep(ol) {
  @apply list-decimal pl-6 my-2;
}

.editor-content :deep(blockquote) {
  @apply border-l-4 border-gray-300 pl-4 italic my-2 text-gray-600;
}

.editor-content :deep(pre) {
  @apply bg-gray-100 p-3 rounded font-mono text-sm overflow-x-auto my-2;
}

.editor-content :deep(a) {
  @apply text-blue-600 underline;
}

.editor-content :deep(img) {
  @apply max-w-full rounded my-2;
}

.editor-content :deep(hr) {
  @apply my-4 border-gray-300;
}
</style>
