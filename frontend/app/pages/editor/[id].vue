<script setup>
const route = useRoute()
const carouselId = route.params.id

const { data: slides, refresh } = await useFetch(`http://127.0.0.1:8000/carousels/${carouselId}/slides`)

async function saveSlide(slide) {
  await $fetch(`http://127.0.0.1:8000/carousels/${carouselId}/slides/${slide.id}`, {
    method: "PATCH",
    body: {
      title: slide.title,
      body: slide.body
    }
  })
  
  await refresh()
}
</script>

<template>
  <div style="padding:40px;font-family:Arial">
    <h1>Carousel Editor</h1>
    
    <a href="/" style="display:inline-block;margin-bottom:20px;color:blue;text-decoration:underline">
      ← Back to carousels
    </a>

    <div v-if="!slides">
      Loading slides...
    </div>

    <div v-else>
      <div
        v-for="slide in slides"
        :key="slide.id"
        style="border:1px solid #ccc;padding:15px;margin-bottom:15px"
      >
        <h3>Slide {{ slide.order }}</h3>
        
        <label style="display:block;margin-bottom:5px;font-weight:bold">Title:</label>
        <input
          v-model="slide.title"
          placeholder="Slide title"
          style="display:block;width:100%;max-width:500px;padding:8px;margin-bottom:10px"
        />
        
        <label style="display:block;margin-bottom:5px;font-weight:bold">Body:</label>
        <textarea
          v-model="slide.body"
          placeholder="Slide body"
          style="display:block;width:100%;max-width:500px;padding:8px;height:120px;margin-bottom:10px"
        ></textarea>
        
        <button
          @click="saveSlide(slide)"
          style="padding:10px 20px;background:#4CAF50;color:white;border:none;cursor:pointer"
        >
          Save
        </button>
      </div>
    </div>
  </div>
</template>
