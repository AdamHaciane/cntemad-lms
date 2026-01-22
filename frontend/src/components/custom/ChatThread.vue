<!--
  ChatThread.vue
  Thread de messagerie simple.

  Props:
    - messages (Array): Liste des messages { id, content, sender, timestamp, isMe }
    - loading (Boolean): Chargement en cours

  Events:
    - @send(message): Émis à l'envoi d'un message

  Example:
    <ChatThread :messages="messages" @send="sendMessage" />
-->
<script setup>
import { Button, Avatar, Spinner } from 'frappe-ui'
import { ref, nextTick, watch } from 'vue'

const props = defineProps({
  messages: {
    type: Array,
    default: () => [],
  },
  loading: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['send'])

const newMessage = ref('')
const messagesContainer = ref(null)

const formatTime = (timestamp) => {
  const date = new Date(timestamp)
  return date.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })
}

const formatDate = (timestamp) => {
  const date = new Date(timestamp)
  const today = new Date()
  const yesterday = new Date(today)
  yesterday.setDate(yesterday.getDate() - 1)

  if (date.toDateString() === today.toDateString()) return 'Aujourd\'hui'
  if (date.toDateString() === yesterday.toDateString()) return 'Hier'
  return date.toLocaleDateString('fr-FR')
}

const sendMessage = () => {
  const content = newMessage.value.trim()
  if (!content) return

  emit('send', content)
  newMessage.value = ''
}

const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

watch(() => props.messages.length, scrollToBottom)
</script>

<template>
  <div class="flex flex-col h-full">
    <!-- Messages -->
    <div
      ref="messagesContainer"
      class="flex-1 overflow-y-auto p-4 space-y-4"
    >
      <div v-if="loading" class="flex justify-center py-8">
        <Spinner class="w-6 h-6" />
      </div>

      <template v-else>
        <div
          v-for="message in messages"
          :key="message.id"
          class="flex gap-3"
          :class="message.isMe ? 'flex-row-reverse' : ''"
        >
          <Avatar
            v-if="!message.isMe"
            :label="message.sender"
            size="sm"
            class="shrink-0"
          />

          <div
            class="max-w-[75%] rounded-lg px-4 py-2"
            :class="message.isMe
              ? 'bg-cntemad-primary text-white rounded-br-none'
              : 'bg-gray-100 text-gray-900 rounded-bl-none'"
          >
            <p class="text-sm whitespace-pre-wrap">{{ message.content }}</p>
            <p
              class="text-xs mt-1"
              :class="message.isMe ? 'text-white/70' : 'text-gray-400'"
            >
              {{ formatTime(message.timestamp) }}
            </p>
          </div>
        </div>
      </template>
    </div>

    <!-- Input -->
    <div class="border-t p-4">
      <form class="flex gap-2" @submit.prevent="sendMessage">
        <input
          v-model="newMessage"
          type="text"
          placeholder="Écrire un message..."
          class="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-cntemad-primary focus:border-transparent"
        />
        <Button type="submit" variant="solid" :disabled="!newMessage.trim()">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
          </svg>
        </Button>
      </form>
    </div>
  </div>
</template>
