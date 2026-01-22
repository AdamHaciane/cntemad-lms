<!--
  Messages.vue
  Messagerie Mentor-Étudiant avec conversations et chat.
-->
<script setup>
import { ref, computed, onMounted, nextTick, watch } from 'vue'
import { Card, Button, Badge, Spinner } from 'frappe-ui'
import {
  ArrowLeft, Send, User, Search, MessageSquare,
  ChevronLeft, MoreVertical
} from 'lucide-vue-next'
import { useMentor } from '@/composables/useMentor'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const {
  messages,
  conversations,
  loading,
  sending,
  error,
  fetchMessages,
  sendMessage,
} = useMentor()

const newMessage = ref('')
const messagesContainer = ref(null)
const searchQuery = ref('')

const studentId = computed(() => route.params.id || null)
const selectedStudent = ref(null)

onMounted(async () => {
  if (studentId.value) {
    // Charger conversation spécifique
    await loadConversation(studentId.value)
  } else {
    // Charger liste des conversations
    await fetchMessages()
  }
})

watch(studentId, async (newId) => {
  if (newId) {
    await loadConversation(newId)
  }
})

const loadConversation = async (id) => {
  selectedStudent.value = { id, name: 'Chargement...' }
  await fetchMessages(id)
  // Trouver le nom dans les conversations
  const conv = conversations.value.find(c => c.student_id === id)
  if (conv) {
    selectedStudent.value = { id, name: conv.student_name }
  }
  scrollToBottom()
}

const filteredConversations = computed(() => {
  if (!searchQuery.value) return conversations.value
  const query = searchQuery.value.toLowerCase()
  return conversations.value.filter(c =>
    c.student_name?.toLowerCase().includes(query)
  )
})

const handleSend = async () => {
  if (!newMessage.value.trim() || !selectedStudent.value) return

  try {
    await sendMessage(selectedStudent.value.id, newMessage.value)
    newMessage.value = ''
    scrollToBottom()
  } catch (e) {
    console.error('Erreur envoi:', e)
  }
}

const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

const selectConversation = (conv) => {
  router.push(`/mentor/messages/${conv.student_id}`)
}

const goBack = () => {
  if (selectedStudent.value && !studentId.value) {
    selectedStudent.value = null
  } else {
    router.push('/mentor/mentees')
  }
}

const formatTime = (timestamp) => {
  if (!timestamp) return ''
  const date = new Date(timestamp)
  return date.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })
}

const formatDate = (timestamp) => {
  if (!timestamp) return ''
  const date = new Date(timestamp)
  const today = new Date()
  const yesterday = new Date(today)
  yesterday.setDate(yesterday.getDate() - 1)

  if (date.toDateString() === today.toDateString()) {
    return "Aujourd'hui"
  } else if (date.toDateString() === yesterday.toDateString()) {
    return 'Hier'
  }
  return date.toLocaleDateString('fr-FR', { day: '2-digit', month: 'short' })
}
</script>

