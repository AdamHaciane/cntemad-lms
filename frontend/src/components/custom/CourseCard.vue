<!--
  CourseCard.vue
  Affiche une carte de cours avec progression.

  Props:
    - course (Object): Données du cours { id, title, year, ecCount, progress }

  Events:
    - @click: Émis au clic sur la carte
-->
<script setup>
import { Card, Badge } from 'frappe-ui'
import { useRouter } from 'vue-router'
import ProgressBar from './ProgressBar.vue'

const props = defineProps({
  course: {
    type: Object,
    required: true,
  },
})

const router = useRouter()

const handleClick = () => {
  router.push(`/courses/${props.course.id}`)
}
</script>

<template>
  <Card
    class="p-4 cursor-pointer hover:shadow-md transition-shadow"
    @click="handleClick"
  >
    <div class="flex justify-between items-start mb-3">
      <h3 class="font-semibold text-gray-900 line-clamp-2">
        {{ course.title }}
      </h3>
      <Badge variant="subtle" class="ml-2 shrink-0">
        {{ course.year }}
      </Badge>
    </div>

    <div class="text-sm text-gray-500 mb-3">
      {{ course.ecCount }} EC
    </div>

    <ProgressBar
      :percent="course.progress"
      :label="course.progress > 0 ? 'En cours' : 'Non commencé'"
      :color="course.progress === 100 ? 'bg-green-500' : 'bg-cntemad-primary'"
    />
  </Card>
</template>
