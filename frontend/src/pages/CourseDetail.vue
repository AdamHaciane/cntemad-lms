<script setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import { Card, Badge, Button } from 'frappe-ui'
import ProgressBar from '@/components/custom/ProgressBar.vue'

const route = useRoute()
const courseId = route.params.id

const course = ref({
  title: 'Algorithmes et structures de données',
  description: 'Ce cours couvre les fondamentaux des algorithmes et des structures de données.',
  year: 'L1',
  instructor: 'Dr. Rakoto',
  ecs: [
    { id: 1, title: 'Introduction aux algorithmes', status: 'validated', duration: 10 },
    { id: 2, title: 'Complexité algorithmique', status: 'validated', duration: 8 },
    { id: 3, title: 'Structures linéaires', status: 'in_progress', duration: 12 },
    { id: 4, title: 'Arbres et graphes', status: 'locked', duration: 15 },
  ],
})
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <header class="bg-cntemad-primary text-white px-4 py-6">
      <div class="max-w-4xl mx-auto">
        <Badge variant="subtle" class="mb-2 bg-white/20 text-white">{{ course.year }}</Badge>
        <h1 class="text-2xl font-bold mb-2">{{ course.title }}</h1>
        <p class="text-blue-100">{{ course.instructor }}</p>
      </div>
    </header>

    <main class="px-4 py-6">
      <div class="max-w-4xl mx-auto space-y-6">
        <!-- Progress -->
        <Card class="p-6">
          <h2 class="font-semibold mb-4">Progression du cours</h2>
          <ProgressBar :percent="50" label="2/4 EC validés" />
        </Card>

        <!-- EC List -->
        <Card class="p-6">
          <h2 class="font-semibold mb-4">Éléments Constitutifs (EC)</h2>
          <div class="space-y-3">
            <div
              v-for="ec in course.ecs"
              :key="ec.id"
              class="flex items-center justify-between p-4 rounded-lg border"
              :class="{
                'bg-green-50 border-green-200': ec.status === 'validated',
                'bg-blue-50 border-blue-200': ec.status === 'in_progress',
                'bg-gray-50 border-gray-200 opacity-60': ec.status === 'locked',
              }"
            >
              <div class="flex items-center gap-3">
                <div
                  class="w-8 h-8 rounded-full flex items-center justify-center text-sm"
                  :class="{
                    'bg-green-500 text-white': ec.status === 'validated',
                    'bg-blue-500 text-white': ec.status === 'in_progress',
                    'bg-gray-300 text-gray-500': ec.status === 'locked',
                  }"
                >
                  <span v-if="ec.status === 'validated'">✓</span>
                  <span v-else-if="ec.status === 'in_progress'">▶</span>
                  <span v-else>🔒</span>
                </div>
                <div>
                  <div class="font-medium">{{ ec.title }}</div>
                  <div class="text-sm text-gray-500">{{ ec.duration }}h</div>
                </div>
              </div>
              <Button
                v-if="ec.status !== 'locked'"
                size="sm"
                :variant="ec.status === 'validated' ? 'subtle' : 'solid'"
              >
                {{ ec.status === 'validated' ? 'Revoir' : 'Continuer' }}
              </Button>
            </div>
          </div>
        </Card>
      </div>
    </main>
  </div>
</template>
