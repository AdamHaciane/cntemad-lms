<script setup>
import { ref } from 'vue'
import { Card, Input, Badge } from 'frappe-ui'
import CourseCard from '@/components/custom/CourseCard.vue'

const searchQuery = ref('')
const courses = ref([
  { id: 1, title: 'Algorithmes et structures de données', year: 'L1', ecCount: 4, progress: 75 },
  { id: 2, title: 'Base de données', year: 'L2', ecCount: 3, progress: 33 },
  { id: 3, title: 'Programmation Web', year: 'L2', ecCount: 5, progress: 0 },
  { id: 4, title: 'Réseaux informatiques', year: 'L3', ecCount: 4, progress: 50 },
])
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <header class="bg-white border-b px-4 py-4 sticky top-0 z-10">
      <div class="max-w-4xl mx-auto">
        <h1 class="text-xl font-bold mb-4">Cours disponibles</h1>
        <Input
          v-model="searchQuery"
          placeholder="Rechercher un cours..."
          class="w-full"
        />
      </div>
    </header>

    <main class="px-4 py-6">
      <div class="max-w-4xl mx-auto">
        <!-- Filters -->
        <div class="flex gap-2 mb-6 overflow-x-auto pb-2">
          <Badge variant="solid" class="cursor-pointer whitespace-nowrap">Tous</Badge>
          <Badge variant="subtle" class="cursor-pointer whitespace-nowrap">L1</Badge>
          <Badge variant="subtle" class="cursor-pointer whitespace-nowrap">L2</Badge>
          <Badge variant="subtle" class="cursor-pointer whitespace-nowrap">L3</Badge>
          <Badge variant="subtle" class="cursor-pointer whitespace-nowrap">M1</Badge>
          <Badge variant="subtle" class="cursor-pointer whitespace-nowrap">M2</Badge>
        </div>

        <!-- Course Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <CourseCard
            v-for="course in courses"
            :key="course.id"
            :course="course"
          />
        </div>
      </div>
    </main>
  </div>
</template>
