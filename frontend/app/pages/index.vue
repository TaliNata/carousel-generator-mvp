<script setup>

const title = ref("")
const text = ref("")
const slides = ref(5)

const { data: carousels, refresh } = await useFetch("http://127.0.0.1:8000/carousels")

async function createCarousel() {

  await $fetch("http://127.0.0.1:8000/carousels", {
    method: "POST",
    body: {
      title: title.value,
      source_type: "text",
      source_payload: text.value,
      language: "en",
      slides_count: slides.value
    }
  })

  title.value = ""
  text.value = ""

  refresh()
}

async function generateSlides(carouselId) {
  await $fetch("http://127.0.0.1:8000/generations", {
    method: "POST",
    body: {
      carousel_id: carouselId
    }
  })
  
  refresh()
}

async function exportCarousel(carouselId) {
  try {
    const response = await fetch("http://127.0.0.1:8000/exports", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        carousel_id: carouselId
      })
    })
    
    if (!response.ok) {
      throw new Error("Export failed")
    }
    
    const blob = await response.blob()
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement("a")
    link.href = url
    link.download = `carousel_${carouselId}_export.zip`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
  } catch (error) {
    console.error("Export error:", error)
    alert("Export failed")
  }
}

</script>

<template>

<div style="padding:40px;font-family:Arial">

<h1>Carousel Generator</h1>

<h2>Create carousel</h2>

<div style="margin-bottom:20px">

<input v-model="title" placeholder="Title" style="display:block;margin-bottom:10px;padding:8px;width:300px"/>

<textarea v-model="text" placeholder="Source text" style="display:block;margin-bottom:10px;padding:8px;width:300px;height:80px"></textarea>

<input type="number" v-model="slides" style="display:block;margin-bottom:10px;padding:8px;width:100px"/>

<button @click="createCarousel" style="padding:10px 20px">
Create
</button>

</div>

<hr/>

<h2>My Carousels</h2>

<button @click="refresh()">Reload</button>

<div v-if="!carousels">
Loading...
</div>

<div v-else>

<div
v-for="carousel in carousels"
:key="carousel.id"
style="border:1px solid #ccc;padding:10px;margin-top:10px"
>

<h3>{{ carousel.title }}</h3>

<p>Status: {{ carousel.status }}</p>

<p>Slides: {{ carousel.slides_count }}</p>

<button
@click="generateSlides(carousel.id)"
style="padding:8px 16px;margin-top:10px;margin-right:10px;background:#FF9800;color:white;border:none;cursor:pointer"
>
Generate slides
</button>

<button
@click="navigateTo(`/editor/${carousel.id}`)"
style="padding:8px 16px;margin-top:10px;margin-right:10px;background:#2196F3;color:white;border:none;cursor:pointer"
>
Open editor
</button>

<button
@click="exportCarousel(carousel.id)"
style="padding:8px 16px;margin-top:10px;background:#4CAF50;color:white;border:none;cursor:pointer"
>
Export
</button>

</div>

</div>

</div>

</template>
