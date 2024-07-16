<!-- MapCard.vue -->
<template>
    <div 
      class="relative flex items-center w-full h-28 bg-cover" 
      :style="{ backgroundImage: `url(${map.previewUrl})` }" 
      @click.prevent="handleClick"
    >
      <div class="absolute inset-0 bg-black opacity-25 transition-opacity duration-300"></div>
      <div class="flex items-center w-full h-full relative overflow-hidden">
        <div 
          v-if="map.banned" 
          class="flex flex-col w-32 h-full bg-red-500 z-10 justify-center transition-transform duration-300"
        >
          <img :src="Ban" class="m-auto" />
          <h1 class="font-koulen text-white m-auto text-sm">Banned</h1>
        </div>
        <div 
          v-else-if="map.picked" 
          class="flex flex-col w-32 h-full bg-green-500 z-10 justify-center transition-transform duration-300"
        >
          <img :src="Pick" class="m-auto" />
          <h1 class="font-koulen text-white m-auto text-sm">Picked</h1>
        </div>
        <img 
          :src="map.title" 
          class="z-10 transform transition-transform duration-300 ml-[-3.5rem]" 
          :class="{ 'translate-x-16': map.banned || map.picked }"
        >
      </div>
    </div>
  </template>
  
  <script setup>
  import Ban from '../assets/maps/ban.svg';
  import Pick from '../assets/maps/pick.svg';
  
  const props = defineProps({
    map: Object,
    currentTurn: Number,
    isMyTurn: Boolean,
  });
  
  const emit = defineEmits(['banMap', 'pickMap']);
  
  const handleClick = () => {
    if (!props.isMyTurn) return;
  
    if (props.map.banned || props.map.picked) return;
  
    if (props.currentTurn === 0 && props.currentStage === 'ban') {
      emit('banMap', { mapId: props.map.id });
    } else if (props.currentTurn === 1 && props.currentStage === 'pick') {
      emit('pickMap', { mapId: props.map.id });
    }
  };
  </script>
  