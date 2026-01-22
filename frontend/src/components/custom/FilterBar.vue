<!--
  FilterBar.vue
  Barre de filtres réutilisable avec état URL.

  Props:
    - filters (Array): Configuration des filtres
      [{ key, label, type: 'select'|'search'|'date', options }]

  Events:
    - @change(filters): Émis au changement

  Example:
    <FilterBar
      :filters="[
        { key: 'year', label: 'Année', type: 'select', options: ['L1', 'L2', 'L3'] },
        { key: 'search', label: 'Recherche', type: 'search' }
      ]"
      @change="handleFilter"
    />
-->
<script setup>
import { Input, Button } from 'frappe-ui'
import { ref, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const props = defineProps({
  filters: {
    type: Array,
    required: true,
  },
})

const emit = defineEmits(['change'])

const route = useRoute()
const router = useRouter()

const filterValues = ref({})

// Initialiser depuis URL
onMounted(() => {
  props.filters.forEach((filter) => {
    filterValues.value[filter.key] = route.query[filter.key] || ''
  })
})

// Mettre à jour URL et émettre
const updateFilter = (key, value) => {
  filterValues.value[key] = value

  // Mettre à jour URL
  const query = { ...route.query }
  if (value) {
    query[key] = value
  } else {
    delete query[key]
  }
  router.replace({ query })

  emit('change', { ...filterValues.value })
}

const resetFilters = () => {
  props.filters.forEach((filter) => {
    filterValues.value[filter.key] = ''
  })
  router.replace({ query: {} })
  emit('change', {})
}

const hasActiveFilters = () => {
  return Object.values(filterValues.value).some((v) => v)
}
</script>

<template>
  <div class="flex flex-wrap gap-3 items-center p-4 bg-gray-50 rounded-lg">
    <template v-for="filter in filters" :key="filter.key">
      <!-- Select -->
      <div v-if="filter.type === 'select'" class="min-w-[150px]">
        <select
          :value="filterValues[filter.key]"
          class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-cntemad-primary focus:border-transparent"
          @change="updateFilter(filter.key, $event.target.value)"
        >
          <option value="">{{ filter.label }}</option>
          <option
            v-for="opt in filter.options"
            :key="opt.value || opt"
            :value="opt.value || opt"
          >
            {{ opt.label || opt }}
          </option>
        </select>
      </div>

      <!-- Search -->
      <div v-else-if="filter.type === 'search'" class="flex-1 min-w-[200px]">
        <Input
          :modelValue="filterValues[filter.key]"
          :placeholder="filter.label || 'Rechercher...'"
          type="search"
          @update:modelValue="updateFilter(filter.key, $event)"
        />
      </div>

      <!-- Date -->
      <div v-else-if="filter.type === 'date'" class="min-w-[150px]">
        <input
          type="date"
          :value="filterValues[filter.key]"
          class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-cntemad-primary focus:border-transparent"
          @change="updateFilter(filter.key, $event.target.value)"
        />
      </div>
    </template>

    <!-- Reset button -->
    <Button
      v-if="hasActiveFilters()"
      variant="subtle"
      size="sm"
      @click="resetFilters"
    >
      Réinitialiser
    </Button>
  </div>
</template>
