<script setup>
import { ref, onMounted } from 'vue'
import { Card, Badge, Button } from 'frappe-ui'
import ProgressBar from '@/components/custom/ProgressBar.vue'

const dashboard = ref(null)
const loading = ref(true)

onMounted(async () => {
  // Fetch dashboard data
  // TODO: Use $resources pattern
  loading.value = false
})
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <header class="bg-white border-b px-4 py-4">
      <div class="max-w-4xl mx-auto">
        <h1 class="text-xl font-bold">Mon Dashboard</h1>
      </div>
    </header>

    <main class="px-4 py-6">
      <div class="max-w-4xl mx-auto space-y-6">
        <!-- Progress Card -->
        <Card class="p-6">
          <h2 class="font-semibold mb-4">Ma Progression</h2>
          <ProgressBar :percent="65" label="8/12 EC validés" />
          <div class="mt-4 flex gap-2">
            <Badge variant="success">L2</Badge>
            <Badge variant="subtle">Informatique</Badge>
          </div>
        </Card>

        <!-- Current Courses -->
        <Card class="p-6">
          <div class="flex justify-between items-center mb-4">
            <h2 class="font-semibold">Mes cours en cours</h2>
            <Button variant="subtle" size="sm">Voir tout</Button>
          </div>
          <div class="space-y-3">
            <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div>
                <div class="font-medium">Algorithmes</div>
                <div class="text-sm text-gray-500">3 EC restants</div>
              </div>
              <Badge variant="warning">En cours</Badge>
            </div>
            <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div>
                <div class="font-medium">Base de données</div>
                <div class="text-sm text-gray-500">2 EC restants</div>
              </div>
              <Badge variant="warning">En cours</Badge>
            </div>
          </div>
        </Card>

        <!-- Quick Actions -->
        <div class="grid grid-cols-2 gap-4">
          <Button class="h-20 flex-col gap-2" variant="outline">
            <span class="text-2xl">📚</span>
            <span>Mes cours</span>
          </Button>
          <Button class="h-20 flex-col gap-2" variant="outline">
            <span class="text-2xl">💳</span>
            <span>Paiements</span>
          </Button>
        </div>
      </div>
    </main>

    <!-- Bottom Navigation (Mobile) -->
    <nav class="fixed bottom-0 left-0 right-0 bg-white border-t md:hidden">
      <div class="flex justify-around py-2">
        <button class="flex flex-col items-center p-2 text-cntemad-primary">
          <span>🏠</span>
          <span class="text-xs">Accueil</span>
        </button>
        <button class="flex flex-col items-center p-2 text-gray-500">
          <span>📚</span>
          <span class="text-xs">Cours</span>
        </button>
        <button class="flex flex-col items-center p-2 text-gray-500">
          <span>📊</span>
          <span class="text-xs">Progression</span>
        </button>
        <button class="flex flex-col items-center p-2 text-gray-500">
          <span>👤</span>
          <span class="text-xs">Profil</span>
        </button>
      </div>
    </nav>
  </div>
</template>
