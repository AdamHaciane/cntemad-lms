<script setup>
import { Button, Card } from 'frappe-ui'
</script>

<template>
  <div class="min-h-screen">
    <!-- Hero Section -->
    <section class="bg-cntemad-primary text-white py-12 px-4">
      <div class="max-w-4xl mx-auto text-center">
        <h1 class="text-3xl md:text-5xl font-bold mb-4">
          CNTEMAD LMS
        </h1>
        <p class="text-lg md:text-xl text-blue-100 mb-8">
          Centre National de Télé-Enseignement de Madagascar
        </p>
        <div class="flex flex-col sm:flex-row gap-4 justify-center">
          <Button variant="solid" class="bg-white text-cntemad-primary">
            S'inscrire
          </Button>
          <Button variant="outline" class="border-white text-white">
            Se connecter
          </Button>
        </div>
      </div>
    </section>

    <!-- Features -->
    <section class="py-12 px-4">
      <div class="max-w-4xl mx-auto">
        <h2 class="text-2xl font-bold text-center mb-8">
          Pourquoi choisir CNTEMAD ?
        </h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Card class="text-center p-6">
            <div class="text-4xl mb-4">34</div>
            <div class="font-semibold">Centres régionaux</div>
            <div class="text-gray-500 text-sm">Sur tout Madagascar</div>
          </Card>
          <Card class="text-center p-6">
            <div class="text-4xl mb-4">17k+</div>
            <div class="font-semibold">Étudiants</div>
            <div class="text-gray-500 text-sm">Chaque année</div>
          </Card>
          <Card class="text-center p-6">
            <div class="text-4xl mb-4">30+</div>
            <div class="font-semibold">Années</div>
            <div class="text-gray-500 text-sm">D'expérience</div>
          </Card>
        </div>
      </div>
    </section>
  </div>
</template>
