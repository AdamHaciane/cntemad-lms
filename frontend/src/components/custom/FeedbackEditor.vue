<!--
  FeedbackEditor.vue
  Éditeur de feedback pour les évaluateurs avec templates et formatage.

  Props:
    - modelValue (String): Contenu du feedback
    - placeholder (String): Placeholder du textarea
    - showTemplates (Boolean): Afficher les templates de feedback
    - showPreview (Boolean): Afficher le preview en temps réel
    - maxLength (Number): Longueur max du feedback

  Events:
    - @update:modelValue: Émis au changement

  Example:
    <FeedbackEditor v-model="feedback" show-templates />
-->
<script setup>
import { ref, computed, watch } from 'vue'
import { Button, Badge } from 'frappe-ui'
import { Bold, Italic, List, ListOrdered, MessageSquare, Copy, Eye, EyeOff } from 'lucide-vue-next'

const props = defineProps({
  modelValue: {
    type: String,
    default: '',
  },
  placeholder: {
    type: String,
    default: 'Saisissez votre feedback...',
  },
  showTemplates: {
    type: Boolean,
    default: true,
  },
  showPreview: {
    type: Boolean,
    default: false,
  },
  maxLength: {
    type: Number,
    default: 5000,
  },
})

const emit = defineEmits(['update:modelValue'])

const internalContent = ref(props.modelValue)
const previewVisible = ref(props.showPreview)
const textareaRef = ref(null)

watch(() => props.modelValue, (newVal) => {
  internalContent.value = newVal
})

watch(internalContent, (newVal) => {
  emit('update:modelValue', newVal)
})

const characterCount = computed(() => internalContent.value.length)
const isOverLimit = computed(() => characterCount.value > props.maxLength)

// Templates de feedback prédéfinis
const feedbackTemplates = [
  {
    id: 'excellent',
    label: 'Excellent travail',
    icon: '🌟',
    theme: 'green',
    content: `Excellent travail ! Votre copie démontre une très bonne maîtrise du sujet.

Points forts :
-
-

Continuez ainsi !`,
  },
  {
    id: 'good',
    label: 'Bon travail',
    icon: '👍',
    theme: 'blue',
    content: `Bon travail dans l'ensemble. Votre copie montre une bonne compréhension.

Points forts :
-

Points à améliorer :
-

Conseil : `,
  },
  {
    id: 'average',
    label: 'Travail moyen',
    icon: '📝',
    theme: 'yellow',
    content: `Travail acceptable mais des améliorations sont nécessaires.

Ce qui est acquis :
-

Ce qui reste à travailler :
-
-

Recommandations pour progresser :
`,
  },
  {
    id: 'insufficient',
    label: 'Insuffisant',
    icon: '⚠️',
    theme: 'orange',
    content: `Le travail fourni est insuffisant pour valider cet EC.

Lacunes identifiées :
-
-

Actions correctives :
1.
2.

Je vous encourage à revoir le cours et à reprendre cet exercice.`,
  },
  {
    id: 'plagiarism',
    label: 'Plagiat détecté',
    icon: '🚫',
    theme: 'red',
    content: `Attention : Des similitudes importantes ont été détectées avec d'autres sources.

Sections concernées :
-

Rappel : Le plagiat est strictement interdit et peut entraîner des sanctions académiques.

Merci de soumettre un travail original.`,
  },
]

// Snippets rapides
const quickSnippets = [
  { label: 'Bien argumenté', text: 'Argumentation bien structurée et convaincante. ' },
  { label: 'Exemples pertinents', text: 'Bons exemples qui illustrent bien les concepts. ' },
  { label: 'À approfondir', text: 'Ce point mériterait d\'être approfondi davantage. ' },
  { label: 'Revoir la méthode', text: 'La méthodologie utilisée doit être revue. ' },
  { label: 'Manque de clarté', text: 'L\'explication manque de clarté à cet endroit. ' },
  { label: 'Bonne initiative', text: 'Bonne initiative d\'avoir abordé ce sujet. ' },
]

const applyTemplate = (template) => {
  internalContent.value = template.content
  focusTextarea()
}

const insertSnippet = (snippet) => {
  if (textareaRef.value) {
    const start = textareaRef.value.selectionStart
    const end = textareaRef.value.selectionEnd
    const before = internalContent.value.substring(0, start)
    const after = internalContent.value.substring(end)
    internalContent.value = before + snippet.text + after

    // Repositionner le curseur après l'insertion
    setTimeout(() => {
      const newPos = start + snippet.text.length
      textareaRef.value.setSelectionRange(newPos, newPos)
      textareaRef.value.focus()
    }, 0)
  } else {
    internalContent.value += snippet.text
  }
}

const insertFormatting = (type) => {
  if (!textareaRef.value) return

  const start = textareaRef.value.selectionStart
  const end = textareaRef.value.selectionEnd
  const selectedText = internalContent.value.substring(start, end)
  const before = internalContent.value.substring(0, start)
  const after = internalContent.value.substring(end)

  let newText = ''
  let cursorOffset = 0

  switch (type) {
    case 'bold':
      newText = `**${selectedText || 'texte'}**`
      cursorOffset = selectedText ? newText.length : 2
      break
    case 'italic':
      newText = `*${selectedText || 'texte'}*`
      cursorOffset = selectedText ? newText.length : 1
      break
    case 'list':
      newText = selectedText
        ? selectedText.split('\n').map(line => `- ${line}`).join('\n')
        : '- '
      cursorOffset = newText.length
      break
    case 'numbered':
      newText = selectedText
        ? selectedText.split('\n').map((line, i) => `${i + 1}. ${line}`).join('\n')
        : '1. '
      cursorOffset = newText.length
      break
    default:
      return
  }

  internalContent.value = before + newText + after

  setTimeout(() => {
    textareaRef.value.setSelectionRange(start + cursorOffset, start + cursorOffset)
    textareaRef.value.focus()
  }, 0)
}