<template>
  <div class="h-screen flex flex-col bg-gray-50">
    <!-- Header -->
    <div class="bg-white border-b flex-shrink-0">
      <div class="max-w-7xl mx-auto px-4 py-3">
        <div class="flex items-center gap-4">
          <Button variant="ghost" @click="goBack">
            <ArrowLeft class="w-5 h-5" />
          </Button>
          <div class="flex-1">
            <h1 class="text-lg font-bold text-gray-900">
              {{ selectedStudent ? selectedStudent.name : 'Messages' }}
            </h1>
            <p v-if="!selectedStudent" class="text-sm text-gray-500">
              {{ conversations.length }} conversations
            </p>
          </div>
        </div>
      </div>
    </div>

    <div class="flex-1 flex overflow-hidden max-w-7xl mx-auto w-full">
      <!-- Liste des conversations (desktop: sidebar, mobile: plein écran si pas de sélection) -->
      <div
        class="w-full md:w-80 border-r bg-white flex-shrink-0 flex flex-col"
        :class="{ 'hidden md:flex': selectedStudent }"
      >
        <!-- Recherche -->
        <div class="p-3 border-b">
          <div class="relative">
            <Search class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Rechercher..."
              class="w-full pl-10 pr-4 py-2 border rounded-lg text-sm focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>

        <!-- Liste -->
        <div class="flex-1 overflow-y-auto">
          <div v-if="loading && !selectedStudent" class="flex justify-center py-8">
            <Spinner class="w-6 h-6" />
          </div>

          <div v-else-if="filteredConversations.length === 0" class="text-center py-8 text-gray-500">
            <MessageSquare class="w-8 h-8 mx-auto mb-2 opacity-50" />
            <p>Aucune conversation</p>
          </div>

          <div v-else>
            <div
              v-for="conv in filteredConversations"
              :key="conv.student_id"
              class="p-3 border-b cursor-pointer hover:bg-gray-50 transition-colors"
              :class="{ 'bg-blue-50': selectedStudent?.id === conv.student_id }"
              @click="selectConversation(conv)"
            >
              <div class="flex items-start gap-3">
                <div class="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center flex-shrink-0">
                  <span class="text-blue-600 font-semibold">
                    {{ conv.student_name?.charAt(0) }}
                  </span>
                </div>
                <div class="flex-1 min-w-0">
                  <div class="flex items-center justify-between">
                    <span class="font-medium text-gray-900 truncate">{{ conv.student_name }}</span>
                    <span class="text-xs text-gray-500">{{ formatDate(conv.timestamp) }}</span>
                  </div>
                  <p class="text-sm text-gray-600 truncate">{{ conv.last_message }}</p>
                </div>
                <Badge v-if="conv.unread_count > 0" theme="blue" size="sm">
                  {{ conv.unread_count }}
                </Badge>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Zone de chat -->
      <div
        class="flex-1 flex flex-col bg-white"
        :class="{ 'hidden md:flex': !selectedStudent }"
      >
        <!-- Aucune conversation sélectionnée -->
        <div v-if="!selectedStudent" class="flex-1 flex items-center justify-center text-gray-500">
          <div class="text-center">
            <MessageSquare class="w-12 h-12 mx-auto mb-3 opacity-50" />
            <p>Sélectionnez une conversation</p>
          </div>
        </div>

        <!-- Chat -->
        <template v-else>
          <!-- Header chat mobile -->
          <div class="md:hidden p-3 border-b flex items-center gap-3">
            <Button variant="ghost" size="sm" @click="selectedStudent = null">
              <ChevronLeft class="w-5 h-5" />
            </Button>
            <div class="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
              <span class="text-blue-600 font-semibold text-sm">
                {{ selectedStudent.name?.charAt(0) }}
              </span>
            </div>
            <span class="font-medium">{{ selectedStudent.name }}</span>
          </div>

          <!-- Messages -->
          <div
            ref="messagesContainer"
            class="flex-1 overflow-y-auto p-4 space-y-4"
          >
            <div v-if="loading" class="flex justify-center py-4">
              <Spinner class="w-6 h-6" />
            </div>

            <template v-else>
              <div
                v-for="msg in messages"
                :key="msg.id"
                class="flex"
                :class="msg.sender === 'mentor' ? 'justify-end' : 'justify-start'"
              >
                <div
                  class="max-w-[75%] px-4 py-2 rounded-2xl"
                  :class="msg.sender === 'mentor'
                    ? 'bg-blue-500 text-white rounded-br-md'
                    : 'bg-gray-100 text-gray-900 rounded-bl-md'"
                >
                  <p class="text-sm whitespace-pre-wrap">{{ msg.content }}</p>
                  <span
                    class="text-xs mt-1 block"
                    :class="msg.sender === 'mentor' ? 'text-blue-100' : 'text-gray-500'"
                  >
                    {{ formatTime(msg.timestamp) }}
                  </span>
                </div>
              </div>
            </template>
          </div>

          <!-- Input -->
          <div class="p-3 border-t bg-white">
            <form @submit.prevent="handleSend" class="flex gap-2">
              <input
                v-model="newMessage"
                type="text"
                placeholder="Écrire un message..."
                class="flex-1 px-4 py-2 border rounded-full focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                :disabled="sending"
              />
              <Button
                type="submit"
                variant="solid"
                :loading="sending"
                :disabled="!newMessage.trim()"
                class="rounded-full"
              >
                <Send class="w-4 h-4" />
              </Button>
            </form>
          </div>
        </template>
      </div>
    </div>
  </div>
</template>