const copyToClipboard = async () => {
  try {
    await navigator.clipboard.writeText(internalContent.value)
  } catch (err) {
    console.error('Erreur copie:', err)
  }
}

const focusTextarea = () => {
  setTimeout(() => {
    textareaRef.value?.focus()
  }, 0)
}

const togglePreview = () => {
  previewVisible.value = !previewVisible.value
}

// Convertir le markdown basique en HTML pour le preview
const formattedPreview = computed(() => {
  let html = internalContent.value
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    .replace(/^- (.+)$/gm, '<li>$1</li>')
    .replace(/^(\d+)\. (.+)$/gm, '<li>$2</li>')
    .replace(/\n/g, '<br>')

  // Wrapper les listes
  html = html.replace(/(<li>.*<\/li>)+/g, '<ul class="list-disc pl-4 my-2">$&</ul>')

  return html
})
</script>

<template>
  <div class="space-y-3">
    <!-- Templates de feedback -->
    <div v-if="showTemplates" class="space-y-2">
      <div class="text-sm font-medium text-gray-700">Templates</div>
      <div class="flex flex-wrap gap-2">
        <button
          v-for="template in feedbackTemplates"
          :key="template.id"
          type="button"
          class="inline-flex items-center gap-1 px-2 py-1 text-xs rounded-full border transition-colors hover:bg-gray-50"
          :class="{
            'border-green-300 text-green-700': template.theme === 'green',
            'border-blue-300 text-blue-700': template.theme === 'blue',
            'border-yellow-300 text-yellow-700': template.theme === 'yellow',
            'border-orange-300 text-orange-700': template.theme === 'orange',
            'border-red-300 text-red-700': template.theme === 'red',
          }"
          @click="applyTemplate(template)"
        >
          <span>{{ template.icon }}</span>
          <span>{{ template.label }}</span>
        </button>
      </div>
    </div>

    <!-- Toolbar formatage -->
    <div class="flex items-center gap-1 p-1 bg-gray-50 rounded-lg border">
      <button
        type="button"
        class="p-1.5 rounded hover:bg-gray-200 transition-colors"
        title="Gras"
        @click="insertFormatting('bold')"
      >
        <Bold class="w-4 h-4" />
      </button>
      <button
        type="button"
        class="p-1.5 rounded hover:bg-gray-200 transition-colors"
        title="Italique"
        @click="insertFormatting('italic')"
      >
        <Italic class="w-4 h-4" />
      </button>
      <button
        type="button"
        class="p-1.5 rounded hover:bg-gray-200 transition-colors"
        title="Liste à puces"
        @click="insertFormatting('list')"
      >
        <List class="w-4 h-4" />
      </button>
      <button
        type="button"
        class="p-1.5 rounded hover:bg-gray-200 transition-colors"
        title="Liste numérotée"
        @click="insertFormatting('numbered')"
      >
        <ListOrdered class="w-4 h-4" />
      </button>

      <div class="w-px h-5 bg-gray-300 mx-1"></div>

      <button
        type="button"
        class="p-1.5 rounded hover:bg-gray-200 transition-colors"
        title="Copier"
        @click="copyToClipboard"
      >
        <Copy class="w-4 h-4" />
      </button>
      <button
        type="button"
        class="p-1.5 rounded hover:bg-gray-200 transition-colors"
        :class="{ 'bg-blue-100': previewVisible }"
        title="Aperçu"
        @click="togglePreview"
      >
        <Eye v-if="!previewVisible" class="w-4 h-4" />
        <EyeOff v-else class="w-4 h-4" />
      </button>
    </div>

    <!-- Zone de saisie -->
    <div class="grid gap-3" :class="previewVisible ? 'md:grid-cols-2' : ''">
      <div class="relative">
        <textarea
          ref="textareaRef"
          v-model="internalContent"
          :placeholder="placeholder"
          rows="8"
          class="w-full px-3 py-2 border rounded-lg resize-y focus:ring-2 focus:ring-blue-500 focus:border-transparent font-mono text-sm"
          :class="{ 'border-red-500': isOverLimit }"
        ></textarea>
        <div class="absolute bottom-2 right-2 text-xs" :class="isOverLimit ? 'text-red-500' : 'text-gray-400'">
          {{ characterCount }} / {{ maxLength }}
        </div>
      </div>

      <!-- Preview -->
      <div
        v-if="previewVisible"
        class="p-3 border rounded-lg bg-gray-50 overflow-auto text-sm prose prose-sm max-w-none"
        style="max-height: 250px"
        v-html="formattedPreview || '<span class=\'text-gray-400\'>Aperçu du feedback...</span>'"
      ></div>
    </div>

    <!-- Snippets rapides -->
    <div class="space-y-2">
      <div class="text-sm font-medium text-gray-700 flex items-center gap-1">
        <MessageSquare class="w-4 h-4" />
        Insertions rapides
      </div>
      <div class="flex flex-wrap gap-1">
        <button
          v-for="snippet in quickSnippets"
          :key="snippet.label"
          type="button"
          class="px-2 py-1 text-xs bg-white border border-gray-200 rounded hover:bg-gray-50 hover:border-gray-300 transition-colors"
          @click="insertSnippet(snippet)"
        >
          {{ snippet.label }}
        </button>
      </div>
    </div>

    <!-- Avertissement si trop long -->
    <div v-if="isOverLimit" class="flex items-center gap-2 p-2 bg-red-50 text-red-700 rounded text-sm">
      <span>⚠️</span>
      <span>Le feedback dépasse la limite de {{ maxLength }} caractères.</span>
    </div>
  </div>
</template>
